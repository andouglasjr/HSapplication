---
sort: 1
---
# Holographic System for Machine Learning Approaches (HolSys-ML)

The HolSys-ML is a complete holographic system developed by [Natalnet Laboratory Network](http://www.natalnet.br) (Brazil) and [Institute of Applied Sciences and Intelligent Systems - ISASI](https://www.isasi.cnr.it/) (Italy) to identify and classify microparticles in water samples. The system was designed to be used by scientists and researches in order to make easier the studies of particles using holography techniques and deep learning trained models. In this page is detailed all the steps to build a HolSys and it is available the Web Application developed to work with the system to perform all need steps to reconstruct the hologram and classify it using ML. 

## HolSys Hardware

The holographic system is composed by optical and structural components that have been designed to make the setup easier for different sort of applications. All the documentation to clone the HolSys is detailed [here]().

## HSWebApp

The HSWebApp was developed to be used with the HolSys but can be used for any holographic device that acquire the hologram using a digital camera. This application is able to make the follow steps:

1. **Acquisition**: The device camera plugged in the computer is accessed directly by the browser and the hologram can be acquired and uploaded to the server. It is also possible to use acquired holograms saved in the "/saved_holograms" folder. In this case, .png, .jpeg, and .bmp images and .mat file are supported.
2. **Processing**: In this step is possible to apply some image filters, like bright and contrast, to improve the fringes partners. 
3. **Reconstruction**: Once the hologram was acquired and processed, it is possible to make its reconstruction with pixel size, wavelength and plane Z range parameters. Besides that, to off-axis setup, a manual spatial filter can be applied to isolate only the real image for the reconstruction. The reconstruction step realizes the propagation (using the HoloPy library modified) and the autofocusing using Tamura Coefficient technique and return the intensity and phase of the reconstructed hologram. 
4. **Segmentation:** Depending on how the samples is disposed in the image, it is necessary to perform the separation to be inserting on the machine learning model. This is performed using Otsu algorithm and image fill.
5. **Machine Learning**: In this last step, the user can upload some ML models and use it to classify the test samples for their application. More than one model can be used in a ensemble model approach.

The web application codes are available on [github](). To use this code access the [Get Started]() section and to know more about the application access [HSWebApp Doc]().

## Credits and Citation

Please, visit the [Credits and Citation]() page to see how to credit this system and how to help to improve it.

## License

The theme is available as open source under the terms of the MIT License.


## site.pages

<!-- prettier-ignore-start -->

| source          | link                                                           |
| --------------- | -------------------------------------------------------------- |
{% for page in site.pages -%}
| {{ page.path }} | [{{ page.url | relative_url }}]({{ page.url | relative_url }}) |
{% endfor %}

<!-- prettier-ignore-end -->

## Documents

https://jekyll-rtd-theme.rundocs.io

## Local debug

```sh
gem install jekyll bundler

bundle install

JEKYLL_GITHUB_TOKEN=blank PAGES_API_URL=http://0.0.0.0 bundle exec jekyll server --livereload
```

## The license

The theme is available as open source under the terms of the MIT License
