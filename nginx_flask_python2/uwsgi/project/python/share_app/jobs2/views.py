import json,os
from flask import g
from models import db_proxy,Job,Job_type,Ip,Mail
from datetime import datetime
from peewee import SqliteDatabase
from jinja2 import Environment, FileSystemLoader
import GeoIP
from share_util import guid, mail_handler
import job_types
from app import sys_conf

app_conf = sys_conf.mconfig['jobs']
print(os.path.join(sys_conf._basedir,app_conf['db_path']))
db_path = os.path.join(sys_conf._basedir,app_conf['db_path'])
db = SqliteDatabase(db_path, **sys_conf.DATABASE_CONNECT_OPTIONS)
db_proxy.initialize(db)
if not os.path.exists(db_path):
	db.create_tables([Job_type,Ip,Mail,Job],safe=True)
	for i in app_conf['type2info']:
		Job_type.create(name=i)

class job_handler():
	"""offer a interface to treat web job
	"""
	def __init__(self):
		self.gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
	def add_by_info(self,info_o):
		"save a job from request"
		# check info_o in db or not
		t_sql = Job.select().where(Job.guid==info_o.get('guid',''))
		if t_sql.count(): # get match job, it's resubmit, reset time and mail
			t_sql[0].update(time_submit=datetime.now(),time_complete=None,time_process=None,mail=self._mail_check(info_o.get('mail',''))).execute()
			return t_sql[0]
		else:
			t_guid = guid.id_get([x.guid for x in Job.select()])
			t_job = Job(guid=t_guid,job_type=Job_type.get(Job_type.name==info_o['type']))
			t_job.ip=self._ip_check(info_o['ip'])
			t_job.mail=self._mail_check(info_o.get('mail',''))
			t_job.save()
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
			return Ip.create(addr=ip_addr,country=self.gi.country_code_by_name(ip_addr))

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

	def todo_list(self):
		return Job.select().where(Job.time_process==None)

class mailer():
	"""based on mail_handler and jinja template to send html mail to user
	"""
	def __init__(self):
		self.env = Environment(loader=FileSystemLoader(app_conf['mail_tmpl_path']))

	def send(self,job_o,info):
		"info need status['submitted','completed']"
		if job_o.mail:
			info.update(app_conf['mail_info'])
			args_path = os.path.join(sys_conf._basedir,app_conf['doc_path'],job_o.guid,'args.json')
			info.update({'args':json.load(open(args_path))})
			info.update({'index_url':sys_conf.index_url})
			info.update({'guid':job_o.guid,'type':job_o.job_type.name})
			tmpl = self.env.get_template(info['status']+'.tmpl.html')
			body =tmpl.render(info)
			mail_han = mail_handler.mail_handler(sys_conf.smtp_info['account'],sys_conf.smtp_info['password'],sys_conf.smtp_info['server'])
			return mail_han.send({'To':[job_o.mail.addr]},'%s %s:%s' % (info['title'],info['type'],info['guid']),body,'html')
		else:
			False

class args_han():
	"""submit (and create job dir) or get arguments of a job or parse result
	"""
	def __init__(self,job_o):
		self.path = os.path.join(sys_conf._basedir,app_conf['doc_path'],job_o.guid)
		self.type_o = getattr(job_types,job_o.job_type.name)

	def submit(self,args):
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		t_args = {}
		for i,j in args.items():
			if i in self.type_o.arg2fw:
				open(os.path.join(self.path,self.type_o.arg2fw[i]),'w').write(j)
			elif i in (self.type_o.args+app_conf['option_args']) and j.strip():
				t_args[i]=j
		json.dump(t_args,open(os.path.join(self.path,'args.json'),'w'))

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
