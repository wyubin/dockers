"use model and other function tools to return data for routers"
from flask import g
import os,sys,json
from peewee import SqliteDatabase
from models import db_proxy,Contig,ORF,Anno_db,Anno_hit,Anno_info,Taxa,FPKM
import operator as op
sys.path.append('../python/share_app')
from share_util import url_tool
# common args
op_list = ['lt','le','eq','ne','ge','gt']
# init views db
def db_conn():
	app_conf = g.conf.mconfig['rna_seq']
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
			if seq_type == 'orf':
				if i.orfs.count():
					orf = i.orfs[0]
					seq = {'name':'%s[%s]' % (i.name,orf.range_info),'seq':orf.seq}
				else:
					continue
			else:
				seq = {x:getattr(i,x) for x in ['name','seq']}
			seqs.append(seq)
		return seqs

	def anno_hits(self):
		"return hits info by annohits_v"
		res = {'hits':{},'db_info':{},'id2hits':{}}
		for i in self.model:
			if i.anno_infos.count():
				t_anno = annohit_v([x.anno_hit for x in i.anno_infos]).hits_dict()
				res['id2hits'][i.id] = t_anno['hits'].keys()
				for j,k in t_anno.items():
					res[j].update(k)
		return res

	def lineage_info(self):
		"return lineage info by taxa_v"
		tax_o,res = [],{'id2tax':{}}
		temp = [[tax_o.append(x.taxas[0]),res['id2tax'].update({x.id:x.taxas[0].taxa_id})] for x in self.model if x.taxas.count()]
		res.update(taxa_v(tax_o).lineage())
		res.update({'tax2comp':taxa_v(tax_o).tax2comp()})
		return res

	def value_search(self,args):
		"filter by Stat and FPKM cutoff"
		args.update({x:int(args[x]) for x in ['pvalue','fc','o_type','vs_ind','item','get_result'] if x in args})
		m_mod = Contig.select().join(Stat).join(FPKM,on=(FPKM.contig==Stat.contig)).where(getattr(Stat,'ind%s' % args['item']) < 1.0/(10**args['pvalue']))
		bool_filter = bool(set(args.keys()).intersection(['comp']))
		# define 4 sector
		qry_gr = [sum([getattr(FPKM,y) for y in x])/len(x) for x in Stat._groups[Stat._names[args['item']]][:2]]
		qry_0 = [x==0 for x in qry_gr]
		qry_fc = [qry_gr[x] > args['fc']*qry_gr[x-1] for x in range(2)]
		qry_set = [~qry_0[x-1] & qry_fc[x] for x in range(2)] + qry_0
		if args['get_result']:
			m_mod = m_mod.where(qry_set[args['vs_ind']])
			if 'comp' in args:
				args['comp'] = args['comp'].split(',') if type(args['comp'])!=list else args['comp']
				m_mod = m_mod.join(Taxa,on=(Taxa.contig==Contig.id)).where(Taxa.taxa_id.in_(*args['comp']))
			# output format switch
			if args['o_type']==0:
				# fpkm mode
				res = {'fpkm_label':FPKM._label,'c_names':[],'c_ids':[],'fpkm':[],'pvalue':[]}
				for i in m_mod:
					res['c_names'].append(i.name)
					res['c_ids'].append(i.id)
					res['fpkm'].append(fpkm_v(i.fpkms).s_fpkm())
					res['pvalue'].append(stat_v(i.stats).s_stat()[args['item']])
			elif args['o_type']==1:
				res = contig_v(m_mod).enrich_kegg()
			elif args['o_type']>1:
				res = contig_v(m_mod).enrich_go()
			# update filter_info if not from filter
			if not bool_filter:
				res.update({'filter_info':contig_v(m_mod).filter_info()})
			return res
		else:
			return {'counts':[m_mod.where(x).count() for x in qry_set]}

	def filter_info(self):
		"return filter_info(taxa) based on contig module"
		# Taxa
		tax2count,tax_set = {},[]
		for i in self.model:
			if i.taxas.count():
				tax_id = str(i.taxas[0].taxa_id)
				if tax_id not in tax2count:
					tax2count[tax_id] = 0
					tax_set.append(i.taxas[0])
				tax2count[tax_id] += 1
		comp2taxids = {}
		temp = [comp2taxids.setdefault(y,[]).append(x) for x,y in taxa_v(tax_set).tax2comp().items()]
		comp2count = {x:sum([tax2count[z] for z in y]) for x,y in comp2taxids.items()}
		return {'comp':{'to_taxids':comp2taxids,'to_count':comp2count}}

	def enrich_kegg(self):
		"count ac2counts(local,global),sel_num"
		sel_num = self.model.count()
		# get anno_db_id
		o_db = Anno_db.get(Anno_db.name=='kegg')
		ac2ids = {}
		m_mod = self.model.join(Anno_info,on=(Contig.id==Anno_info.contig)).join(Anno_hit,on=(Anno_hit.id==Anno_info.anno_hit)).join(Anno_db,on=(Anno_db.id==Anno_hit.anno_db))
		for i in m_mod.where(Anno_db.name==o_db.name):
			for j in i.anno_infos:
				if j.anno_hit.anno_db == o_db:
					t_ac = j.anno_hit.ac
					ac2ids.setdefault(t_ac,[]).append(i.id)
		# associated pathway
		enrich_info = json.loads(url_tool.post(self.app_conf['url_enrich_kegg'],{'kos':','.join(ac2ids.keys())}))
		# global data input
		t_info=json.load(open(os.path.join(g.conf.static_dir,g.conf.db_conn,'enrich_kegg.json')))
		enrich_info.update({
			'path2count':{x:t_info['path2count'][x] for x in enrich_info['path2kos'] if x in t_info['path2count']},
			'count_pool':t_info['pool_count']
		})
		return {'sel_num':sel_num,'ac2ids':ac2ids,'enrich_info':enrich_info}

	def enrich_go(self):
		"count ac2counts(local,global),sel_num"
		sel_num = self.model.count()
		go2ids = {'cc':{},'bp':{},'mf':{}}
		m_mod = self.model.join(Go,on=(Contig.id==Go.contig))
		for i in m_mod:
			t2gos = json.loads(url_tool.post(self.app_conf['url_go_extype'],{'gos':i.gos[0].goid}))
			for j,k in t2gos.items():
				temp = [go2ids[j].setdefault(x,[]).append(i.id) for x in k]
		go2ids = {x:y for x,y in go2ids.items() if y}
		# associated tree
		total_gos = []
		temp = [total_gos.extend(y.keys()) for x,y in go2ids.items()]
		go_tree = json.loads(url_tool.post(self.app_conf['url_go_type2tree'],{'gos':','.join(total_gos)}))
		# global data input
		t_info=json.load(open(os.path.join(g.conf.static_dir,'json','enrich_go.json')))
		pool_info = {'num':t_info['pool_count'],'go2num':{}}
		for i,j in go2ids.items():
			for t_goid in j.keys():
				pool_info['go2num'][t_goid] = t_info['go2count'][i][t_goid]

		return {'sel_num':sel_num,'go2ids':go2ids,'pool_info':pool_info,'go_tree':go_tree}

	def search_info(self):
		"return contig search info"
		data = [[x.name,x.id,bool(x.orfs),bool(x.fpkms),x.id] for x in self.model]
		return {'data':data,'anno':self.anno_hits()}

