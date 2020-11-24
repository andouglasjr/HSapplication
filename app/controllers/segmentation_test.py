from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as colo

import holopy as hp
from holopy.core.io import get_example_data_path, load_average
from holopy.core.process import bg_correct

image = io.imread('../static/saved_holograms/test_img_out.bmp')
fig = plt.figure()
plt.imshow(image)


def image_show(image, nrows=1, ncols=1, cmap='gray'):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 14))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    return fig, ax


def circle_points(resolution, center, radius):
    radians = np.linspace(0, 2 * np.pi, resolution)
    c = center[1] + radius * np.cos(radians)  #polar co-ordinates
    r = center[0] + radius * np.sin(radians)

    return np.array([c, r]).T

imagepath = get_example_data_path('image01.jpg')
raw_holo = hp.load_image(imagepath, spacing = 0.0851, medium_index = 1.33, illum_wavelen = 0.66, )
bgpath = get_example_data_path(['bg01.jpg','bg02.jpg','bg03.jpg'])
bg = load_average(bgpath, refimg = raw_holo)
holo = bg_correct(raw_holo, bg)

zstack = np.linspace(0, 20, 11)
rec_vol = hp.propagate(holo, zstack)
hp.show(rec_vol)


image = np.abs(rec_vol.data[1])

points = circle_points(200, [96, 101], 30)[:-1]
fig, ax = image_show(image)
ax.plot(points[:, 0], points[:, 1], '--r', lw=3)

snake = seg.active_contour(image, points, alpha=0.06, beta=0.3)

fig, ax = image_show(image)
ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
plt.show()