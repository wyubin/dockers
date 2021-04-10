#!/usr/bin/env python
import os,sys
import operator as op
from datetime import datetime
from peewee import SqliteDatabase
# load models
m_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(m_dir)
from models import db_proxy,Job,Job_type,Ip,Mail
# load local settings
l_dir = os.path.dirname(__file__)
sys.path.append(l_dir)
from config import system as sys_conf

class pkg():
	"""based on job model to remove specific job record and their files

	:param args: args
	:type args: dict
	"""
	def __init__(self, args={}):
		"add all options var into self"
		self.args = {}
		self.args.update(args)
		# addition
		self.m_conf = sys_conf.mconfig['jobs']
		# init load
		self.db_load()

	def db_load(self):
		"load db"
		db_path = os.path.join(sys_conf._basedir,self.m_conf['db_path'])
		db = SqliteDatabase(db_path, **sys_conf.DATABASE_CONNECT_OPTIONS)
		db_proxy.initialize(db)

	def job_filter(self):
		"return jobs based on criteria"
		jobs = Job.select()
		r_key = set(['from','before']).intersection(self.args.keys())
		if self.args.get('job_id'):
			jobs = jobs.where(Job.guid == self.args['job_id'])
		else:
			# date range
			for i in ['from','before']:
				if self.args[i]:
					t_op = op.ge if i=='from' else op.le
					jobs = jobs.where(t_op(Job.time_submit,datetime.strptime(self.args[i],'%Y-%m-%d')))
			if self.args['j_type']:
				jobs = jobs.join(Job_type,on=(Job.job_type == Job_type.id)).where(Job_type.name == self.args['j_type'])
			if self.args['mail']:
				jobs = jobs.join(Mail,on=(Job.mail == Mail.id)).where(Mail.addr == self.args['mail'])

		return jobs

	def job_remove(self,job):
		"remove job record and files"
		job.delete_instance()
		job_path = os.path.join(sys_conf._basedir,self.m_conf['doc_path'],job.guid)
		if os.path.exists(job_path):
			os.system('rm -rf %s' % job_path)

	def clean(self):
		"clean db based on their jobs item"
		# clean
		for i in [Ip,Mail]:
			for j in i.select():
				if j.jobs.count()==0:
					sys.stdout.write('clean %s without job\n' % j.addr)
					j.delete_instance()

	def main(self):
		# parse input rdp
		if not self.args['all']:
			jobs = self.job_filter()
		else:
			jobs = Job.select()
		jc = 0
		for i in jobs:
			jc += 1
			self.job_remove(i)
		# clean remainder mail and ip
		self.clean()
		sys.stdout.write('remove %s jobs in total\n' % jc)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description = pkg.__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-a','--all',help='remove all jobs', action='store_true', default=False)
	parser.add_argument('-f','--from',help='remove job with create date from...',metavar='date')
	parser.add_argument('-b','--before',help='remove job with create date until...',metavar='date')
	parser.add_argument('-t','--j_type',help='remove job which type name is...',metavar='type')
	parser.add_argument('-j','--job_id',help='remove job which job_id is...',metavar='job_id')
	parser.add_argument('-m','--mail',help='remove job which mail is...',metavar='mail_addr')
	args = parser.parse_args()

	a=pkg(vars(args))
	a.main()