class fpkm_v(base):
	def __init__(self,model=None):
		self.app_conf = db_conn()
		self.model = model or FPKM.select()

	def fpkm(self):
		"return fpkm with ids and fpkms( or plus detail)"
		res={'ids':[],'names':[],'fpkms':[]}
		for i in self.model:
			res['ids'].append(i.contig.id)
			res['names'].append(i.contig.name)
			res['fpkms'].append(map(float,i.data.split(',')))
		return res

class taxa_v(base):
	def __init__(self,model=None):
		self.app_conf = db_conn()
		self.model = model or Taxa.select()

	def lineage(self):
		"output taxid map to their lv name + taxname"
		ids = [str(x.taxa_id) for x in self.model]
		t_url = json.loads(url_tool.post(self.app_conf['url_lineage'],{'ids':','.join(ids)}))
		return {
			'tax2names':{y:(t_url['lv_name'][x]+[t_url['taxname'][x]]) for x,y in enumerate(t_url['h_ids'])},
			'ex':t_url['ex'],
			'lv_tag':t_url['default_lv']
		}

	def tax2comp(self):
		"detect component group"
		ids = [str(x.taxa_id) for x in self.model]
		t_url = json.loads(url_tool.post(self.app_conf['url_lineage_id'],{'ids':','.join(ids)}))
		tax2comp = {'33208':'Coral','33630':'Symbiodinium','33634':'Symbiodinium','33090':'Symbiodinium','2':'Bacteria'}
		tax_set = set(tax2comp.keys())
		res = {}
		for i,j in t_url['tax2line'].items():
			t_inter = tax_set.intersection(j)
			if t_inter:
				res[i]=tax2comp[t_inter.pop()]
			else:
				res[i]='intermediate homology'
		return res

class annohit_v(base):
	def __init__(self,model=None):
		self.app_conf = db_conn()
		self.model = model or Anno_hit.select()

	def hits_dict(self):
		"list hits info with id key and other info"
		res = {'hits':{},'db_info':{}}
		for i in self.model:
			if i.id not in res['hits']:
				res['hits'][i.id] = {x:getattr(i,x) for x in ['ac','des']}
				res['hits'][i.id]['db'] = i.anno_db.id
				if i.anno_db.id not in res['db_info']:
					res['db_info'][i.anno_db.id] = {x:getattr(i.anno_db,x) for x in ['name','url_pre']}
		return res

	def search_info(self):
		"return info for data search"
		db_url,data = {},[]
		for i in self.model:
			data.append([i.anno_db.name,i.ac,i.des,list(set([y.contig.id for y in i.anno_infos]))])
			if i.anno_db.name not in db_url:
				db_url[i.anno_db.name] = i.anno_db.url_pre
		data = [[x.anno_db.name,x.ac,x.des,list(set([y.contig.id for y in x.anno_infos]))] for x in self.model]
		return {'data':data,'db_url':db_url}
