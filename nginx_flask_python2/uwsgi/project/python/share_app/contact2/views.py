import os,sys
from jinja2 import Environment, FileSystemLoader
from peewee import SqliteDatabase
from flask import g
from models import db_proxy,db_init,Qtype,Ip,Mail,Question
# load share_app module
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from share_util import mail_handler

def app_conf():
	"init db and return app_conf"
	m_conf = g.conf.mconfig['contact']
	db_path = os.path.join(g.conf._basedir,m_conf['db_path'])
	db = SqliteDatabase(db_path, **g.conf.DATABASE_CONNECT_OPTIONS)
	# proxy to db
	db_proxy.initialize(db)
	if not os.path.exists(db_path):
		db_init(db,m_conf)
	return m_conf

class quest_handler():
	"""offer a interface to treat web job
	"""
	def __init__(self):
		self.m_conf = app_conf()

	def add(self,info):
		"save from request"
		q_o = Question(content=info['content'],qtype=Qtype.get(Qtype.id==info['q_type']))
		q_o.ip=self._ip_check(info['ip'])
		q_o.mail=self._mail_check(info['mail'])
		q_o.save()
		return q_o

	def _ip_check(self,ip_addr):
		"check ip exist or not and return ip object"
		t_sql = Ip.select().where(Ip.addr == ip_addr)
		if t_sql.count():
			return t_sql[0]
		else:
			return Ip.create(addr=ip_addr,country='default')

	def _mail_check(self,mail_addr):
		"check mail exist or not and return mail object"
		t_sql = Mail.select().where(Mail.addr == mail_addr)
		if t_sql.count():
			return t_sql[0]
		else:
			return Mail.create(addr=mail_addr)

class mailer():
	"""based on mail_handler and jinja template to send html mail to user
	"""
	def __init__(self):
		self.m_conf = app_conf()
		self.env = Environment(loader=FileSystemLoader(self.m_conf['mail_tmpl']))

	def send(self,q_o,tmpl_name = 'notify'):
		"send based on ques object and tmpl name"
		t_args = {'content':q_o.content,'q_type':q_o.qtype.name}
		t_args.update(self.m_conf['mail_info'])
		t_args.update({'index_url':g.conf.index_url})
		tmpl = self.env.get_template(tmpl_name+'.tmpl.html')
		body =tmpl.render(t_args)
		mail_han = mail_handler.mail_handler(g.conf.smtp_info['account'],g.conf.smtp_info['password'],g.conf.smtp_info['server'])
		t_mails = {x:y[:] for x,y in self.m_conf['mail_list'].items()}
		t_mails['To'].append(q_o.mail.addr)
		return mail_han.send(t_mails,self.m_conf['titles'][tmpl_name],body,'html')
