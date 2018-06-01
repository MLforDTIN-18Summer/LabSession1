## Installation steps
### 1. Linux (Ubuntu)
- **Clone the git repository**
	```git clone https://github.com/MLforDTIN-18Summer/LabSession1.git```
- **Install python3.6**
	```sudo apt-get install python3.6```
- **Pip install virtual env**
	```pip install virtualenv```
- **Create virtual env and activate it**
	```virtualenv venv -p python3.6 && source venv/bin/activate```
- **Install python dependencies**
	```pip install -r requirements.txt```
- **Installing pyqt4**
	1. Download sip and pyqt4
		- Make a tmp directory
			```mkdir tmp && cd tmp```
		- ```wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.8/sip-4.19.8.tar.gz```
		- ```wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12.1/PyQt4_gpl_x11-4.12.1.tar.gz```
	2. Extract source from downloaded zip files
		- ```tar -xvf PyQt4_gpl_x11-4.12.1.tar.gz```
		- ```tar -xvf sip-4.19.8.tar.gz```
		- ```rm -rf ./*gz```
	3. Build and install sip
		- ```cd sip-4.19.8/```
		- ```python configure.py```
		- ```make```
		- ```sudo make install```
	4. Build and install pyqt4
		- ```cd ../PyQt4_gpl_x11-4.12.1/```
		- ```python configure.py```
		- ```make```
		- ```sudo make install```
	5. Check the installation
		- ```import PyQt4```
	6. Run the python qt application
		- ```cd ../../qt_gui/```
		- ```python final_scratch_pad.py```

### 2. OSx
- **Clone the git repository**
	```git clone https://github.com/MLforDTIN-18Summer/LabSession1.git```
- **Install python3.6**
	```brew install python3.6```
- **Pip install virtual env**
	```pip install virtualenv```
- **Create virtual env and activate it**
	```virtualenv venv -p python3.6 && source venv/bin/activate```
- **Install python dependencies**
	```pip install -r requirements.txt```
- **Installing pyqt4**
	1. Download sip and pyqt4
		- Make a tmp directory
			```mkdir tmp && cd tmp```
		- ```wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.8/sip-4.19.8.tar.gz```
		- ```wget http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12.1/PyQt4_gpl_mac-4.12.1.tar.gz```
	2. Extract source from downloaded zip files
		- ```tar -xvf PyQt4_gpl_x11-4.12.1.tar.gz```
		- ```tar -xvf sip-4.19.8.tar.gz```
		- ```rm -rf ./*gz```
	3. Build and install sip
		- ```cd sip-4.19.8/```
		- ```python configure.py```
		- ```make```
		- ```sudo make install```
	4. Build and install pyqt4
		- ```cd ../PyQt4_gpl_x11-4.12.1/```
		- ```python configure.py```
		- ```make```
		- ```sudo make install```
	5. Check the installation
		- ```import PyQt4```
	6. Run the python qt application
		- ```cd ../../qt_gui/```
		- ```python final_scratch_pad.py```

### 3. Windows
- **Install python3.6**
	```sudo apt-get install python3.6```
- **Pip install virtual env**
	```pip install virtualenv```
Steps:	
	1. Install Python 3.6 => https://www.python.org/downloads/release/python-365/
	2. Create a new virtual environment => python3 -m venv /path/to/new/virtual/environment
	3. Activate the environment => C:\><venv>\Scripts\activate.bat
	4. Install Sip => pip3 install SIP
	5. Download PyQt4 package => https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4 and Install it C:\path\where\wheel\is\> pip install PyQt4-4.11.4-cp35-none-win_amd64.whl
	6. Install all the dependencies: Numpy, Scipy, OpenCV, Scikit-learn, MatplotLib
		=> pip3 install opencv-python
		=> pip3 install scipy
		=> pip3 install -U scikit-learn
		=> python3 -mpip install matplotlib
	7. Run the program!
