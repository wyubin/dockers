import os
from flask import Blueprint,request,jsonify,g
from app import sys_conf
from views import job_handler,mailer,args_han

mod = Blueprint('jobs', __name__)

@mod.route('/submit/', methods = ['POST'])
def submit():
	# job_info need guid,type,mail,ip
	job_info = dict([[x,request.form.get(x)] for x in ['guid','type','mail']]+[['ip',request.remote_addr]])
	job_o = job_handler().add_by_info(job_info)
	args_han(job_o).submit(request.form)
	# send a mail
	mailer().send(job_o,{'status':'submitted'})

	return jsonify({'guid':job_o.guid})

@mod.route('/get_args/')
def get_args():
	"get args json of a job"
	job_o = job_handler().get_by_guid(request.args['guid'])
	if job_o:
		args = args_han(job_o).get()
		if args:
			return jsonify(args)
		else:
			jsonify({'_msg':{'_type':'error','des':'job deleted'}})
	else:
		return jsonify({'_msg':{'_type':'error','des':'no this job'}})

@mod.route('/get_result/')
def get_result():
	"as an result parser, each call will check daemon running if job un-complete, return _msg if job un-completed"
	job_o = job_handler().get_by_guid(request.args['guid'])
	if job_o:
		if job_o.time_complete:
			result = args_han(job_o).parse()
			if result:
				return jsonify(result)
			else:
				return jsonify({'_msg':{'_type':'error','des':'data parse error'}})
		else:
			daemon_path = os.path.abspath(os.path.join(g.conf._basedir,g.conf.mconfig['jobs']['daemon_path']))
			proc = os.system('ps x | awk \'$6 == "%s"{ck=1;exit}END{if(!ck)system("nohup %s &")}\'' % (daemon_path,daemon_path))
			wait_list = job_handler().todo_list()
			return jsonify({'_msg':{'_type':'status','des':'your job ranking at %s' % (0 if not wait_list.count() else (job_o.id - job_handler().todo_list().first().id))}})
	else:
		return jsonify({'_msg':{'_type':'error','des':'no this job'}})
