from flask import Blueprint,request,jsonify
import views

mod = Blueprint('kegg_app', __name__)
def query_format(dict_args,keys):
	"input args dict and format key and value into a new dict"
	return {i:dict_args[i].encode('ascii','ignore') for i in keys if dict_args.get(i,'') not in ['','undefined']}

@mod.route('/path2kos/', methods = ['POST'])
def path2kos():
	"based on kos to generate associated path and their kos"
	args = query_format(request.form,['kos'])
	if args:
		return jsonify(views.kegg_api.ko2path_dict(args['kos'].split(',')))

@mod.route('/enrich_info/', methods = ['POST'])
def enrich_info():
	"based on kos generate path2kos path2name"
	args = query_format(request.form,['kos'])
	return jsonify(views.enrich_info(args.get('kos','').split(',')))

@mod.route('/map_info/', methods = ['POST'])
def map_info():
	"based on kos and path_id generate map_url and kos_coor"
	args = query_format(request.form,['kos','path_id'])
	return jsonify(views.map_info(args.get('kos','').split(','),args['path_id']))
