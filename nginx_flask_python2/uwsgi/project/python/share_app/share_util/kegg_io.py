import os.path
import plyvel
class kegg_io():
	"based kegg lvdb to get data"
	def __init__(self,path_db):
		for i in ['info','ko2sites','ko2des','site2path_coor','path2des']:
			setattr(self,i,plyvel.DB(os.path.join(path_db,i)))

	def ko2path_dict(self,kos):
		"aggregate ko list to path2kos"
		path2kos = {}
		for i in set(kos):
			t_sites = self.ko2sites.get(i)
			if t_sites:
				t_path = set([self.site2path_coor.get(x).split(',')[0] for x in t_sites.split(',')])
				for j in t_path:
					path2kos.setdefault(j,[]).append(i)

		return path2kos

	def ko2map_info(self,kos,path_id):
		"based ko list and path id to get map info(list of kos_coor)"
		site2kos,site2coor = {},{}
		for i in set(kos):
			t_sites = self.ko2sites.get(i)
			t_sites = [] if not t_sites else t_sites.split(',')
			for j in t_sites:
				t_pc = self.site2path_coor.get(j).split(',',1)
				# check path is selected
				if t_pc[0]==path_id:
					# check site got already
					if j not in site2coor:
						site2coor[j] = t_pc[1]
						site2kos[j]=[]
					site2kos[j].append(i)
		return [{'kos':y,'coor':site2coor[x]} for x,y in site2kos.items()]
