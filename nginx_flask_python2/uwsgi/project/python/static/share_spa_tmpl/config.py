import os
from datetime import datetime
class config(object):
	project_dir = os.path.split(os.path.abspath(os.path.join(os.path.dirname(__file__),'../../')))[1]
	base = {
		'title':'human somatic mutation analysis',
		'nav':{
			'order':['home','analyze'],
			'tab2html':{
				'home':'Home',
				'analyze':'Analyze'
			}
		},
		'footer':{
			'date_start':'2014',
			'company_html':'<a href="http://eln.iis.sinica.edu.tw/">Lab of Systems and Network Biology</a>,<br/><a href="http://www.iis.sinica.edu.tw/index.htm">Institute of Information Science</a>, <a href="http://www.sinica.edu.tw/main_e.shtml">Academic Sinica</a>',
		},
		'pages':['home','analyze']
	}
	_html_list = ['index']
	# static file
	js_src=[
		'../../../static/js/stdlib.uri_sw.js',
		'../../../static/js/uri_sw.Router.js',
		'../../../static/js/jquery.mynav.js',
		'../../../static/js/jquery.myfooter.js',
		'model_home.js',
		'model_analyze.js'
	]
	js_target='../js/index.bundle.min.js'
	css_src=['../../../static/css/mynav.min.css']
	css_target='../css/index.bundle.min.css'
