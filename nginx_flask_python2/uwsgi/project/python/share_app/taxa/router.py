import json
from flask import Blueprint,request,jsonify
from views import taxa_api,krona_html

mod = Blueprint('taxa_app', __name__)
def args_error(args_dict, args, errors):
	res = {}
	for i,j in enumerate(args):
		if j not in args_dict:
			return jsonify({'error':errors[i][0],'msg':errors[i][1]})
		else:
			res[j] = args_dict[j].encode('ascii','ignore')
	return res

@mod.route('/check/',methods = ['GET','POST'])
def check():
	"return available ids"
	args = args_error(request.args or request.form,['ids'],['query_key','please submit multiple taxid with "ids" key'])
	q_ids = set(args['ids'].split(','))
	h_ids,h_names = [], []
	for i in q_ids:
		t_name = taxa_api.tax2name.get(i)
		if t_name:
			h_ids.append(i)
			h_names.append(t_name)
	return jsonify({'h_ids':h_ids,'h_names':h_names})

@mod.route('/lineage/',methods = ['GET','POST'])
def lineage():
	"check the lineage levels and names"
	args = args_error(request.args or request.form,['ids'],['query_key','please submit multiple taxid with "ids" key'])
	q_ids = set(args['ids'].split(','))
	h_ids,taxname,lv_name,lv_id,ex = [],[],[],[],[]
	for i in q_ids:
		lv_ids = taxa_api.id2lv_ids(i)
		if not lv_ids:
			ex.append(i)
		else:
			h_ids.append(i)
			taxname.append(taxa_api.tax2name.get(i))
			lv_name.append([taxa_api.tax2name.get(x,'') for x in lv_ids])
			lv_id.append(lv_ids)
	return jsonify({
		'h_ids':h_ids,
		'taxname':taxname,
		'lv_name':lv_name,
		'lv_id':lv_id,
		'ex':ex,
		'default_lv':taxa_api.default_lv
	})

@mod.route('/lineage_id/',methods = ['GET','POST'])
def lineage_id():
	args = args_error(request.args or request.form,['ids'],['query_key','please submit multiple taxid with "ids" key'])
	q_ids = set(args['ids'].split(','))
	tax2line,ex = {},[]
	for i in q_ids:
		line_ids = taxa_api.id2line_ids(i)
		if len(line_ids)==1:
			ex.append(i)
		else:
			tax2line[i]=line_ids
	return jsonify({'tax2line':tax2line,'ex':ex})

@mod.route('/lca/',methods = ['GET','POST'])
def lca():
	"find LCA of multiple taxid from input"
	args = args_error(request.args or request.form,['ids'],['query_key','please submit multiple taxid with "ids" key'])
	q_ids = set(args['ids'].split(','))
	lca = taxa_api.lca(q_ids)

	return jsonify(lca)

@mod.route('/krona/',methods = ['POST'])
def krona():
	"POST tax2count and return krona html"
	# compatible with curl
	tax2count = request.form.get('tax2count')
	if tax2count:
		res=[]
		ex_ids = []
		for i,j in json.loads(tax2count).items():
			t_taxid = i.encode('ascii','ignore')
			lvs = taxa_api.id2lv_ids(t_taxid)
			if lvs:
				res.append([str(j)]+[taxa_api.tax2name.get(x,'') for x in lvs] if lvs else [''])
			else:
				ex_ids.append(t_taxid)
		# output a table file and run krona
		return jsonify({} if not res else {
			'ex_ids':ex_ids,'tsv':'\n'.join(['\t'.join(x) for x in res]), 'html':krona_html(res)
		})
