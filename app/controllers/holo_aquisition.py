from imutils.video import VideoStream
from flask import Response, jsonify, render_template, request, session
from flask_session import Session

import numpy as np
import threading
import datetime
import imutils
import time
import cv2
import os
import random

from app import app
from app.controllers import holo_processing
from os import listdir
from os.path import isfile, join
from app.controllers.hologram import Hologram
from scipy.io import loadmat
import matplotlib.pyplot as plt
from PIL import Image
import app.controllers.utils as utils
thread_camera = None

#Directories
SAVED_HOLOGRAMS_DIR = os.path.join(app.static_folder, 'saved_holograms')


@app.route("/hologram_acquisition")
def hologram_acquisition():
    global lock, thread_camera, vs, lock
    lock = threading.Lock()

    if not thread_camera:
        vs = VideoStream(src=0)
        vs.start()
        time.sleep(2.0)

        thread_camera = threading.Thread(target=thread_acquisition)
        thread_camera.daemon = True
        thread_camera.start()

    images = [
        f for f in listdir(SAVED_HOLOGRAMS_DIR)
        if isfile(join(SAVED_HOLOGRAMS_DIR, f))
    ]

    return render_template("hologram_acquisition_boot.html",
                           card_images=images)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        print(request.files)
        if 'image1' not in request.files:
            return 'there is no upload_image in form!'

        upload_image = request.files['image1']
        path = os.path.join(SAVED_HOLOGRAMS_DIR, upload_image.filename)
        upload_image.save(path)

        return jsonify({
            'result': 'sucess',
            'images_folder': list_images_folder()
        })


def thread_acquisition():
    global vs, outputFrame, lock, rec_hologram, stop_thread
    rec_hologram = False
    stop_thread = False
    total = 0
    while not stop_thread:

        frame = vs.read()
        frame = imutils.resize(frame, width=600)

        with lock:
            outputFrame = frame.copy()

        if rec_hologram:
            while rec_hologram:
                continue


def generate():
    global outputFrame, lock
    while True:
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            if not flag:
                continue

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) +
               b'\r\n')


def capture(image_name):
    global outputFrame, lock, rec_hologram
    if rec_hologram:
        rec_hologram = False
    else:
        cv2.imwrite(SAVED_HOLOGRAMS_DIR + '/' + image_name, outputFrame)
        rec_hologram = True
    return rec_hologram


def list_images_folder():
    images = [
        f for f in listdir(SAVED_HOLOGRAMS_DIR)
        if isfile(join(SAVED_HOLOGRAMS_DIR, f))
    ]
    return images


@app.route('/stop_thread', methods=['POST'])
def stop_thread():
    global stop_thread, vs, thread_camera
    stop_thread = True
    vs.stream.stream.release()
    thread_camera = None

    image_name = None
    experiment_name = request.form.get('exp_name')
    holo_attr = request.form.get('holo_attrs')
    filename = request.form.get('filename')
    print(filename)

    result = utils.generate_experiment_tree_directory(experiment_name)

    HOLOGRAM_DIR = 'results/' + experiment_name + '/hologram'
    HOLOGRAM_DIR_PATH = os.path.join(app.static_folder, HOLOGRAM_DIR)

    if result is not None:
        file_path = os.path.join(SAVED_HOLOGRAMS_DIR, filename)
        if holo_attr is None:
            image = Image.open(file_path)
            image = np.array(image)

            if image.ndim == 3:
                image = np.squeeze(image, 2)

            hologram_metadata = Hologram(experiment=experiment_name)
            hologram_metadata.update_data(image)
            attr_save_plt = image
            image_name = 'hologram_' + str(random.random()) + '.png'
        else:
            holo_mat = loadmat(file_path)
            hologram_metadata = Hologram(experiment=experiment_name,
                                         data=holo_mat[holo_attr])

            image_name = 'mat_image_' + str(random.random()) + '.png'
            attr_save_plt = np.abs(holo_mat[holo_attr])

        path_image = os.path.join(HOLOGRAM_DIR_PATH, image_name)
        utils.save_image_with_plt(attr_save_plt, path_image)
        path_image_static = 'results/'+experiment_name+'/hologram/'+image_name

        session['hologram_metadata'] = hologram_metadata

    return jsonify({'result': result, 'image_path': path_image_static})


@app.route('/record_hologram', methods=['POST'])
def record_hologram():
    data = request.form['image_name']
    return jsonify({
        'result': 'sucess',
        'rec_hologram': capture(data),
        'images_folder': list_images_folder()
    })


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


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
