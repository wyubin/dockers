import os,json,sys
sys.path.append(os.path.join(os.path.split(__file__)[0],'../../'))
import mzid_parser

# define args list and file args in POST args
arg2fw={'mgf_file':'submit.mgf'}
fw_ignore=['mgf_file']
args=['title','db','mail','enzyme']

def parse(job_path):
	f_res = os.path.join(job_path,'result.mzid')
	if os.path.exists(f_res):
		parser = mzid_parser.parser()
		d_res = parser.parse(open(f_res))
		return {'ms':d_res}
	else:
		return False

def execute(job_path,info):
	# load config from json
	j_conf = json.load(open(os.path.join(job_path,'args.json')))
	# assemble execute command
	str_exe = 'java -Xmx3500M -jar %s -s %s -d %s -e %s -o %s' % (
		info['jar'],
		os.path.join(job_path,'submit.mgf'),
		os.path.join(info['db_path'],j_conf['db']),
		j_conf['enzyme'],
		os.path.join(job_path,'result.mzid')
	)
	err_path = os.path.join(job_path,'error.log')
	print str_exe
	os.system('%s > %s' % (str_exe,err_path))
	if not os.path.getsize(err_path):
		os.unlink(err_path)
