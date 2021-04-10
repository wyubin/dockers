import json,os
import conf
from subprocess import Popen, PIPE, STDOUT

class mview():
	"""based on mview to output alignment view
	"""
	def __init__(self):
		self.info = conf.mview_info
	
	def html_table(self,args):
		"only output table part of html"
		shs = '%s -ruler on -html data -css on -coloring identity -width 100 -colorfile %s -in %s -colormap %s'
		shs = shs % (self.info['bin_path'],self.info['color_map'],self.info['fmt_dict'].get(args['fmt'],'pearson'),args['type'])
		sh = Popen(shs,stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
		t_html = sh.communicate(input=args['data'])[0]
		return t_html[:6]+' class="align"'+t_html[6:]
