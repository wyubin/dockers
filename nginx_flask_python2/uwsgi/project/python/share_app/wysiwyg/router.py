import os,json
from flask import Blueprint,request,jsonify,make_response
from config import wysiwyg as app_conf
from config import system as sys_conf

mod = Blueprint('wysiwyg', __name__)

@mod.route('/save_html/', methods = ['POST'])
def save_html():
	in_args = dict(((x,request.form.get(x,'')) for x in ['page','pw','body']))
	if len(app_conf.passwords)==0 or in_args['pw'] in app_conf.passwords:
		open(os.path.join(sys_conf._basedir,app_conf.html_dir,'%s.html' % in_args['page']),'w').write(in_args['body'].encode('utf-8'))
		return jsonify({'_msg':{'_type':'status','html':"your changes have saved!"}})
	else:
		return jsonify({'_msg':{'_type':'error','html':"permission denied!"}})

@mod.route('/load_img/')
def load_img():
	img_dir = os.path.join(app_conf.img_dir,request.args['page'])
	return make_response(json.dumps([os.path.join(sys_conf.index_url,img_dir,x) for x in os.listdir(os.path.join(sys_conf._basedir, img_dir))]))

@mod.route('/upload_img/', methods = ['POST'])
def upload_img():
	img_dir = os.path.join(app_conf.img_dir,request.form['page'])
	ext_set = set(['.svg','.png', '.jpg', '.jpeg', '.gif'])
	file = request.files['file']
	if file and os.path.splitext(file.filename)[1] in ext_set:
		t_img_path = os.path.join(img_dir,file.filename)
		file.save(t_img_path)
		return jsonify({'link':os.path.join(sys_conf.index_url,t_img_path)})
