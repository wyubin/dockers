import os,uuid,json
from config import system as sys_conf
from share_util import taxa_io

app_conf = json.load(open(os.path.join(sys_conf._basedir,'config','taxa.json')))
taxa_api = taxa_io.taxa_io(app_conf['db_path'])

def krona_html(count2lv):
	"input count2lv list and return krona html"
	# setup unique path for file storage
	uid = str(uuid.uuid1())
	t_path = os.path.join(app_conf['job_path'],uid)
	open('%s.tsv' % t_path,'w').write(
		'\n'.join(['\t'.join(x) for x in count2lv])
	)
	# run krona script
	os.system('%s %s.tsv -c -o %s.html' % (app_conf['script'],t_path,t_path))
	t_html = open('%s.html' % t_path).read()
	os.system('rm -rf %s.*' % t_path)
	return t_html
