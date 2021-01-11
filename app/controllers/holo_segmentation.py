from app import app
from flask import render_template, jsonify, request, session, url_for
import pickle
import numpy as np
import os
import json
import random

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data, io
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb


@app.route('/holo_segmentation')
def holo_segmentation():
    global row_holo, display, show2d, fig
    #infile = open('app/static/hologram_data','rb')
    #row_holo = pickle.load(infile)
    # infile.close()
    image_name = ""
    if request.method == 'GET':
        image_name = request.args['image']

    dir_path = os.path.dirname(os.path.dirname(__file__))
    filename = os.path.join(dir_path, image_name)

    return render_template("hologram_segmentation_boot.html", image=image_name)


@app.route('/segment', methods=['POST','GET'])
def segment():
    RESULT_DIR = os.path.join(app.static_folder, 'results')
    hologram_metadata = session.get('hologram_metadata')    
    EXPERIMENT_NAME = hologram_metadata.experiment
    EXPERIMENT_DIR = os.path.join(RESULT_DIR, EXPERIMENT_NAME)
    RECONSTRUCTION_DIR = os.path.join(EXPERIMENT_DIR,
                                        'reconstructed_hologram')
    SEGMENTED_IMAGES_DIR = os.path.join(EXPERIMENT_DIR,
                                        'segmented_images')
    GENERAL_RESULTS_DIR = os.path.join(RECONSTRUCTION_DIR, 'general_results')
    
    image_name = request.form.get('filename')
    print(image_name)
    
    image = io.imread("app/"+image_name, as_gray=True)
    #image = image[:,:,1]

    # apply threshold
    thresh = threshold_otsu(image)
    

    image = image < thresh
    #image = image < thresh[0]

    bw = closing(image, square(16))

    # remove artifacts connected to image border
    cleared = clear_border(bw)

    # label image regions
    label_image = label(cleared)
    # to make the background transparent, pass the value of `bg_label`,
    # and leave `bg_color` as `None` and `kind` as `overlay`
    image_label_overlay = label2rgb(label_image, image=image, bg_label=128, bg_color=None, kind='overlay')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(image_label_overlay)
    id = 0

    for region in regionprops(label_image):
        # take regions with large enough areas
        if region.area >= 200:
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            image_cropped = image[minr:maxr, minc:maxc]
            f_name = SEGMENTED_IMAGES_DIR + '/img_' + str(id) + '.jpeg'
            io.imsave(f_name, image_cropped)
            id += 1
            

    ax.set_axis_off()
    plt.tight_layout()
    
    
    
    segmentation_name = 'segmented_' + str(random.random()) + '.png'
    filename = '/results/' + hologram_metadata.experiment + '/reconstructed_hologram/general_results/' + segmentation_name
    
    plt.savefig(GENERAL_RESULTS_DIR + '/' + segmentation_name,
                    bbox_inches='tight',
                    transparent=True,
                    pad_inches=0)
    
    return jsonify({'result': 'success', 'image' : filename})
