import os
from flask import Blueprint,request,jsonify
from config import system as config
from views import *
#import views

mod = Blueprint('alignment', __name__)
app_dir = os.path.abspath(os.path.dirname(__file__))

@mod.route('/mview_html/', methods = ['POST'])
def mview_html():
	"get fmt,data,type and dump the viewer html"
	arg2def = {'fmt':'fasta','type':'dna'}
	args = {x:request.form.get(x,y) for x,y in arg2def.items()}
	if 'data' not in request.form:
		return jsonify({'_msg':{'type':'error','des':'need args "data" in your submit'}})
	else:
		args['data']=request.form['data']
		return jsonify({'html':mview().html_table(args)})
