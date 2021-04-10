from flask import Blueprint,jsonify,request
import views
# register a mod name in blueprint
mod = Blueprint('db_updator', __name__)

@mod.route('/state_run/', methods = ['GET'])
def state_run():
	"check password and check state"
	return jsonify(views.state_run(request))

@mod.route('/state_push/', methods = ['POST'])
def state_push():
	"push state with 'state' and its request"
	return jsonify(views.state_push(request))
