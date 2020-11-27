from imutils.video import VideoStream
from flask import Response, jsonify, render_template, request, session, url_for
import numpy as np
import threading
import datetime
import imutils
import time
import cv2
import sys
from app import app
import pickle
import os
import matplotlib.pyplot as plt
import base64
import random

from app.controllers.hologram import Hologram

@app.route('/save_changes', methods=['POST'])
def save_changes():
    if request.method == 'POST':

        filename = os.path.split(request.form['filename'])[0] + '_' + str(
            random.random()) + '.png'

        img_uri = request.form['image_uri'].split(',')[1]
        imgdata = base64.b64decode(img_uri)
        image = np.asarray(bytearray(imgdata), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        image = image.astype(float)

        hologram_metadata = session.get('hologram_metadata')
        hologram_metadata.update_data(image)
        session['hologram_metadata'] = hologram_metadata

        filename_to_web = '/results/' + hologram_metadata.experiment + '/processed_hologram/' + filename
        filename_to_save = app.static_folder + filename_to_web

        with open(filename_to_save, 'wb') as f:
            f.write(imgdata)

    return jsonify({'result': 'sucess', 'path': url_for('holo_reconstruction', image=filename_to_web)})

@app.route("/processing_hologram", methods=['POST', 'GET'])
def processing_hologram():
    global thread_camera, thread_processing, vs, raw_holo
    image_name = ""
    if request.method == 'GET':
        image_name = request.args['image']

    dir_path = os.path.dirname(os.path.dirname(__file__))
    filename = os.path.join(dir_path, image_name)

    return render_template("hologram_processing_boot.html", image=image_name)
