---
sort: 7
---

# Structural Dimensions Computation

Another functionality of the HSWebApp is a tool to compute the structural dimensions, grating-lens distance (dgl) and lens-camera distance (dlc), based on the optical components specification. To carry out this computation are necessary basically six main values:

1. Wavelength of the source light;
2. Pixel size of the camera;
3. Number os pixels used to sample in the hologram acquisition;
4. Grating period;
5. Grating size;
6. Lens focus.

Besides that, to make the computation more precise, some information about the microchannel chip are required, like chip and channel size, and the coverlid. The results are

1. Beta angle (related to the grating diffracted beam);
2. Magnification of the object after the lens plane;
3. Dgl - Grating-Lens distance;
4. Dlc - Lens-Camera distance;
5. Dt - total distance that is given by Dgl + Dlc;

<p align="center">
<img src="{{site.baseurl}}/images/structural_dimensions_screenshot.png" width=900>
</p>