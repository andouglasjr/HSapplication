from app import app
from flask import Response, jsonify, render_template, request

import os
from os import listdir
from os.path import isfile, join
import random

import torch
import torch.nn as nn
from torchvision import transforms

from efficientnet_pytorch import EfficientNet
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import app.controllers.voting_classifier as vs
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image


@app.route('/holo_classification')
def holo_classification():
    dir_path = os.path.dirname(os.path.dirname(__file__))
    path_directory = dir_path + '/static/ml_models'
    models = [
        f for f in listdir(path_directory) if isfile(join(path_directory, f))
    ]
    
    path_directory = dir_path + '/static/reconstructed_images'
    images = [
        f for f in listdir(path_directory) if isfile(join(path_directory, f))
    ]
    
    return render_template('hologram_classification_boost.html', models=models, images=images)


@app.route('/classify', methods=['POST', 'GET'])
def classify():
    models_names = request.form.getlist('model_name[]')
    images_names = request.form.getlist('image_name[]')
    print(models_names)
    cm_name = None

    dir_path = os.path.dirname(os.path.dirname(__file__))

    image_path_directory = dir_path + '/static/reconstructed_images/'
    model_path_directory = dir_path + '/static/ml_models/'
    
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    img_input = torch.Tensor()
    labels = []
    
    for img_name in images_names:
        image = Image.open(image_path_directory + img_name).convert('RGB')
        for i in range(1,50):
            cla_im = "Im"+str(i)+"_"
            cla_phase = "Phase"+str(i)+"_"
            if(cla_im in img_name) or (cla_phase in img_name):
                labels.append(i)
                break
        transform = transforms.Compose([
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ])
        image_test = transforms.CenterCrop(224)(image)
        image_test = transforms.ToTensor()(image_test)
        image_test = transforms.Normalize(mean, std)(image_test)
        
        #image_test = torch.from_numpy(np.asarray(image))
        img_input = torch.cat((img_input, torch.unsqueeze(image_test, 0)), dim=0)
        #image_test = image_test.permute(0, 3, 1, 2)
    
    top_predict_values_list = []
    top_predict_indices_list = []
    estimators = []
    for model_name in models_names:
        model = torch.load(model_path_directory + model_name, map_location='cpu').module
        estimators.append(model)
    
    ensemble = vs.VotingClassifier(estimators)
    
    final_predict, predict, pred= ensemble.predict(img_input)
    pred = nn.Softmax()(torch.Tensor(pred))
    labels_plot = np.unique(labels)
    if(img_input.shape[0]>1):
        cm = confusion_matrix(final_predict, labels, labels_plot)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = labels_plot)
        disp = disp.plot(cmap='Blues')
        
        cm_name = 'cm_' + str(random.random()) + '.png'
        plt.savefig('app/static/results/'+cm_name)    
    
    top_predict_values, top_predict_indices = torch.topk(pred, 5)      
     
    top_predict_values = top_predict_values.detach().numpy()
    top_predict_indices = top_predict_indices.detach().numpy()
    top_predict_indices_list.append(top_predict_indices.tolist())
    top_predict_values_list.append(top_predict_values.tolist())
        
    if len(top_predict_indices_list)>2:
        print('')
        
    return jsonify({
        'sucess': 'sucess',
        'values': top_predict_values.tolist(),
        'indices': top_predict_indices.tolist(),
        'cm_image': cm_name,
    })


def list_models_folder():
    dir_path = os.path.dirname(os.path.dirname(__file__))
    path_directory = dir_path + '/static/ml_models'
    print(path_directory)
    images = [
        f for f in listdir(path_directory) if isfile(join(path_directory, f))
    ]
    return images


@app.route('/upload_model', methods=['POST', 'GET'])
def upload_model():
    if request.method == 'POST':
        print(request.files)
        if 'model' not in request.files:
            return 'there is no upload_image in form!'

        dir_path = os.path.dirname(os.path.dirname(__file__))
        path_directory = dir_path + '/static/ml_models'
        upload_image = request.files['model']
        path = os.path.join(path_directory, upload_image.filename)
        upload_image.save(path)

        return jsonify({
            'result': 'sucess',
            'images_folder': list_models_folder()
        })
