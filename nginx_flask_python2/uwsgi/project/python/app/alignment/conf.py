from config import system as config
import os
mview_info = {
	'fmt_dict':{'fasta':'pearson','clustal':'clustal','blast':'blast'},
	'work_dir':os.path.join(config.static_dir,'doc','mview'),
	'bin_path':os.path.join(config._basedir,'util','mview-1.56','bin','mview'),
	'color_map':os.path.join(config._basedir,'util','mview.color'),
}
