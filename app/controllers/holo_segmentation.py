from app import app
from flask import render_template, jsonify, request
import pickle
import numpy as np
import os

@app.route('/holo_segmentation')
def holo_segmentation():
    global row_holo, display, show2d, fig
    #infile = open('app/static/hologram_data','rb')
    #row_holo = pickle.load(infile)
    #infile.close()
    image_name = ""
    if request.method == 'GET':
        image_name = request.args['image']

    dir_path = os.path.dirname(os.path.dirname(__file__))
    filename = os.path.join(dir_path, image_name)
    
    
    return render_template("hologram_segmentation_boot.html")
