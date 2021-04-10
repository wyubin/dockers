"use model and other function tools to return data for routers"
import os,sys,json
from datetime import datetime
# project func
from config import system as sys_conf
from util import mod_db_updator as mod_update
# mod func
import mod_tools
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from share_util import mail_handler

tool_han = mod_tools._obj(sys_conf)

def state_run(req):
	"continue to check job valid and state to return {'err'} or {'state'} and response in state"
	conf = sys_conf.mconfig['db_updator']
	### init check
	check_fun = getattr(mod_update,'_init_ck')
	if check_fun:
		t_res = check_fun(req,conf)
		if 'err' in t_res:
			return t_res
	### return state
	res = {'state':tool_han.check_state()}
	if 'end' in res['state']:
		res['res'] = tool_han.state_load()
	return res

def state_push(req):
	"use POST to push state to daemon, run req_state first, then run daemon"
	conf = sys_conf.mconfig['db_updator']
	t_state = req.form['state']
	### start state, send req
	tool_han.state_make(t_state)
	conf.update({'tools':tool_han})
	req_fun = getattr(mod_update,'req_'+t_state,None)
	# if find req state function
	if req_fun:
		t_res = req_fun(req,conf)
		if t_res.get('err'):
			return t_res
	state_fun = getattr(mod_update,t_state,None)
	if state_fun:
		# then daemon
		daemon_path = os.path.abspath(conf['daemon'])
		proc_str = 'ps x | awk \'$6 == "%s"{ck=1;exit}END{if(!ck)system("nohup %s &")}\'' % (daemon_path,daemon_path)
		proc = os.system(proc_str)
	else:
		tool_han.state_make(t_state,json.dumps({'end':t_state}))

	return {'end':t_state}
