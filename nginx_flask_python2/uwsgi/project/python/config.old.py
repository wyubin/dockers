import os
_basedir = os.path.abspath(os.path.dirname(__file__))
class default(object):
	DEBUG = True
	ADMINS = frozenset(['wyubin@iis.sinica.edu.tw'])
	SECRET_KEY = 'SecretKeyForSessionSigning'
	DATABASE_URI = 'sqlite:///'
	DATABASE_CONNECT_OPTIONS = {'check_same_thread':False}
	THREADS_PER_PAGE = 8
	CSRF_ENABLED=True
	CSRF_SESSION_KEY="csrfpasswordfors_hystrix"
	APPLICATION_ROOT = _basedir
	# user define
	PROJECT_NAME = os.path.split(_basedir)[1]
	mod2db={
		'main':'db/main.sqlite'
	}
	static_dir = os.path.join(_basedir,"static")
	base_url = 'http://symbiont.iis.sinica.edu.tw'
	index_url = os.path.join(base_url,PROJECT_NAME)
	static_url = os.path.join(index_url,"static")
