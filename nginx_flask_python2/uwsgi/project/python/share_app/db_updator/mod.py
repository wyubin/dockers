import os,timeit,subprocess
from datetime import datetime
#from werkzeug.utils import secure_filename

### args
# 'dir' is the main dir of db_updator
# 'dir_tmp' is dir of the process data of db_updator
# 'dir_ref' is dir of the always exit data of db_updator
###
e_path = '/home/wyubin/edirect'

def init():
	"return current version"
	return {'state':'init'}

def _init_ck(req,args):
	"if pass return True else False"
	t_pw = (req.args or req.form)['pw']
	if t_pw == args['pw']:
		return {'msg':'pass'}
	else:
		return {'err':'pw invalid'}

def req_update(req,args):
	"write file and version"
	log_w = args['_views'].log_write
	# write ver and comment
	v0,v1,t_cmt = [req.form[x] for x in ['v0','v1','comment']]
	log_w(args,"#version: %s.%s comment: %s" % (v0,v1,t_cmt or 'General update procedure'))
	# write files
	for i in ['gtr','gtr_seg','exr','ref_no_gb']:
		t_f = req.files[i]
		t_path = os.path.join(args['mod']['ref'],i)
		f_state = False
		if t_f.filename != '':
			t_f.save(t_path)
			f_state = True

		f_time = datetime.fromtimestamp(os.path.getmtime(t_path))
		log_w(args,'use %s in %s upload[%s]' % (i,'this' if f_state else 'previous',f_time.strftime('%Y-%m-%dT%H:%M:%SZ')))
	return {'state':'ok'}

def update(args):
	"main process to generate new db, run in deamon"
	log_w = args['_views'].log_write
	# get ncbi enterovirus genbank
	log_w(args,'Genbank info of enterovirus(txid12059) download... ')
	s_time = timeit.default_timer()
	#t_srp = '%s/esearch -db nuccore -query "txid12059 [ORGN:exp]" | %s/efetch -format gb > %s' \
	#	% (e_path,e_path,os.path.join(args['dir_tmp'],'nt_taxid12059.gb'))
	#os.system(t_srp)
	log_w(args,'processed in %ss' % int(timeit.default_timer()-s_time))

	# pre-process
	#s_time = timeit.default_timer()
	#t_srp = '/home/wyubin/python_module/file2sql/nhri_enterovirus/pre_process.py -a %s' % args['mod']['sql_conf']
	#p = subprocess.Popen([t_srp], stdout=subprocess.PIPE, shell=True)
	#log_w(args,p.stdout.read(),'genbank pre_process(%ss)' % int(timeit.default_timer()-s_time))

	# R: ncbi.taxonmy.utf8.r
	#s_time = timeit.default_timer()
	#t_srp = 'Rscript --vanilla util/ncbi.taxonmy.utf8.r %s' % args['mod']['tmp']
	#p = subprocess.Popen([t_srp], stdout=subprocess.PIPE, shell=True)
	#log_w(args,p.stdout.read(),'ncbi.taxonmy.r(%ss)' % int(timeit.default_timer()-s_time))
	# R: serotype.r
	s_time = timeit.default_timer()
	t_srp = 'Rscript --vanilla util/serotype.r %s' % args['mod']['tmp']
	p = subprocess.Popen([t_srp], stdout=subprocess.PIPE, shell=True)
	log_w(args,p.stdout.read(),'serotype.r(%ss)' % int(timeit.default_timer()-s_time))

	# constructs sql
	#s_time = timeit.default_timer()
	#t_srp = '/home/wyubin/python_module/file2sql/nhri_enterovirus/file2sql.py -a %s' % args['mod']['sql_conf']
	#p = subprocess.Popen([t_srp], stdout=subprocess.PIPE, shell=True)
	#log_w(args,p.stdout.read(),'DB construction(%ss)' % int(timeit.default_timer()-s_time))
	return {'_evt':{'mail':'update'}}

def cancel(args):
	"delete db and other process files"
	# os.system('rm %s' % os.path.join(args['dir_tmp'],'*'))
	return {'_evt':{'mail':'cancel','log_sw':'cancel','rm_state':'cancel'}}

def replace(args):
	"replace/backup db and generate static files"
	log_w = args['_views'].log_write
	log_w(args,'switch new and old DB...')
	# mv real_db to bak, mv new_db to real_db, mv bak to new_db
	bak_path = '%s.bak' % args['mod']['new_db']
	os.rename(args['mod']['real_db'],bak_path)
	os.rename(args['mod']['new_db'],args['mod']['real_db'])
	os.rename(bak_path,args['mod']['new_db'])
	# generate static files
	s_time = timeit.default_timer()
	t_srp = '/home/wyubin/python_module/file2sql/nhri_enterovirus/sql2static.py -s %s' \
		% args['mod']['setup_conf']
	p = subprocess.Popen([t_srp], stdout=subprocess.PIPE, shell=True)
	log_w(args,p.stdout.read(),'Prepare statistic files(%ss)' % int(timeit.default_timer()-s_time))
	return {'_evt':{'mail':'replace','log_sw':'replace','rm_state':'replace'}}

def restore(args):
	"restore sql from backup and switch now/old log, then process static build"
	replace(args)
	return {'_evt':{'mail':'restore','log_sw':'restore','rm_state':'restore'}}
