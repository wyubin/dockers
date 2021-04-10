from flask import Blueprint,request,jsonify

mod = Blueprint('url_test', __name__)
def query_format(dict_args,keys):
	"input args dict and format key and value into a new dict"
	return {i:dict_args[i].encode('ascii','ignore') for i in keys if dict_args.get(i,'') not in ['','undefined']}

@mod.route('/args/', methods = ['GET','POST'])
def path2kos():
	"test ajax by GET or POST"
	args = query_format(request.args or request.form,['key','value'])
	args.update({'method':'POST' if request.form else 'GET'})
	if args:
		return jsonify(args)
