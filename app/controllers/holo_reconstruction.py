from app import app
from flask import render_template, jsonify, request, session
import pickle
import holopy as hp
from holopy.core.metadata import data_grid
import numpy as np
import os
from time import sleep
from app.controllers.hologram import Hologram
from scipy.io import loadmat
import json
import matplotlib.pyplot as plt
import random
from PIL import Image
import base64
import cv2
from solid import *
import app.controllers.utils as utils
plt.ioff()
#Directories


@app.route('/spatial_filter', methods=['POST'])
def spatial_filter():
    global data, ft, G, contains_zero, d_old
    if request.method == 'POST':
        pitch = float(request.form.get('pitch'))
        lenght = float(request.form.get('lenght'))
        zstart = float(request.form.get('zstart'))
        zend = float(request.form.get('zend'))
        step = float(request.form.get('step'))

        z = np.arange(zstart, zend, step)

        attrlist = {'pitch': pitch, 'lenght': lenght}
        
        hologram_metadata = session.get('hologram_metadata')
        hologram_metadata.update_attrs(attrlist)
        session['hologram_metadata'] = hologram_metadata
        RESULT_DIR = os.path.join(app.static_folder, 'results')        
        EXPERIMENT_NAME = hologram_metadata.experiment
        EXPERIMENT_DIR = os.path.join(RESULT_DIR, EXPERIMENT_NAME)
        RECONSTRUCTION_DIR = os.path.join(EXPERIMENT_DIR,
                                          'reconstructed_hologram')
        GENERAL_RESULTS_DIR = os.path.join(RECONSTRUCTION_DIR, 'general_results')

        holo_ = data_grid(
            hologram_metadata.dataArray.data,
            spacing=hologram_metadata.dataArray.attrs['pitch'],
            medium_index=1,
            illum_wavelen=hologram_metadata.dataArray.attrs['lenght'])

        data, ft, G, contains_zero, d_old = hp.apply_fft(holo_, z)

        fig = plt.figure()
        img = ft.data[0]

        dpi = fig.dpi  #get the default dpi value
        width_fig = ft.data[0].shape[1]
        height_fig = ft.data[0].shape[0]

        fig_size = (width_fig / dpi, height_fig / dpi)  #saving the figure size
        ax = plt.subplots(1, figsize=fig_size)
        plt.imshow(np.log(np.abs(ft.data[0])), cmap='gray')
        plt.axis('off')
        fig.tight_layout()
        rand_number = random.random()
        filename = '/fft' + str(rand_number) + '.png'
        plt.savefig(GENERAL_RESULTS_DIR + filename,
                    bbox_inches='tight',
                    transparent=True,
                    pad_inches=0,
                    dpi=dpi)
        filename = 'static/results/'+EXPERIMENT_NAME+'/reconstructed_hologram/general_results'+filename
        return json.dumps({'fft': filename})


@app.route('/reconstruct_from_fft', methods=['POST'])
def reconstruct_from_fft():
    global data, ft, G, contains_zero, d_old

    mask_pos_x = float(request.form.get('mask_pos_x'))
    mask_pos_y = float(request.form.get('mask_pos_y'))
    mask_width = float(request.form.get('mask_width'))
    mask_height = float(request.form.get('mask_height'))

    ft = apply_mask(ft, mask_pos_x, mask_pos_y, mask_width, mask_height)
    r, fft = hp.reconstrut_from_fft(data, ft, G, contains_zero, d_old)

    RESULT_DIR = os.path.join(app.static_folder, 'results')        
    hologram_metadata = session.get('hologram_metadata')
    EXPERIMENT_NAME = hologram_metadata.experiment
    EXPERIMENT_DIR = os.path.join(RESULT_DIR, EXPERIMENT_NAME)
    RECONSTRUCTION_DIR = os.path.join(EXPERIMENT_DIR, 'reconstructed_hologram')
    GENERAL_RESULTS_DIR = os.path.join(RECONSTRUCTION_DIR, 'general_results')

    amp_img, phase_img = utils.save_images(r, fft, RECONSTRUCTION_DIR)
    amp_img = 'static/results/'+EXPERIMENT_NAME+'/reconstructed_hologram/'+amp_img
    phase_img = 'static/results/'+EXPERIMENT_NAME+'/reconstructed_hologram/'+phase_img
    return json.dumps({'amp_img': amp_img, 'phase_img': phase_img})


