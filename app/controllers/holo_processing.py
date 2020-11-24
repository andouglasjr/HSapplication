from imutils.video import VideoStream
from flask import Response, jsonify, render_template, request, session
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


def thread_processing_hologram():
    global lock_processing, processing_frame, value_bright, value_contrast
    hologram_img = cv2.imread("static/test_img_out.bmp")
    img = hologram_img.copy()
    while True:
        effect = funcBrightContrast(img, int(value_bright),
                                    int(value_contrast))

        with lock_processing:
            processing_frame = effect.copy()


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

        print('Processing')
        print(hologram_metadata.dataArray)

        with open(filename_to_save, 'wb') as f:
            f.write(imgdata)

    return jsonify({'result': 'sucess', 'path': filename_to_web})


def get_hologram():
    global processing_frame, lock_processing
    while True:
        with lock_processing:
            if processing_frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", processing_frame)
            if not flag:
                continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) +
               b'\r\n')


@app.route("/show_hologram", methods=['POST', 'GET'])
def show_hologram():
    global value_bright, value_contrast
    if request.method == 'POST':
        value_bright = request.form.get('value_bright')
        value_contrast = request.form.get('value_contrast')
    else:
        value_bright = 128
        value_contrast = 60

    return Response(get_hologram(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/processing_hologram", methods=['POST', 'GET'])
def processing_hologram():
    global thread_camera, thread_processing, vs, raw_holo
    image_name = ""
    if request.method == 'GET':
        image_name = request.args['image']

    dir_path = os.path.dirname(os.path.dirname(__file__))
    filename = os.path.join(dir_path, image_name)

    return render_template("hologram_processing_boot.html", image=image_name)
