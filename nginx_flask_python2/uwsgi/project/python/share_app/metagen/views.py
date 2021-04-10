"use model and other function tools to return data for routers"
from flask import g
import os,sys,json
from peewee import SqliteDatabase
from models import db_proxy,Contig,Taxa,Count
import operator as op
sys.path.append('../python/share_app')
from share_util import url_tool
# common args
op_list = ['lt','le','eq','ne','ge','gt']
# init views db
def db_conn():
	app_conf = g.conf.mconfig['metagen']
	db_path = os.path.join(g.conf._basedir,app_conf['db_path'])
	db = SqliteDatabase(db_path, **g.conf.DATABASE_CONNECT_OPTIONS)
	db_proxy.initialize(db)
	return app_conf

class base():
	def filter(self,key,str_op,value):
		"univeral filter function"
		if str_op in op_list:
			exp_wh = getattr(op,str_op)(getattr(self.model.model_class,key),value)
		else:
			exp_wh = getattr(getattr(self.model.model_class,key),str_op)(*value if type(value)==list else [value])
		return self.model.where(exp_wh)

	def text_search(self,key,value):
		"use like to search by key word"
		return self.model.where(getattr(getattr(self.model.model_class,key),'contains')(value))

class contig_v(base):
	def __init__(self,model=None):
		self.app_conf = db_conn()
		self.model = model or Contig.select()

	def seq_info(self,seq_type='contig'):
		"return seq info including contig and orf"
		seqs=[]
		for i in self.model:
			seq = {x:getattr(i,x) for x in ['name','seq']}
			seqs.append(seq)
		return seqs

	def lineage_info(self):
		"return lineage info by taxa_v"
		tax_o,res = [],{'id2tax':{}}
		temp = [[tax_o.append(x.taxas[0]),res['id2tax'].update({x.id:x.taxas[0].taxa_id})] for x in self.model if x.taxas.count()]
		res.update(taxa_v(tax_o).lineage() if tax_o else {})
		return res

class count_v(base):
	def __init__(self,model=None):
		self.app_conf = db_conn()
		self.model = model or Count.select()

	def data(self):
		"return fpkm with ids and fpkms( or plus detail)"
		res={'ids':[],'names':[],'counts':[]}
		for i in self.model:
			res['ids'].append(i.contig.id)
			res['names'].append(i.contig.name)
			res['counts'].append(map(float,i.data.split(',')))
		return res

class taxa_v(base):
	def __init__(self,model=None):
		self.app_conf = db_conn()
		self.model = model or Taxa.select()

	def lineage(self):
		"output taxid map to their lv name + taxname"
		ids = [str(x.taxa_id) for x in self.model]
		t_url = json.loads(url_tool.post(url_tool.make(g.conf.service_conf,'taxa_lv'),\
			{'ids':','.join(ids)}))
		return {
			'tax2names':{y:(t_url['lv_name'][x]+[t_url['taxname'][x]]) for x,y in enumerate(t_url['h_ids'])},
			'ex':t_url['ex'],
			'lv_tag':t_url['default_lv']
		}
