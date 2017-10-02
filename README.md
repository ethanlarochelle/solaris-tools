# Overview
This repository is intended to contain a number of utilities
that can be used to interact with data collected by the PerkinElmer
Solaris imaging system. Very limited testing has been done to verify
functionality.

# Notebook
Contains an iPython (Jupyter) notebook written to batch convert data into
image files that can be analyzed using third-party software. 

# CLI
Command line interface for batch exporting Solaris experiment data. This tool can be called from a .bat file on the Solaris to export whole experiment directories to 16-bit TIF images.

# Future tools
Other scripts to analyze video content have also been developed. As 
these and future tools are tested for minimum functionality they will 
be added to this repository. 

# Requirements
Very limited testing has been done to verify functionality on MacOS. Additional testing using Windows 7 as well as more detailed documentation has been provided by Sakib Elahi.

## MacOS (or Linux)
### Python 3
Verify you are using Python 3

In the terminal, type:
>$ python3 --version

#### Installing Python3
Digiital Ocean has a few nice write-ups of how to install Python 3 on different operating systems:
https://www.digitalocean.com/community/tutorial_series/how-to-install-and-set-up-a-local-programming-environment-for-python-3

It is best to use a virtual environment to install the dependecies.

### Using Virtual Environments
Activate your Python 3 virtual environment
>$ source ~/.virtualenvs/notebook/bin/activate

where ~/.virtualenvs/notebook is the location of your virtual environment

### Python Packages
>(notebook)$ pip3 install numpy

>(notebook)$ pip3 install scikit-image


### Jupyter
>(notebook)$ pip3 install jupyter

>(notebook)$ jupyter notebook --generate-config

Modify config in your favorite text editor i.e.:
>$ vim ~/.jupyter/jupyter_notebook_config.py 

Change the following lines:
>c.NotebookApp.open_browser = True

>c.NotebookApp.enable_mathjax = True

>c.NotebookApp.notebook_dir = '/your/home/directory/Notebooks'

clone the current reposity into you notebook directory:
>$ git clone https://github.com/ethanlarochelle/solaris-tools.git

Start Jupyter:
>(notebook)$ jupyter notebook

## Windows
* Obtained administrator privileges to desktop computer
* Open PowerShell as administrator
  * Verify by folowing instrucions at this link: https://superuser.com/questions/749243/detect-if-powershell-is-running-as-administrator
* Change active directory
* Change permission to allow accepting and running downloaded scripts, if not already set
  * Ensure that ExecutionPolicy of CurrentUser is "RemoteSigned"
    * `Get-ExecutionPolicy -List`
  * If not RemoteSigned, change it:
    * `Set-ExecutionPolicy -Scope CurrentUser`
    * Enter `RemoteSigned` when prompted
    * Confirm Y when prompted
    * Verify that it changed using `Get-ExecutionPolicy -List`