def apply_mask(fft, mask_pos_x, mask_pos_y, mask_width, mask_height,
               image_scaleX=None, image_scaleY=None):
    out = fft.copy()
    mask = np.zeros((round(out.data.shape[1]),
                     round(out.data.shape[2])))

    mask_pos_x = mask_pos_x
    mask_pos_y = mask_pos_y
    mask_width = mask_width
    mask_height = mask_height

    mask[round(mask_pos_y):round(mask_pos_y + mask_height),
         round(mask_pos_x):round(mask_pos_x + mask_width)] = 1 + 0j

    #mask = cv2.resize(mask, dsize=(out.data[0].shape[1], out.data[0].shape[0]))
    fft_ = out.data[0] * mask
    fft_ = np.expand_dims(fft_, 0)
    out.data = fft_

    log_fft_ = np.where(fft_ != 0, np.log(np.abs(fft_)), 0)

    fig = plt.figure()
    plt.imshow(log_fft_[0], cmap='gray')
    plt.axis('off')
    fig.tight_layout()
    rand_number = random.random()
    filename = '/fft_changed' + str(rand_number) + '.png'

    RESULT_DIR = os.path.join(app.static_folder, 'results')        
    hologram_metadata = session.get('hologram_metadata')
    EXPERIMENT_NAME = hologram_metadata.experiment
    EXPERIMENT_DIR = os.path.join(RESULT_DIR, EXPERIMENT_NAME)
    RECONSTRUCTION_DIR = os.path.join(EXPERIMENT_DIR, 'reconstructed_hologram')
    GENERAL_RESULTS_DIR = os.path.join(RECONSTRUCTION_DIR, 'general_results')

    plt.savefig(GENERAL_RESULTS_DIR + filename,
                bbox_inches='tight',
                transparent=False,
                pad_inches=0)

    return out


@app.route('/generate_stl', methods=['POST'])
def generate_stl():
    RESULT_DIR = os.path.join(app.static_folder, 'results')        
    hologram_metadata = session.get('hologram_metadata')
    EXPERIMENT_NAME = hologram_metadata.experiment
    EXPERIMENT_DIR = os.path.join(RESULT_DIR, EXPERIMENT_NAME)
    STL_FILES_DIR = os.path.join(EXPERIMENT_DIR, 'stl_files')
    FILES_DIR = os.path.join(app.static_folder, 'files')

    if request.method == 'POST':
        dgl = float(request.form.get('dgl'))
        dlc = float(request.form.get('dlc'))
        folder = FILES_DIR
        save_folder = STL_FILES_DIR
        scad_file = import_scad(folder + "/file.scad")
        out = scad_file.generate(dgl, dlc)
        scad_render_to_file(out, save_folder + '/out_file.scad')

        out_file_name = '/out_file_' + str(random.random()) + ".stl"
        os.system("openscad {} -o {}".format(save_folder + '/out_file.scad',
                                             save_folder + out_file_name))

        return json.dumps({
            'result': 'sucess',
            'out_file_name': out_file_name,
        })


@app.route('/reconstruct', methods=['POST'])
def reconstruct():
    if request.method == 'POST':
        pitch = float(request.form.get('pitch'))
        lenght = float(request.form.get('lenght'))
        zstart = float(request.form.get('zstart'))
        zend = float(request.form.get('zend'))
        step = float(request.form.get('step'))

        z = np.arange(zstart, zend, step)
        
        attrlist = {'pitch': pitch, 'lenght': lenght}
        hologram_metadata = session.get('hologram_metadata')
        hologram_metadata.update_attrs(attrlist)
        session['hologram_metadata'] = hologram_metadata

        holo_ = data_grid(
            hologram_metadata.dataArray.data,
            spacing=hologram_metadata.dataArray.attrs['pitch'],
            medium_index=1.333,
            illum_wavelen=hologram_metadata.dataArray.attrs['lenght'])
        
        #med_wavelen = holo_.illum_wavelen / holo_.medium_index
        r, fft = hp.propagate(holo_, z)

        hologram_metadata = session.get('hologram_metadata')
        RESULT_DIR = os.path.join(app.static_folder, 'results')
        EXPERIMENT_NAME = hologram_metadata.experiment
        EXPERIMENT_DIR = os.path.join(RESULT_DIR, EXPERIMENT_NAME)
        RECONSTRUCTION_DIR = os.path.join(EXPERIMENT_DIR,
                                          'reconstructed_hologram')
        GENERAL_RESULTS_DIR = os.path.join(RECONSTRUCTION_DIR, 'general_results')

        amp_img, phase_img = utils.save_images(r, fft, RECONSTRUCTION_DIR)
        
        amp_img = 'static/results/'+EXPERIMENT_NAME+'/reconstructed_hologram/'+amp_img
        phase_img = 'static/results/'+EXPERIMENT_NAME+'/reconstructed_hologram/'+phase_img

        return json.dumps({
            'result': 'sucess',
            'amp_img': amp_img,
            'phase_img': phase_img
        })


@app.route('/holo_reconstruction')
def holo_reconstruction():
    global row_holo, display, show2d, fig
    image_name = ""
    if request.method == 'GET':
        image_name = request.args['image']

    return render_template("hologram_reconstruction_boot.html",
                           image=image_name)
