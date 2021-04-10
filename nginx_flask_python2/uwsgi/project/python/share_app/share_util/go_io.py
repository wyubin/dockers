import os.path
import plyvel
class go_io():
	"based go lvdb to get data"
	def __init__(self,path_db):
		for i in ['info','go2type','go2des','go2pa']:
			setattr(self,i,plyvel.DB(os.path.join(path_db,i)))

	def go_extend(self,gos):
		"extend go term based on go2pa"
		base_gos = set([x for x in gos if self.go2des.get(x)])
		res_gos = set()
		while(len(base_gos)):
			res_gos.update(base_gos) # record current set
			base_gos = self.gos2pa(base_gos).difference(res_gos) # return next set with different to collected set

		return res_gos

	def gos2pa(self,gos):
		"find parents of input gos"
		go_pa = set()
		for i in gos:
			pas = self.go2pa.get(i,None)
			if pas:
				go_pa.update(pas.split(','))

		return go_pa

	def gos2type(self,gos):
		"separate go by type"
		res = {'bp':[],'cc':[],'mf':[]}
		for i in gos:
			t_type = self.go2type.get(i,None)
			if t_type:
				res[t_type].append(i)

		return {x:y for x,y in res.items() if y}

	def gos2tree(self,gos):
		"output single parent tree based on input gos"
		# find all extended go first
		ex_gos = self.go_extend(gos)
		# then extract all parents
		res = {}
		for i in ex_gos:
			pas = self.go2pa.get(i,None)
			if pas:
				res[i]=pas.split(',')[0]

		return res
