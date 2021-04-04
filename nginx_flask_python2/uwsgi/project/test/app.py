from flask import Flask
app = Flask(__name__)

@app.route("/test/")
def index():
	return "Hello!, I'm flask"
