import os,sys
from config import system as sys_conf
sys.path.append(os.path.join(os.path.dirname(__file__),'../../share_app/'))
from share_util import transdecoder as td

def transdecoder(req):
	"trans req.files['fasta'] as protein"
	args = {x:req.form.get(x) for x in ['code','multi','sense']}
	args['fasta'] = req.files['fasta']
	args['tmp'] = os.path.join(sys_conf.temp_dir,'transdecoder')
	td_han = td.pkg(args)
	return {'seqs':td_han.res()}
