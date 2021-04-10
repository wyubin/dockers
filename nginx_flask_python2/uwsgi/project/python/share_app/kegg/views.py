import os.path
# load module from ex_project
from config import system as sys_conf
# load module from script_project
from share_util import kegg_io

app_conf = sys_conf.mconfig['kegg']
kegg_api = kegg_io.kegg_io(app_conf['db_path'])

def _map_url(path_id):
	"based path_id to get map_url"
	return app_conf['fmt_map'] % path_id

def enrich_info(kos):
	t_path2kos = kegg_api.ko2path_dict(kos)
	return {
		'path2kos':t_path2kos,
		'path2name':{x:kegg_api.path2des.get(x).split('|') for x in t_path2kos}
	}

def map_info(kos,path_id):
	kos_coor = kegg_api.ko2map_info(kos,path_id)
	return {
		'kos_coor':kos_coor,
		'map_url':_map_url(path_id)
	}
