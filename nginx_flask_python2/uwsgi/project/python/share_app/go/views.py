import os.path
# load module from ex_project
from config import system as sys_conf
# load module from script_project
from share_util import go_io

app_conf = sys_conf.mconfig['go']
go_api = go_io.go_io(app_conf['db_path'])

def ex_type(gos):
	"separate type and extend go term"
	res = go_api.gos2type(gos)
	for i,j in res.items():
		res[i] = list(go_api.go_extend(j))
	return res
