from app import app
from flask import render_template
from app.controllers import holo_aquisition

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/test")
def test():
	return render_template("test.html")