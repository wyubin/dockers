import os,json,sys
#sys.path.append(os.path.join(os.path.split(__file__)[0],'../../'))
from share_util import blast_tool

# define args list and file args in POST args
arg2fw={'fa':'query.fna'}
args=['e','gc','ms','ws','db','job_title','prog','mail']

def parse(job_path):
	blast_file = os.path.join(job_path,'blast.xml')
	if os.path.exists(blast_file):
		colnames = ['t_id','q_s','q_e','t_s','t_e','e','ident','a_r','q_align','t_align']
		query_names,b_info = [],[]
		q_count = 0
		for i in blast_tool.parser(open(blast_file)):
			b_info.append([[x.t_id,x.q_s,x.q_e,x.t_s,x.t_e,x.e,x.ident,x.a_r,x.q_align,x.t_align] for x in i])
			query_names.append(i[0].q_id)
			q_count += 1
		return {'names':query_names,'labels': colnames, 'datas':b_info}
	else:
		return False

def execute(job_path,info):
	j_conf = json.load(open(os.path.join(job_path,'args.json')))
	# assemble blast args
	blast_s = '%s -db %s -query %s -out %s' % (j_conf['prog'],os.path.join(info['db_path'],j_conf['db']),os.path.join(job_path,'query.fna'),os.path.join(job_path,'blast.xml'))
	blast_s += ' -evalue %s -num_threads %s -word_size %s' % (j_conf['e'],info['core_num'],j_conf['ws'])
	if 'ms' in j_conf:
		blast_s += ' -reward %s -penalty %s' % tuple(j_conf['ms'].split(','))
	if 'gc' in j_conf:
		blast_s += ' -gapopen %s -gapextend %s' % tuple(j_conf['gc'].split(','))
	err_path = os.path.join(job_path,'blast.err')
	os.system('%s -num_alignments 50 -outfmt 5 > %s' % (blast_s,err_path))
	if not os.path.getsize(err_path):
		os.unlink(err_path)
