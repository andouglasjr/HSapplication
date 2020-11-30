---
sort: 3
---

# Reconstruction

The most important point of the web application is the reconstruction. In this step, the wavelength, pixel size, and the interval of distances in which the propagation must be carried out are requested by the application and saved in the hologram metadata. 

<p align="center">
<img src="{{site.baseurl}}/images/reconstruction_screen.png" width=900>
</p>

At this point, the user can choose if wants to realize the spatial filter manually, only defining the region of the real image in Fourier space, or performs the reconstruction without this step. This is important because applications with in-line setup use other algorithms to perform this filter. If the user wants to apply a spatial filter, a modal page is open and a crop in the frequency space can be made using [Konva.js API](https://konvajs.org/).

The reconstruction is made using a library developed by Manoharan Lab, Harvard University called [HoloPy](https://holopy.readthedocs.io/en/master/). This library is a python based tool for working with digital holograms and light scattering. It is important to notice that to work properly in a web application same changes have been made directly in the API. Besides that, the spatial filter and autofocus algorithm were implemented since this API has not these implementations. Therefore, **it is important to use the Holopy versions available on the application GitHub, in order to make the system work properly.**

This step can take while depending on the hologram image size and the number of planes that will be applied to the propagation. Once the reconstruction is completed and the autofocus finds the best distance Z, the intensity and phase are shown in the browser.