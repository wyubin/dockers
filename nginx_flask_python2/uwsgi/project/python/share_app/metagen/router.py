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

@mod.route('/contig_count/', methods = ['POST'])
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
			res['count_info']=views.count_v([x.counts.get() for x in t_contig]).data()
			res['taxa']=views.contig_v(t_contig).lineage_info()
			return jsonify(res)
