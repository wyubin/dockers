# upper key will input flask system by config.from_object
DEBUG = True
ADMINS = frozenset(['wyubin@iis.sinica.edu.tw'])
DATABASE_CONNECT_OPTIONS = {'check_same_thread':False}
import os,json
config_dir = os.path.dirname(os.path.abspath(__file__))
_basedir = os.path.dirname(config_dir)
PROJECT_NAME = os.path.split(_basedir)[1]
static_dir = os.path.join(_basedir,"static")
base_url = 'http://symbiont.iis.sinica.edu.tw'
index_url = os.path.join(base_url,PROJECT_NAME)
smtp_info={
	'server':'smtp.gmail.com:587',
	'account':'synbiont401@gmail.com',
	'password':'06111979'
}
# load modules' config
mconfig = {x[0]:json.load(open(os.path.join(config_dir,''.join(x)))) for x in [os.path.splitext(y) for y in os.listdir(config_dir)] if x[1] == '.json'}
# multi db setting
_sdb = ''

def conf_update(conf_id=None):
	"update conf by conf_id"
	if conf_id:
		t_path = os.path.join(static_dir,conf_id,'conf.server.json')
		t_conf = json.load(open(t_path))
		temp = [mconfig[x].update(y) for x,y in t_conf.items()]
	return mconfig

def req2sdb(req):
	"update mconf and return conf id by input request"
	_sdb = os.path.split(os.path.dirname(request.referrer))[1]
	return _sdb
