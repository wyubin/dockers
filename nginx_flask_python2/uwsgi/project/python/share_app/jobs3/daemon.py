#!/usr/bin/env python
import os,sys
sys.path.append(os.getcwd())
from config import system as sys_conf
s_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(s_dir)
from views import job_handler, mailer

sys.path.append(sys_conf.mconfig['jobs'].get('mod_path',os.path.join(s_dir,'mod_tools')))
import job_types

class main_fun():
	"find sequence that associate input pfam id"
	def __init__(self,**kwargs):
		self.env = {'core_num':kwargs['core_num']}
		self.mail_han = mailer()
		self.job_han = job_handler()

	def main(self):
		j_list = self.job_han.todo_list()
		while j_list.count():
			t_job = self.job_han.tag_process(j_list[0])
			app_conf = self.mail_han.m_conf(t_job)
			jobs_path = os.path.join(os.path.dirname(__file__),app_conf['doc_path'])
			t_type = getattr(job_types,t_job.job_type.name)
			t_info = app_conf['type2args'][t_job.job_type.name]
			t_info.update(self.env)
			t_type.execute(os.path.join(jobs_path,t_job.guid),t_info)
			# job finish
			t_job = self.job_han.tag_complete(t_job)
			# send a mail
			self.mail_han.send(t_job,'completed')
			j_list = self.job_han.todo_list()

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = main_fun.__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-c", "--core_num", help="core number for blast", default=4, type=int)
	args = parser.parse_args()
	a=main_fun(**vars(args))
	a.main()
