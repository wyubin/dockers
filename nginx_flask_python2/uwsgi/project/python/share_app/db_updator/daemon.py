#!/usr/bin/env python
import os,sys,json
sys.path.append(os.getcwd())
from config import system as sys_conf
from util import mod_db_updator as mod_update
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import mod_tools

tool_han = mod_tools._obj(sys_conf)

class main_fun():
	"daemon of db_updator"
	def __init__(self,**kwargs):
		self.env = {'core_num':kwargs['core_num']}

	def main(self):
		# check submit state
		t_state = tool_han.check_state()
		# run update
		m_conf = sys_conf.mconfig['db_updator']
		m_conf.update({'tools':tool_han})
		# set init var
		t_ctrl = {'_next':t_state['run']}
		while t_ctrl.get('_next'):
			r_state = t_ctrl['_next']
			tool_han.state = r_state
			tool_han.log_write('### [state:%s] start ###' % r_state)
			t_res = getattr(mod_update,r_state)(m_conf) or {}
			t_ctrl = t_res

		return json.dumps(t_res)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = main_fun.__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-c", "--core_num", help="core number for blast", default=4, type=int)
	args = parser.parse_args()
	a=main_fun(**vars(args))
	a.main()
