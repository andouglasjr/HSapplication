---
sort: 2
---
# Get Started

The web application was developed through [Flask Framework]() and can run locally. 

## Environment 
First, we really recommend to create a environment to protect other projects and to install the correct library versions. To do so, install the venv package using pip

    python3 -m pip install --user virtualenv

## Requirements
In the requirements.txt files you will find all the libraries with their respects versions to make the application work properly. Run the follow command

    pip install -r requirements.txt

## Running Flask Server
Once the requirements have been installed, go to the root directory and run

    python run.py

It will be shown the local ip to access the server in web browser.

## Some considerations
1. The reconstruction step uses a modified version of Holopy. This modification is the separation of the propagation method in order to use the spatial filtering. Please, use the holopy available in the git repository available in this application.
2. The machine learning models supported by the application are Resnet, Densenet, SENet and EfficientNet. If you will use another kind of network, please install the equivalent library to the environment.