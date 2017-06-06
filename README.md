# Overview
This repository is intended to contain a number of utilities
that can be used to interact with data collected by the PerkinElmer
Solaris imaging system. Very limited testing has been done to verify
functionality.

# Requirements
## Python 3
Verify you are using Python 3
In the terminal, type:
>$ python3 --version

### Installing Python3
Digiital Ocean has a few nice write-ups of how to install Python 3 on different operating systems:
https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3

It is best to use a virtual environment to install the dependecies.

## Using Virtual Environments
Activate your Python 3 virtual environment
>$ source ~/.virtualenvs/notebook/bin/activate

where ~/.virtualenvs/notebook is the location of your virtual environment

## Python Packages
>(notebook)$ pip3 install numpy

>(notebook)$ pip3 install scikit-image


## Jupyter
>(notebook)$ pip3 install jupyter

>(notebook)$ jupyter notebook --generate-config

Modify config in your favorite text editor i.e.:
>$ vim ~/.jupyter/jupyter_notebook_config.py 

Change the following lines:
>c.NotebookApp.open_browser = True

>c.NotebookApp.enable_mathjax = True

>c.NotebookApp.notebook_dir = '/hour/home/directory/Notebooks'

clone the current reposity into you notebook directory:
>$ git clone https://github.com/ethanlarochelle/solaris-tools.git

Start Jupyter:
>(notebook)$ jupyter notebook

# Notebooks
## Solaris Batch Export
This is a iPython (Jupyter) notebook written to batch convert data into
image files that can be analyzed using third-party software. 
It was written using Python 3.4

### Edit cell with input and output directories
Then run each cell sequentially. Depending on whether the user supplied group information will dictate whether you use the "Group" or "No Group" code block to process the images

# Future tools
Other scripts to analyze video content have also been developed. As 
these and future tools are tested for minimum functionality they will 
be added to this repository. 
