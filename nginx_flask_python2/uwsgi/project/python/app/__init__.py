import os,sys
from flask import Flask

app = Flask(__name__)
# read setting from config.py
app.config.from_object('config.system')

#register blueprint
from alignment.router import mod as alignment_mod
app.register_blueprint(alignment_mod, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'alignment'))
from seq_trans.router import mod as seq_trans_mod
app.register_blueprint(seq_trans_mod, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'seq_trans'))


# shared app
sys.path.append(os.path.join(os.path.dirname(__file__),'../share_app'))
from url_test.router import mod as mod_test
app.register_blueprint(mod_test, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'url_test'))
from taxa.router import mod as mod_taxa
app.register_blueprint(mod_taxa, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'taxa'))
from kegg.router import mod as mod_kegg
app.register_blueprint(mod_kegg, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'kegg'))
from go.router import mod as mod_go
app.register_blueprint(mod_go, url_prefix=os.path.join('/',app.config['PROJECT_NAME'],'go'))
