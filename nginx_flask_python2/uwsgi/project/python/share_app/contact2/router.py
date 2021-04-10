from flask import Blueprint,request,jsonify
from views import quest_handler,mailer,mail_handler

mod = Blueprint('contact', __name__)

@mod.route('/verify/', methods = ['GET'])
def verify():
	"verify mail by input mail address"
	ind = mail_handler.verify(request.args.get('mail'))
	return jsonify({'_res':'success' if ind else 'fail'})

@mod.route('/submit/', methods = ['POST'])
def submit():
	# check args
	info = dict([[x,request.form.get(x)] for x in ['q_type','content','mail']]+[['ip',request.remote_addr]])
	# save question
	q_o = quest_handler().add(info)
	# send a mail
	mailto = mailer().send(q_o)
	return jsonify({'send_count':q_o.mail.Question.count()})
