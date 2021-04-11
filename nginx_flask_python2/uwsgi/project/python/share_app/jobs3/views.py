import json,os,sys
from flask import g
from models import db_proxy,Job,Job_type,Ip,Mail,db_init
from datetime import datetime
from peewee import SqliteDatabase
from jinja2 import Environment, FileSystemLoader
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from share_util import guid, mail_handler
from app import sys_conf

app_conf = sys_conf.mconfig['jobs']
db_path = os.path.join(sys_conf._basedir,app_conf['db_path'])
db = SqliteDatabase(db_path, **sys_conf.DATABASE_CONNECT_OPTIONS)
db_proxy.initialize(db)
if not os.path.exists(db_path):
	db_init(db,app_conf)

# import job_types
sys.path.append(app_conf.get('mod_path',os.path.join(os.path.dirname(__file__),'mod_tools')))
import job_types

class job_handler():
	"""offer a interface to treat web job
	"""
	def __init__(self):
		self.version = 'test'
	
	def create_job(self,req):
		"create job by input request"
		t_guid = req.form.get('guid','')
		if t_guid:
			# use assign guid
			job_o = self.get_by_guid(t_guid)
			if job_o:
				job_o.delete_instance()
		else:
			# no guid or error guid, create a new guid
			t_guid = guid.id_get([x.guid for x in Job.select()])

		t_job = Job(guid=t_guid,job_type=Job_type.get(Job_type.name==req.form[app_conf.get('type_key','type')]))
		t_job.ip=self._ip_check(req.remote_addr)
		t_job.mail=self._mail_check(req.form.get(app_conf.get('mail_key','mail'),''))
		t_job.conf_id = getattr(g.conf,'_sdb',None)
		#t_job.save()
		return t_job

	def get_by_guid(self,guid):
		jobs = Job.select().where(Job.guid==guid)
		if jobs.count():
			return jobs[0]
		else:
			return None

	def _ip_check(self,ip_addr):
		"check ip exist or not and return ip object"
		t_sql = Ip.select().where(Ip.addr == ip_addr)
		if t_sql.count():
			return t_sql[0]
		else:
			return Ip.create(addr=ip_addr,country="default")

	def _mail_check(self,mail_addr):
		"check mail exist or not and return mail object"
		if mail_addr:
			t_sql = Mail.select().where(Mail.addr == mail_addr)
			if t_sql.count():
				return t_sql[0]
			else:
				return Mail.create(addr=mail_addr)
		else:
			return None

	def tag_process(self,job_o):
		job_o.time_process=datetime.now()
		job_o.save()
		return job_o

	def tag_complete(self,job_o):
		job_o.time_complete=datetime.now()
		job_o.save()
		return job_o

	def reset(self,job_o):
		"reset a job"
		job_o.time_submit = datetime.now()
		job_o.time_process = None
		job_o.time_complete = None
		job_o.save()
		return job_o

	def todo_list(self):
		return Job.select().where(Job.time_process==None)

class mailer():
	"""based on mail_handler and jinja template to send html mail to user
	"""
	def __init__(self):
		self.env = Environment(loader=FileSystemLoader(app_conf['mail_tmpl']))

	def send(self,job_o,status):
		"info need status['submitted','completed']"
		if job_o.mail:
			m_conf = self.m_conf(job_o)
			mail_info = {
				'guid':job_o.guid,
				'index_url':sys_conf.index_url
			}
			mail_info.update(m_conf['mail_info'])
			mail_info.update(m_conf['type2info'][job_o.job_type.name])
			t_mails = {x:y[:] for x,y in m_conf['mail_list'].items()}
			t_mails['To'].append(job_o.mail.addr)
			m_args = {
				'smpt_info':sys_conf.smtp_info,
				'mail_list':t_mails,
				'path':os.path.join(app_conf['mail_tmpl'],'%s.tmpl.html' % status),
				'args':mail_info,
				'title':mail_info['title']
			}
			return mail_handler.jinja2mail(m_args)
		else:
			False

	def m_conf(self,job_o):
		"return an updated app conf"
		if job_o.conf_id:
			sys_conf.conf_update(job_o.conf_id)
		return sys_conf.mconfig['jobs']

class args_han():
	"""submit (and create job dir) or get arguments of a job or parse result
	"""
	def __init__(self,job_o):
		self.path = os.path.join(g.conf._basedir,g.conf.mconfig['jobs']['doc_path'],job_o.guid)
		self.type_o = getattr(job_types,job_o.job_type.name)

	def submit(self,req):
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		t_args = {}
		# general args
		for i,j in req.form.items():
			if i in self.type_o.arg2fw:
				open(os.path.join(self.path,self.type_o.arg2fw[i]),'w').write(j)
			elif i in self.type_o.args and j.strip():
				t_args[i]=j
		json.dump(t_args,open(os.path.join(self.path,'args.json'),'w'))
		# if have files
		for i,j in req.files.items():
			if j.filename != '':
				j.save(os.path.join(self.path,i))

		return t_args

	def get(self):
		if os.path.exists(self.path):
			t_args = json.load(open(os.path.join(self.path,'args.json')))
			# do not read file as args
			fw_ignore = getattr(self.type_o,'fw_ignore',[])
			for i,j in self.type_o.arg2fw.items():
				if i not in fw_ignore:
					t_args[i] = open(os.path.join(self.path,j)).read()

			return t_args
		else:
			return None

	def parse(self):
		return self.type_o.parse(self.path)

def daemon_ck():
	"run daemon (if no run) and return waiting count"
	daemon_path = os.path.abspath(os.path.join(g.conf._basedir,g.conf.mconfig['jobs']['daemon_path']))
	proc = os.system('ps x | awk \'$6 == "%s"{ck=1;exit}END{if(!ck)system("nohup %s &")}\'' % (daemon_path,daemon_path))
