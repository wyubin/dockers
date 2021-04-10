from flask import Blueprint,jsonify,request
import views
# register a mod name in blueprint
mod = Blueprint('rna_seq', __name__)

def query_format(keys):
	"input args dict and format key and value into a new dict"
	res = {}
	for i in keys:
		t_val = (request.args or request.form).get(i,'')
		if t_val in ['','undefined']:
			continue
		res[i] = t_val.split(',') if ',' in t_val else t_val
	return res

@mod.route('/test/', methods = ['POST'])
def test():
	args = query_format(['db_conn'])
	return jsonify(args)

@mod.route('/anno_search/', methods = ['GET'])
def anno_search():
	"search annotation by key word"
	args = query_format(['des'])
	if args:
		res = views.annohit_v().text_search('des',args['des'])
		return jsonify(views.annohit_v(res).search_info())

@mod.route('/contig_search/', methods = ['GET'])
def contig_search():
	"search contig by name"
	args = query_format(['name'])
	if args:
		res = views.contig_v().text_search('name',args['name'])
		return jsonify(views.contig_v(res).search_info())

@mod.route('/contig_fpkm/', methods = ['POST'])
def contig_fpkm():
	args = query_format(['key','value'])
	if args:
		t_op = 'eq' if type(args['value'])==str else 'in_'
		t_contig = views.contig_v().filter(args['key'],t_op,args['value'])
		t_fpkm = [x.fpkms.get() for x in t_contig if x.fpkms.count()]
		if t_fpkm:
			return jsonify(views.fpkm_v(t_fpkm).fpkm())

@mod.route('/contig_seq/', methods = ['GET','POST'])
def contig_seq():
	args = query_format(['key','value','seq_type'])
	if args:
		t_op = 'eq' if type(args['value'])!=list else 'in_'
		ctg_set = views.contig_v().filter(args['key'],t_op,args['value'])
		res = views.contig_v(ctg_set).seq_info(args.get('seq_type',None))
		if res:
			return jsonify({'seqs':res})

@mod.route('/contig_detail/', methods = ['GET','POST'])
def contig_detail():
	"based key and value to search contig model, if value contain ',', the operator will be 'in_', not 'eq'"
	args = query_format(['key','value'])
	res={}
	if args:
		t_op = 'eq' if type(args['value'])==str else 'in_'
		t_contig = views.contig_v().filter(args['key'],t_op,args['value'])
		if t_contig.count():
			res['ids'] = [x.id for x in t_contig]
			res['seqs']=views.contig_v(t_contig).seq_info()
			res['orf_seqs']=views.contig_v(t_contig).seq_info('orf')
			res['express']=views.fpkm_v([x.fpkms.get() for x in t_contig if x.fpkms.count()]).fpkm()
			res['anno']=views.contig_v(t_contig).anno_hits()
			res['taxa']=views.contig_v(t_contig).lineage_info()
			return jsonify(res)

@mod.route('/enrich_kegg/', methods = ['POST'])
def enrich_kegg():
	"use the input key and value to find contigs, then based on type to generate enrich_info"
	args = query_format(['key','value'])
	if args:
		t_op = 'eq' if type(args['value'])!=list else 'in_'
		ctg_set = views.contig_v().filter(args['key'],t_op,args['value'])
		res = views.contig_v(ctg_set).enrich_kegg()
		return jsonify(res)
