---
sort: 2
---
# Get Started

The web application was developed through [Flask Framework]() and can run locally. 

## Environment 
First, we really recommend to create a environment to protect other projects and to install the correct library versions. To do so, install the venv package using pip

    python3 -m pip install --user virtualenv

Once the virtualenv is installed, create a virtual environment

    python3 -m venv /path/to/new/virtual/environment

Clone this repository

    git clone https://github.com/andouglasjr/HSapplication/

Finally, go to the correct folder and activate the environment

    cd /path/to/new/virtual/environment
    source bin/activate

    

## Requirements
In the requirements.txt files you will find all the libraries with their respects versions to make the application work properly. First update your pip

    pip install --upgrade pip

Then, run the follow command

    pip install -r requirements.txt

```tip
If you will not use the classification step, comment the torch library line in the requirements file for speed up the installation.
```

## Install Holopy Modified

The reconstruction step is performed using the [Holopy Library]() with some changes to work on in a web environment. To install this library, enter in **holopy** folder and run the follow command

    python setup.py develop

### To MAC users

If some error occurred in the command above, likely is missing **gfortran** compiler. We recommend to use **brew** package manager as follow

    brew install gfortran

## Running Flask Server
Once the requirements have been installed, go to the root directory and run

    python run.py

It will be shown the local ip to access the server in web browser.

```danger
This server is running over https protocol. By missing the certificate, the browser will show a warning message about this. Go to advance and not secure connection.
```

## Some considerations
1. The reconstruction step uses a modified version of Holopy. This modification is the separation of the propagation method in order to use the spatial filtering. Please, use the holopy available in the git repository available in this application.
2. The machine learning models supported by the application are Resnet, Densenet, SENet and EfficientNet. If you will use another kind of network, please install the equivalent library to the environment.