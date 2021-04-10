import os
from flask import Blueprint,request,jsonify
from config import jobs as app_conf
from config import system as sys_conf
import views

mod = Blueprint('jobs', __name__)
job_han = views.job_handler()
mail_han = views.mailer()

@mod.route('/submit/', methods = ['POST'])
def submit():
	# job_info need guid,type,mail,ip
	job_info = dict([[x,request.form.get(x)] for x in ['guid','type','mail']]+[['ip',request.remote_addr]])
	job_o = job_han.add_by_info(job_info)
	views.args_han(job_o).submit(request.form)
	# send a mail
	mail_han.send(job_o,{'status':'submitted'})

	return jsonify({'guid':job_o.guid})

@mod.route('/get_args/')
def get_args():
	"get args json of a job"
	job_o = job_han.get_by_guid(request.args['guid'])
	if job_o:
		args = views.args_han(job_o).get()
		if args:
			return jsonify(args)
		else:
			jsonify({'_msg':{'_type':'error','des':'job deleted'}})
	else:
		return jsonify({'_msg':{'_type':'error','des':'no this job'}})

@mod.route('/get_result/')
def get_result():
	"as an result parser, each call will check daemon running if job un-complete, return _msg if job un-completed"
	job_o = job_han.get_by_guid(request.args['guid'])
	if job_o:
		if job_o.time_complete:
			result = views.args_han(job_o).parse()
			if result:
				return jsonify(result)
			else:
				return jsonify({'_msg':{'_type':'error','des':'data parse error'}})
		else:
			daemon_path = os.path.abspath(os.path.join(sys_conf._basedir,app_conf.daemon_path))
			proc = os.system('ps x | awk \'$6 == "%s"{ck=1;exit}END{if(!ck)system("nohup %s &")}\'' % (daemon_path,daemon_path))
			#time.sleep(3)
			#proc.terminate()
			wait_list = job_han.todo_list()
			return jsonify({'_msg':{'_type':'status','des':'your job ranking at %s' % (0 if not wait_list.count() else (job_o.id - job_han.todo_list().first().id))}})
	else:
		return jsonify({'_msg':{'_type':'error','des':'no this job'}})
