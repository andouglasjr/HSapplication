import base64
from imutils.video import VideoStream
from flask import Response, jsonify, render_template, request, session, stream_with_context, url_for
from flask_session import Session

import numpy as np
import imutils
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

# Directories
SAVED_HOLOGRAMS_DIR = os.path.join(app.static_folder, 'saved_holograms')


@app.route("/hologram_acquisition")
def hologram_acquisition():
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


def list_images_folder():
    images = [
        f for f in listdir(SAVED_HOLOGRAMS_DIR)
        if isfile(join(SAVED_HOLOGRAMS_DIR, f))
    ]
    return images


@app.route('/record_hologram', methods=['POST'])
def record_hologram():
    if request.method == 'POST':
        img_uri_recorded = request.form.get('image_uri')
        experiment_name = request.form.get('exp_name')
        holo_attr = request.form.get('holo_attrs')
        filename = request.form.get('filename')
        file_path = os.path.join(SAVED_HOLOGRAMS_DIR, filename)
        image_name = None

        if img_uri_recorded is not None:
            img_uri_recorded = request.form['image_uri']
            filename = os.path.split(img_uri_recorded)[0] + '_' + str(
                random.random()) + '.png'

            img_uri = img_uri_recorded.split(',')[1]
            imgdata = base64.b64decode(img_uri)
            image = np.asarray(bytearray(imgdata), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
            image = image.astype(float)

        result = utils.generate_experiment_tree_directory(experiment_name)

        HOLOGRAM_DIR = 'results/' + experiment_name + '/hologram'
        HOLOGRAM_DIR_PATH = os.path.join(app.static_folder, HOLOGRAM_DIR)

        if result is not None:

            if holo_attr is None:
                if img_uri_recorded is None:
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
            path_image_static = url_for('processing_hologram', image='results/'+experiment_name+'/hologram/'+image_name)

            if img_uri_recorded is not None:
                with open(path_image, 'wb') as f:
                    f.write(imgdata)

            session['hologram_metadata'] = hologram_metadata

    return jsonify({'result': 'sucess', 'path': path_image_static})
