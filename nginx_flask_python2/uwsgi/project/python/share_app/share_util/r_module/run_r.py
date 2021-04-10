import subprocess,os,json
from uuid import uuid4

def run(code_name,args,file_path=os.getcwd()):
	"run R with input args file and output file for python"
	# generate a valid uuid
	tid = uuid4().hex
	while "%s_%s.log" % (code_name,tid) in os.listdir(file_path):
		tid = uuid4().hex
	tname = os.path.join(file_path,"%s_%s" % (code_name,tid))
	code_path = os.path.join(os.path.split(__file__)[0],'%s.r' % code_name)
	# save args into json file
	json.dump(args,open('%s.args' % tname,'w'))
	r_cmd = "R CMD BATCH --no-save --no-restore '--args %s.args %s.out' %s %s.log" % (tname,tname,code_path,tname)
	if subprocess.call(r_cmd,shell=True):
		print(open('%s.log' % tname).read())
		raise

	res = json.load(open('%s.out' % tname))
	os.system('rm %s.*' % tname)
	return res
