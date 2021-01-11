from app import app
from flask import render_template

@app.route("/structural_dimensions")
def structural_dimensions():
	return render_template("structural_dimensions.html")
