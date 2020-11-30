---
sort: 2
---

# Processing

Once the image was acquired, it can be processed by applying some transformations to delete some undesirable areas, change the size, apply bright and contrast masks, and crop the image that will be reconstructed. This step can be skipped if the acquired image is already right to be reconstructed. Generally, saved data in mat files can be directly reconstructed, without necessarily making changes to the image.

<p align="center">
<img src="{{site.baseurl}}/images/processing_screen.png" width=900>
</p>

All this step is made directly in the browser, using the [API Konva.js](https://konvajs.org/). This API is a powerful tool to work with images in web applications, due to facilities to manipulate them. It's possible to apply different kinds of transformations, masks, events, animations, and others, with an object-oriented Javascript API.