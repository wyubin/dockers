from flask import Blueprint,request,jsonify
import views

mod = Blueprint('jobs', __name__)
job_han = views.job_handler()
mail_han = views.mailer()

@mod.route('/guid_ck/')
def guid_ck():
	"check input guid if it had in db"
	job_o = job_han.get_by_guid(request.args['guid'])
	return jsonify({'_state':'reject' if job_o else 'pass'})

@mod.route('/submit/', methods = ['POST'])
def submit():
	# job_info need guid,type,mail,ip
	job_o = job_han.create_job(request)
	views.args_han(job_o).submit(request)
	job_o.save()
	# send a mail
	mail_han.send(job_o,'submitted')

	return jsonify({'guid':job_o.guid})

@mod.route('/get_args/')
def get_args():
	"get args json of a job to create form"
	job_o = job_han.get_by_guid(request.args['guid'])
	if job_o:
		args = views.args_han(job_o).get()
		if args:
			return jsonify(args)
	else:
		return jsonify({'_err':'no_job'})

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
				return jsonify({'_err':'parser_err'})
		else:
			job_count = views.daemon_ck()

			return jsonify({'_msg':'waiting'})
	else:
		return jsonify({'_err':'no_job'})
