from flask import Blueprint,request,jsonify
import views

mod = Blueprint('go_app', __name__)
def query_format(dict_args,keys):
	"input args dict and format key and value into a new dict"
	return {i:dict_args[i].encode('ascii','ignore') for i in keys if dict_args.get(i,'') not in ['','undefined']}

@mod.route('/ex_type/', methods = ['POST'])
def ex_type():
	"based on gos to generate type and extend go"
	args = query_format(request.form,['gos'])
	if args:
		return jsonify(views.ex_type(args['gos'].split(',')))

@mod.route('/tree_info/', methods = ['POST'])
def tree_info():
	"based on gos to generate tree and names"
	args = query_format(request.form,['gos'])
	gos = args['gos'].split(',') if 'gos' in args else []
	tree = views.go_api.gos2tree(gos)
	name = {x:views.go_api.go2des.get(x) for x in tree}
	return jsonify({'tree':tree,'name':name})
