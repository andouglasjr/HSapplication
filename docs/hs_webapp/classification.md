---
sort: 5
---

# Classification

Finally, in the classification step is possible to choose the models and images that will be used to make the classification. The selected options made by the user are sent to the server that used the trained models contained in ML_models folder to perform the classification.

If more than one model is selected, so the system uses an ensemble learning technique to make the classification and return the probabilities vector (the softmax output) to be shown in the application.

As the training as the test was made using PyTorch framework. This framework was developed to be used in the machine learning approach, having several APIs that make easier the development of this kind of application. 

To exemplify, it was performed a diatoms classification task. The screenshot shown below is this application. The models used were EfficientNet_B0, EfficientNet_B1 and SEResnet50. The selected image and the classification results are also indicated in the figure.

<p align="center">
<img src="{{site.baseurl}}/images/classification_screen.png" width=900>
</p>

