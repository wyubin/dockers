"tools for views and daemon based on sysconf"
import os,sys,json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from share_util import mail_handler

class _obj:
	def __init__(self,sys_conf,state=None):
		"record sys_conf for other function"
		self.sys_conf = sys_conf
		self.state = state
		self.m_conf = sys_conf.mconfig['db_updator']

	def mailer(self,tmpl_name=None):
		tmpl_name = tmpl_name or self.state
		m_conf = self.m_conf
		args = {
			'smpt_info':self.sys_conf.smtp_info,
			'mail_list':m_conf['mail']['list'],
			'path':os.path.join(m_conf['mail']['tmpl'],'%s.tmpl.html' % tmpl_name),
			'args':{
				'project_url':self.sys_conf.index_url,
				'update_url':os.path.join(self.sys_conf.index_url,m_conf['url'])
			},
			'title':'%s:%s' % (m_conf['mail']['info']['title'],tmpl_name)
		}
		return mail_handler.jinja2mail(args)

	def check_state(self):
		"check state based on *.state"
		t_state = 'init'
		end_ind = 1
		for i in self.m_conf['states']:
			s_path = os.path.join(self.m_conf['dir'],'%s.state' % i)
			if os.path.exists(s_path):
				t_state = i
				if not os.path.getsize(s_path):
					end_ind = 0
				break
		return {'end' if end_ind else 'run':t_state}

	def state_make(self,state=None,tag=None):
		"default add state or write into state, if tag == 'rm', remove the state"
		m_conf = self.m_conf
		# check valid state
		state = state or self.state
		if state not in m_conf['states']:
			raise NameError('invalid state')

		state_path = os.path.join(m_conf['dir'],'%s.state' % state)
		pre_state = self.check_state()
		#log_write(m_conf,'%s %s...' % (state,'start' if not tag else 'end'))
		if not tag:
			req_state = m_conf['state_need'].get(state)
			if req_state:
				if pre_state.get('end') != req_state:
					raise NameError('state_need')
				else:
					# remove pre state
					pre_path = os.path.join(m_conf['dir'],'%s.state' % pre_state.get('end'))
					if os.path.exists(pre_path):
						os.remove(pre_path)
			open(state_path,'w')
		elif tag=='rm':
			if os.path.exists(state_path):
				os.remove(state_path)
		else:
			# tag is the end response
			open(state_path,'w').write(tag)

	def state_load(self):
		"load state from current state file, parse by json"
		n_state = self.check_state()['end']
		if n_state!='init':
			return json.load(open(os.path.join(self.m_conf['dir'],'%s.state' % n_state)))
		else:
			return {'state':'init'}

	def log_write(self,log_str,session=None):
		"write log with or without session"
		t_str = '%s\n' % log_str
		if type(session) == str:
			t_str = ('=== log start [%s] ===\n' % session) +t_str+ ('=== log end [%s] ===\n' % session)
		open(os.path.join(self.m_conf['dir'],'new.log'),'a').write(t_str)

	def log_switch(self,state=None):
		"switch log based on state(replace,cancel,restore)"
		state = state or self.state
		t_p = {x:os.path.join(self.m_conf['dir'],x+'.log') for x in ['new','now','old']}
		old_time = datetime.fromtimestamp(os.path.getctime(t_p['old']))
		old_p = os.path.join(self.m_conf['dir'],'old_log','%s.log' % old_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
		if state == 'restore':
			os.rename(t_p['old'],t_p['new'])
		if state == 'replace':
			# save old log
			os.rename(t_p['old'],old_p)
		if state in ['replace','restore']:
			os.rename(t_p['now'],t_p['old'])
			os.rename(t_p['new'],t_p['now'])
		if state == 'cancel':
			os.remove(t_p['new'])
