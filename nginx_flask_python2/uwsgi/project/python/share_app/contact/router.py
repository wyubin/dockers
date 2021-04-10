import os
from flask import Blueprint,request,jsonify
from views import quest_handler,mailer
from share_util import mail_handler

mod = Blueprint('contact', __name__)

@mod.route('/submit/', methods = ['POST'])
def submit():
	# check args
	info = dict([[x,request.form.get(x)] for x in ['q_type','content','mail']]+[['ip',request.remote_addr]])
	# check email available
	if mail_handler.verify(info['mail']):
		# save question
		q_o = quest_handler().add(info)
		# send a mail
		mailto = mailer().send({'mail':info['mail'],'content':info['content']},{'status':'submitted'})
		return jsonify({'_done':'thanks for your suggestion for %s time(s)' % q_o.mail.Question.count()})
	else:
		return jsonify({'_error':'check your mail available!'})
