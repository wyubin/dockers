# upper key will input flask system by config.from_object
DEBUG = True
ADMINS = frozenset(['wyubin@iis.sinica.edu.tw'])
DATABASE_CONNECT_OPTIONS = {'check_same_thread':False}
# custom general setting
import os,json
config_dir = os.path.dirname(os.path.abspath(__file__))
_basedir = os.path.dirname(config_dir)
db_dir = os.path.join(_basedir,'db')
share_app_dir = os.path.join(_basedir,'../python/share_app')

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
