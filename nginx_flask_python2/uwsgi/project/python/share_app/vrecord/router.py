import json
from flask import Blueprint,request,jsonify
from views import record_han

# router content
mod = Blueprint('vrecord', __name__)

@mod.route('/access/')
def access():
	"add record or add record times"
	# generate
	if 'type' in request.args:
		ip_addr = request.remote_addr
		v_string = request.args['type']
		ret = record_han().visit(ip_addr,v_string)
		if ret:
			return jsonify({'msg':'got msg from %s' % v_string})
		else:
			return jsonify({'msg':'no valid record type'})
	else:
		return jsonify({'msg':'check ajax item'})

@mod.route('/info/')
def info():
	"return info object of assigned type"
	if 'type' in request.args:
		v_string = request.args['type']
		ret = record_han().info(v_string)
		return jsonify(ret) if ret else jsonify({'msg':'no valid record type'})
