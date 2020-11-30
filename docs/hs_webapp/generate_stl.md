---
sort: 6
---

# Generate STL File

One interesting function of the web application is to generate a 3D microscope stl file that can be printed and used in a specific application. Once the system setup was made and the reconstruction step works, the distances between grating and lens, and lens and camera, can be used in that specific configuration to that samples that were tested before. In this case, passing these parameters, the HS-WebApp generates automatically the 3D device in the STL_Files folder.

<p align="center">
<img src="{{site.baseurl}}/images/generation_stl_screen.png" width=900>
</p>

The 3D microscope is based on the work of Teresa Cacace published [here](https://www.osapublishing.org/boe/fulltext.cfm?uri=boe-11-5-2511&id=430110).The generated file is a STL file as shown in the figure below.

<p align="center">
<img src="{{site.baseurl}}/images/microscope.png" width=160>
<img src="{{site.baseurl}}/images/microscope_1.png" width=200>
</p>