* Install the Package Manager "Chocolatey"
  * [Chocolatey](https://chocolatey.org/install) allows to install applications and tools off the Internet, like Python and the Nano text editor
  * Create WebClient object `$script` to share Internet connection settings with Internet Explorer
    * `$script = New-Object Net.WebClient`
  * Return all available members of this object:
    * `$script | Get-Member`
  * Download and display the install file. (Good practice to inspect script before running.)  The method from the list we need is DownloadString
    * `$script.DownloadString("https://chocolatey.org/install.ps1")`
  * Install Chocolatey
    * iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    * The [digitalocean.com](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10) instructions are for Windows 10 which uses a newer version of PowerShell. Got this line from the Chocolatey website instructions for installing on Windows 7: https://chocolatey.org/install#install-with-powershellexe
    *  Close and reopen PowerShell, in accordance with warning given by installation script, since .NET Framework needed to be automatically upgraded for this installation.
  *  Verifying that Chocolatey is installed
    * After reopening PowerShell and changing directory again, type `choco -?` to list all available commands.  This should run if Chocolatey is properly installed.
* Install the text editor Nano.
  * Nano is a command-line driven text editor that is often used to write Python scripts
  * Use Chocolatey to install Nano:
    * `choco install -y nano`
      * The -y flag confirms automatically to run the script without being prompted
* Install Python 3 using Chocolatey
  * `choco install -y python3`
  * upgrade pip software package manager for Python:
    * `python -m pip install --upgrade pip`
      * If this fails due to SSL issue, one work-around is posted at on [StackOverflow](https://stackoverflow.com/questions/25981703/pip-install-fails-with-connection-error-ssl-certificate-verify-failed-certi)
### Installing and Using Virtual Environments
* Set up virtual environment
  * Creates an isolated directory on computer for Python projects. This is best practice to ensure that each project has its own set of dependencies that won't disrupt other projects.
  * Type `mkdir Environments` to create a folder called Environments current folder
  * Type `cd Environments` to make this new folder we just created the current directory.
  * Type `Python -m venv notebook` to create the virtual environment called notebook under the Environments directory (you could call it whatever you want).
    * Type `ls notebook` to view the contents of this folder. You can also navigate to it using Windows Explorer to verify everything is working so far. Should have 3 folders in the virtual environment: Include, Lib, and Scripts and a pyvenv CFG file.
  *  Activate the virtual environment by typing `notebook\Scripts\activate`
    *  Prompt will now be prefixed with the name of the environment
### Verify Installation
* Test that everything's working by creating "Hello, World!" program
  * Open Nano and create new file: `nano hello.py`
  * Type `print("Hello, World!")`
  * Exit Nano and save the file: `Ctrl+x, y, enter` when prompted
  * Run the program by typing `python hello.py`
  * Terminal should output `Hello, World!` if everything's working.
  * To get out of the virtual environment, type `deactivate`
* Success!  Python3 is installed and working properly.  Now install the Python packages needed to run the notebooks.
  *  Get back in the virtual environment: `notebook\Scripts\activate`
### Python Packages
#### numpy
* See this site for a notes on downloading and installing NumPy on Python 3 for Windows: https://solarianprogrammer.com/2017/02/25/install-numpy-scipy-matplotlib-python-3-windows/
  * Make sure it is 64bit version
  * An additional helpful link: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
  * Download the .whl file and move to the Environments directory (one level up from notebook).
  *  Back in PowerShell, which should still be in the notebook virtual environment with active directory Environments (where the .whl file is located), type: `pip install numpy-1.11.3+mkl-cp36-cp36m-win_amd64.whl` (or name of latest .whl file)
#### scikit-image
* Useful link: http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-image
* Download the 64-bit version *_win_amd64.whl to the Environments folder
* Back in PowerShell, type: `pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org scikit_image-0.13.0-cp36-cp36m-win_amd64.whl` (or name of latest .whl file)
  * The --index-url flag is necessary again because the first time when I ran it without it, I got that same SSL certificate error.  Apparently this .whl file needed to go to that site to download other packages. 
#### scipy
* Useful link: http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
* Download the 64-bit version *_win_amd64.whl to the Environments folder
* Back in PowerShell, type: `pip install scipy-0.19.1-cp36-cp36m-win_amd64.whl` (or name of latest .whl file)
#### jupyter
* Type `pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org jupyter`
  * PowerShell automatically downloads and installs many  (~33) packages.
  * Type `jupyter notebook --generate-config`
  * That created a config file in the folder `C:\$HOME\.jupyter` called jupyter_notebook_config.py
  * Use Nano, the text editor we installed earlier, to open and edit the config file:
    * Type `nano C:\$HOME\.jupyter\jupyter_notebook_config.py`, where $HOME is the current user's directory
    * Change the following lines:
      >c.NotebookApp.open_browser = True

      >c.NotebookApp.enable_mathjax = True

      >c.NotebookApp.notebook_dir = '/your/home/directory/Notebooks'

 #### Git
* Get out of the virtual environment by typing `deactivate`,
  * Use Chocolatey to install Git by typing `choco install -y git`
    * If this fails, try downloading and installing: 
      * Download git setup file from git-scm website: https://git-scm.com/downloads
  * If this continues to fail, download the repository as a zip and unzip in the Notebooks directory

 ### Start Jupyter 
 * Start jupyter to browse and edit scripts
   * In the virtual environment, type: `jupyter notebook`
      * Web browser should open in the Notebooks directory
 #### Stopping Jupyter
 * Click the interrupt kernel button (looks like a stop button).
* Close the script tab in Chrome.
* On the jupyter notebook tab in Chrome, click the "Running" button.
* Click shutdown next to the running scripts.
* Close that browser tab too.
* Back in PowerShell, type Ctrl+C to exit jupyter.

 ### Windows Quirks
 * Use double backslashes ("\\") rather than single in the input and output directory lines to force it to read as strings
   * Do not use a closing slash









