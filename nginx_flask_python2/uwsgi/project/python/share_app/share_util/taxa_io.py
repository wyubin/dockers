import os.path,sys
try:
	import plyvel
except ImportError:
	print("No leveldb api")
from table_io import table_io
class taxa_io():
	"base ncbi tax handler(load 'tax2lv','tax2pare','tax2name')"

	def __init__(self,path_db,db_type='leveldb'):
		self.default_lv = ['superkingdom','phylum','class','order','family','genus','species']
		for i in ['tax2lv','tax2pare','tax2name']:
			if db_type=='leveldb':
				db=plyvel.DB(os.path.join(path_db,i))
			else:
				db={x:y for x,y in table_io(open(os.path.join(path_db,i)))}
			setattr(self,i,db)

	def id2line_ids(self,taxid):
		"get a ancestor taxid list of a taxid(str)"
		pare = self.tax2pare.get(taxid) or '1'
		res = [taxid]
		while(pare != '1'):
			res.append(pare)
			pare = self.tax2pare.get(pare)
		return res

	def id2lv_ids(self,taxid):
		"get tax name list of a taxid based on assign lv list, level by ['superkingdom','phylum','class','order','family','genus','species']"
		par_list = self.id2line_ids(taxid)
		if len(par_list)==1: # no parent info
			return []
		lv2par = {}
		for i in par_list:
			t_lv = self.tax2lv.get(i)
			if t_lv:
				lv2par[t_lv]=i
		return [lv2par.get(str(x),'') for x in range(7)]

	def ancestor_filter(self,ances_id,ids):
		"extract a list form input taxid list or set that has a assigned ances_id"
		return [x for x in ids if ances_id in set(self.id2line_ids(x))]

	def lca(self,ids):
		"get a common ancestor tax id and lv"
		id2lines = [self.id2line_ids(x) for x in ids]
		min_len = 1
		ex_id = []
		for ind,i in enumerate(id2lines):
			t_len = len(i)
			if t_len==1:
				ex_id.append(ids[ind])
				id2lines.remove(i)
			else:
				min_len = t_len if t_len>min_len else min_len

		ids2line = zip(*[[y for y in reversed(x)][:min_len] for x in id2lines])
		# set a leaf taxid as init lca
		lca_taxid = ids2line[-1][0]
		for x in range(len(ids2line)):
			if len(set(ids2line[x])) != 1:
				lca_taxid = ids2line[x-1][0]
				break
		return {'taxid':lca_taxid,'name':self.tax2name.get(lca_taxid),'exclude_ids':ex_id}

	def get_close_lv(self,taxid):
		"return closet ancestor name whose level in default lv"
		for i,j in enumerate(reversed(self.id2lv_ids(taxid))):
			if j:
				break
		return j,self.tax2name.get(j),self.default_lv[6-i]

	def db_extract(self,ids):
		"return dict needed with terminal ids"
		id_set=set()
		# gether associated id in ids
		temp = [id_set.update(self.id2line_ids(x)) for x in ids]
		db={}
		for i in ['tax2lv','tax2pare','tax2name']:
			db[i]={}
			for taxid in id_set:
				item = getattr(self,i).get(taxid)
				if item:
					db[i][taxid]=item
		return db
