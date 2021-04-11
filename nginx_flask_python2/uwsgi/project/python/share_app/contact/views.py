import json,os
from models import Qtype,Ip,Mail,Question
from datetime import datetime
from share_util import mail_handler
from jinja2 import Environment, FileSystemLoader
from config import contact as app_conf
from config import system as sys_conf

class quest_handler():
	"""offer a interface to treat web job
	"""
	def __init__(self):
		self.version = 'test'
	
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
		self.env = Environment(loader=FileSystemLoader(app_conf.mail_tmpl_path))

	def send(self,info,tmpl_args):
		"send with info as {'mail','content'}"
		info.update(app_conf.mail_info)
		info.update({'index_url':sys_conf.index_url})
		tmpl = self.env.get_template(tmpl_args['status']+'.tmpl.html')
		body =tmpl.render(info)
		mail_han = mail_handler.mail_handler(sys_conf.smtp_info['account'],sys_conf.smtp_info['password'],sys_conf.smtp_info['server'])
		t_mails = app_conf.mail_list.copy()
		t_mails.update({'To':[info['mail']]})
		return mail_han.send(t_mails,info['title'],body,'html')
