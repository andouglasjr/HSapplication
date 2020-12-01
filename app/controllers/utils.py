import os
import matplotlib.pyplot as plt
import random
import numpy as np
import cv2
from app import app
plt.switch_backend('Agg')

#Directories
STATIC_DIRECTORY = app.static_folder
RESULTS_DIRECTORY = os.path.join(STATIC_DIRECTORY, "results")


def generate_experiment_tree_directory(experiment_name):
    EXPERIMENT_NAME_DIRECTORY = os.path.join(RESULTS_DIRECTORY,
                                             experiment_name)
    if not os.path.isdir(EXPERIMENT_NAME_DIRECTORY):
        #Create Experiment Directory
        os.mkdir(EXPERIMENT_NAME_DIRECTORY)
        #Create hologram, processed_hologram, reconstructed_hologram, stl_files, segmented_images, classification_results Folders
        folder_names = [
            'hologram', 'processed_hologram', 'reconstructed_hologram',
            'stl_files', 'segmented_images', 'classification_results', 'reconstructed_hologram/general_results'
        ]
        for name in folder_names:
            os.mkdir(os.path.join(EXPERIMENT_NAME_DIRECTORY, name))
        print('Directory Tree Generated.')
    return EXPERIMENT_NAME_DIRECTORY


def save_image_with_plt(imshow_arg, path):
    plt.ioff()
    fig = plt.figure()
    plt.imshow(imshow_arg, cmap='gray')
    plt.axis('off')
    fig.tight_layout()
    rand_number = random.random()
    plt.savefig(path, bbox_inches='tight', transparent=False, pad_inches=0)


def autofocusing(r):
    tc = []
    media_ = []
    std_ = []
    for i in range(r.data.shape[0]):
        U = r[i].data
        value = np.abs(U)
        media = np.mean(value)
        std = np.std(value)
        tamura = std / media
        tc.append(tamura)
    rho = (tc[1] - tc[0])/np.abs(tc[1] - tc[0])
    rho = np.array(rho)
    tc = np.array(tc)
    tc = tc*rho
    best_focus = np.where(tc == np.max(np.max(tc)))
    best_focus = np.squeeze(best_focus)
    return best_focus


def save_images(r, fft, path_directory):
    fig = plt.figure()
    plt.imshow(np.log(np.abs(fft[0])), cmap='gray')
    plt.axis('off')
    fig.tight_layout()
    rand_number = random.random()
    plt.savefig(path_directory + '/general_results/fft' + str(rand_number) + '.png',
                bbox_inches='tight',
                transparent=False,
                pad_inches=0)

    best_focus = autofocusing(r)

    fig = plt.figure()
    plt.imshow(np.abs(r[best_focus].data[:, :]), cmap='gray')
    plt.axis('off')
    fig.tight_layout()
    rand_number = random.random()
    plt.savefig(path_directory + '/reconstructed_amplitude' +
                str(rand_number) + '.png',
                bbox_inches='tight',
                transparent=False,
                pad_inches=0)
    amp_img = 'reconstructed_amplitude' + str(rand_number) + '.png'

    fig = plt.figure()
    plt.imshow(np.angle(r[best_focus].data[:, :]), cmap='gray')
    plt.axis('off')
    fig.tight_layout()
    rand_number = random.random()
    plt.savefig(path_directory + '/reconstructed_phase' + str(rand_number) +
                '.png',
                bbox_inches='tight',
                transparent=False,
                pad_inches=0)
    phase_img = 'reconstructed_phase' + str(rand_number) + '.png'

    return amp_img, phase_img

def check_available_cameras():
    # detect all connected webcams
    valid_cams = []
    for i in range(2):
        cap = cv2.VideoCapture(i)
        if cap is (not None) or cap.isOpened():
            valid_cams.append(i)
        cap.release()

    return valid_cams
