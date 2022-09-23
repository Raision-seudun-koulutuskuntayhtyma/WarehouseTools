# WarehouseTools
This repository contains tools for Raseko lending application. With those tools you can create and print student cards and product catalog pages.

From the repository you can find Python source files, documentation and installers for the tool set. Most important files are in the following table:

| File name | Purpose |
|---|---|
productPicture.py | Source code for creating product catalog pages
productPicture.ui | Qt Designer file for the UI of catalog page tool
productPictureSettings.dat | JSON based settings file for product catalog application. Used for camera and folder settings.
productPicture.spec | Build settings for the product catalog tool
studentCardv2.py | Source code for creating student cards
studentCardv2.ui | Qt Designer file for student card tool
studentCardv2.spec | Build settings for student card tool
studentPicture.py | Source code for webcamera tool which takes still pictures for the student card
studentPicture.ui | Qt Designer file for the webcamera tool
studentPictureSettings.dat |  JSON based settings file for student photo application. Used for camera and folder settings.
studentPicture.spec | Build settings for student photo taking tool
code128Bcode | Module for generating barcodes with the Libre barcode 128 font
Omakuva2.png | A placeholder image for the student card tool
Raseko-logo-vaaka.png | RASEKO's logo for the student card

## Product Catalog Tool

This tool is for creating quarter of the product catalog page. Every page consist of 4 rectangels showing a product picture, name of the product and the barcode. Tools saves this information into a pdf file. Catalog pages are created with Inkscape application and printed for a catalog stand. This tool is intended to be used with camera stand designed by TeSu students. UI has rule of thrirds view finder to get correctly sized and positioned product pictures. Pictures are rotated 90 degrees clock wise for final catalog page. When the picture is perfect it can be printed to a pdf file. These files are merged into catalog pages with Inkscape drawing application.

Tool is multithreaded application. Video processing is done in a separate thread to avoid frozen UI while reading the video stream from a webcam. Threads are created with `QThread` class from **PyQt5**.

![image](https://user-images.githubusercontent.com/24242044/170026343-726bc5d4-f182-451d-9f8d-a704fc72058b.png)

> There is a new check box for sharpening the image. It has been added to the UI below video buttons. Missing from the picture above.

This is what a catalog page looks like:

![33666](https://user-images.githubusercontent.com/24242044/170033080-1586f793-a23f-4b9d-8ae5-1684fd411eba.jpg)


## Student Card Tool

This tools allows printing student cards using photos taken with student photo tool.

![image](https://user-images.githubusercontent.com/24242044/170027259-51607205-f17e-4fa5-9b48-db46a2a03762.png)

## Student Photo tool

This is a simple tool for taking student photographs with a webcam. The UI has same settings component as Product Catalog Tool, but it has not been implemented yet.

Tool is multithreaded application. Video processing is done in a separate thread to avoid frozen UI while reading the video stream from a webcam. Threads are created with `QThrad` class from **PyQt5**.

![image](https://user-images.githubusercontent.com/24242044/170027658-5979a2aa-4a61-4b5c-af62-13f972f7862c.png)

## Dependencies

Tools UIs has been made with **QT Designer** so **PyQT5** is needed. You can install it by typing `pip install pyqt5`. Webcam uses **OpenCV** library for imagecapture. For Pyhton environment it can be installed by typing `pip install opencv-python`.

:warning: Keep pip up to date, because some libraries use latest versions of **pip**. Update it with following command `pip install --upgrade pip` before installing dependencies.

Barcode font **Libre Barcode 128** must be installed to operating system for showning barcodes in student cards and product catalog pages. Font can be downloaded from https://fonts.google.com/specimen/Libre+Barcode+128+Text 

### Student Photo Tool dependents

The app needs following files: 
* `studentPictureSettings.dat` camera and folder parameters
* `studentPicture.ui` UI definitions

Libraries and modules needed:

```Python
# LIBRARIES AND MODULES
import json # For saving and reading settings in JSON format
import cv2 # For OpenCV video and picture manipulation for reading Web camera
import sys # For accessing system parameters
import os # For file paht handling
from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt, QRect # For image scaling and cropping
from PyQt5.QtGui import QImage, QPixmap, QTransform # For image handling
```

### Student Card Tool dependents

App needs only the UI file `studentCardv2.ui`.

Libraries and modules needed:

```Python
# LIBRARIES AND MODULES
import sys # For accessing system parameters
import os # For directory and file handling
from PyQt5 import QtWidgets, uic , QtPrintSupport # For the UI and printing
from PyQt5.QtGui import QPixmap, QTransform, QPainter # For image handling

```

### Product Picture Tool
The app needs the following files:

* `productPictureSettings.dat` camera and folder parameters
* `productPicture.uit` UI definitions
* `code128Bcode.py` module for calculating barcode values

Libraries and modules needed:

```Python
import json # For saving and reading settings in JSON format
import code128Bcode # DIY Module for creating barcodes with a font
import cv2 # For OpenCV video and picture manipulation
import sys # For accessing system parameters
import os # For accessing users profile path
from PyQt5 import QtWidgets, uic, QtPrintSupport # For the UI and printing
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt # For image scaling
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter # For image handling
```
### Building Apps

Apps can be converted to `exe` files with **PyInsaller**. `spec` files contain istructions how to build delivery packages. The following snippet shows how dependencies are defined:

```
datas=[('code128Bcode.py', '.'), ('productPicture.ui', '.'), ('productPictureSettings.dat', '.')],

```

Allways add non precompiled resources like logos or placeholder images to `datas` section of the `spec` file.

⚠️ When using QT UI recources which are not precompiled into python file you must copy resources like ui or picture files manually into `dist` folder in the first build of your application. If you create your own modules needeb by the app they must either reside in the `libs` folder of the virtual environment or you must add your own python modules into the `.spec` file to copy them automatically during the build process. Alfter 1st build you can edit the created `.spec` file. When you have a `.spec` file you can build with command `PyInstaller studentPicture.spec` or what ever is your build specification file.

If python console is needed it can be enabled by editing `.spec` file and altering `exe = EXE()` block. Change console option to `console=True`.

⚠️ Windows Defender might claim that there is a trojan in the executable. This is a known false positive. Most of computers in the school have FSecure Safe as malware detection software. It does not give any alerts concerning the executable. Defender users may find this article useful: https://python.plainenglish.io/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184.

## Installer
Applications can be distributed with or without an installer. When used without an installer contents of the distribution folder are copied to the other computer. Some of the files are shown in the picture below:

![image](https://user-images.githubusercontent.com/24242044/168031298-51e47538-b4a7-4a97-9837-cc349822a9e7.png)

Distribution can be made with zipped folder containing installation instructions and contents of the distribution folder. Creating an installer is more sophisticated way of delivering the application to a client. Free installer building application is **InstallForge**. You can load it from https://installforge.net/download/. There is a nice tutorial at https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/ about using `PyInstaller` and `InstallForge` It is essential to add instructions for installing **Libre Code 128** font from Goolgle. Font can be found at https://fonts.google.com/specimen/Libre+Barcode+128+Text.
