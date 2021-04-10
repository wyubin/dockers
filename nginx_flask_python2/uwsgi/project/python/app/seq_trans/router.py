import os
from flask import Blueprint,request,jsonify
import views
#import views

mod = Blueprint('seq_trans', __name__)

@mod.route('/transdecoder/', methods = ['POST'])
def transdecoder():
	"get fmt,data,type and dump the viewer html"
	if 'fasta' in request.files:
		return jsonify(views.transdecoder(request))
	else:
		return jsonify({'_err':'no fasta file'})
