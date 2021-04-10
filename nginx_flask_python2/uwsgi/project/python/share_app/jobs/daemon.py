#!/usr/bin/env python
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../python/share_app/'))
from config import jobs as app_conf
from util import job_types
from jobs.views import job_handler, mailer

class main_fun():
	"find sequence that associate input pfam id"
	def __init__(self,**kwargs):
		self.env = {'core_num':kwargs['core_num']}
		self.mail_han = mailer()
		self.job_han = job_handler()
	
	def main(self):
		j_list = self.job_han.todo_list()
		jobs_path = os.path.join(os.path.dirname(__file__),app_conf.doc_path)
		while j_list.count():
			t_job = self.job_han.tag_process(j_list[0])
			t_type = getattr(job_types,t_job.job_type.name)
			t_info = app_conf.type2info[t_job.job_type.name]
			t_info.update(self.env)
			t_type.execute(os.path.join(jobs_path,t_job.guid),t_info)
			# job finish
			t_job = self.job_han.tag_complete(t_job)
			# send a mail
			self.mail_han.send(t_job,{'status':'completed'})
			j_list = self.job_han.todo_list()

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = main_fun.__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-c", "--core_num", help="core number for blast", default=4, type=int)
	args = parser.parse_args()
	a=main_fun(**vars(args))
	a.main()
