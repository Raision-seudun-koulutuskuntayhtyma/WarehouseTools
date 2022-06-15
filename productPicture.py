# EXAMPLE OF QT APPICATION FOR TAKING PRODUCT IMAGES IN SEPARATE THREAD USING WEB CAMERA

# LIBRARIES AND MODULES
# ----------------------

import json # For saving and reading settings in JSON format
import code128Bcode # DIY Module for creating barcodes with a Libre code 128 font
import cv2 # For OpenCV video and picture manipulation
import sys # For accessing system parameters
import os # For accessing users profile path
from PyQt5 import QtWidgets, uic, QtPrintSupport # For the UI and printing
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt # For image scaling
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter # For image handling


# CLASS FOR A SEPARATE THREAD TO CAPTURE VIDEO
# --------------------------------------------

class VideoThread(QThread):

    # ---- CONSTRUCTOR -----
    def __init__(self):
        super().__init__()
        self.alive = True # Property for stopping the video

    # Create signal to change the image field in the UI
    changePixmap = pyqtSignal(QImage)

    
    # The runner function that will be started with start() method
    def run(self):

        # Create a videocapture object and set capture dimensions according to settings file
        file = open('settings.dat', 'r') # Read all settings from the settings file
        settings = json.load(file) # Create a dictionary from JSON data in the settings file
        file.close()
        camIx = settings.get('camIx') # Get the camIX
        hResolution = settings.get('hResolution') # Get the horizontal resolution
        vResolution = settings.get('vResolution') # Get the vertical resolution
        videoStream = cv2.VideoCapture(camIx, cv2.CAP_DSHOW) # Start capturing the webcam
        videoStream.set(cv2.CAP_PROP_FRAME_WIDTH, hResolution) # Set horizontal resolution
        videoStream.set(cv2.CAP_PROP_FRAME_HEIGHT, vResolution) # Set vertical resolution

        # Read the videostream until Video Reset button is pressed
        while self.alive:
            ret, frame = videoStream.read()
            if ret:
                # Resize and convert video to UI
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> RGB
                height, width, channels = rgbImage.shape # Image size & number of channels
                bytesPerLine = channels * width # Calculate how many bytes per video line
                inQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888)
                videoOut = inQtFormat.scaled(640, 360, Qt.KeepAspectRatio) # Size of picture is 50% of original
                self.changePixmap.emit(videoOut) # Signal out the video
    
    # Function to kill the thread, invoked by Reset Video button
    def stop(self):
         self.alive = False


# APPLICATION CLASS FOR THE UI
# -----------------------------

class App(QtWidgets.QWidget):

    # ---- CONSTRUCTOR ----
    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi('productPicture.ui', self)

        # Read the settings file
        self.settingsFile = open('productPictureSettings.dat', 'r') # Read all settings from the settings file
        self.settings = json.load(self.settingsFile) # Dreate a dict fron JSON data

        #  Empty list for photo list Qlist widet in the UI
        self.listItems = [] 

        # UI elements (Direct assignment to properties)
        self.picture = self.productImage # Video window
        self.productCode = self.productId # Line edit for product number
        self.picFolder = self.productPicFolder # Settings: line edit for image folder
        self.videoWidth = self.hResolution # Settings: spinner for horizontal resolution
        self.videoHeight = self.vResolution # Settings: spinner for vertical resolution
        self.camera = self.cameraIxSpinBox # Settings: spinner for web camera index
        self.bigImage = self.catalogPicture # Image for the product catalog
        self.barCode = self.bcLabel # The barcode presentation of the product number
        self.photoList = self.pictureList # List of saved images
        
        

        # Set the intial values and properties of UI elements
        self.captureButton.setEnabled(True) # Enable capture button 
        self.initCamIx = self.settings.get('camIx') # Read the camIx from settings
        self.initPicFolder = self.settings.get('picFolder')
        self.camera.setValue(self.initCamIx) # Set the initial value for camIx spinner
        self.picFolder.setText(self.initPicFolder) # Set the initial value of product picture folder
        self.initVideoWidth = self.settings.get('hResolution') # Read the horizontal resolution from settings
        self.videoWidth.setValue(self.initVideoWidth) # Set the initial value for video width
        self.initVideoHeight = self.settings.get('vResolution') # Read the vertical resolution from settings
        self.videoHeight.setValue(self.initVideoHeight) # Set the initial value for video height

        # --------SIGNALS -------- 

        # Set Camera settings when spin box values are changed
        self.camera.valueChanged.connect(self.adjustSettings)
        self.videoWidth.valueChanged.connect(self.adjustSettings)
        self.videoHeight.valueChanged.connect(self.adjustSettings)

        # Set the product pictute folder setting when edited in the UI
        self.picFolder.textEdited.connect(self.adjustSettings)

        # Start Capture button signal to capture slot -> call capture function
        self.captureButton.clicked.connect(self.capture)

        # Save image to a file with still button 
        self.stillButton.clicked.connect(self.saveStill)

        # Reset video, stops the thread
        self.videoReset.clicked.connect(self.resetCam)

        # Print the product card
        self.printCardButton.clicked.connect(self.printCard)

        # Set the Window Title and initialize the UI
        self.title = 'RASEKO varasohallinta - tuotekuvan tallennus'
        self.initUI()

    # ------------SLOTS------------

    # Set camera parameters and folder path for saving product pictures
    def adjustSettings(self):

        # Read the values of spinners and line edits in the settings section of the UI
        camIx = self.camera.value()
        picFolder = self.picFolder.text()
        hResolution = self.videoWidth.value()
        vResolution = self.videoHeight.value()

        # Read all settings from the settings file
        file = open('productPicturSsettings.dat', 'r') 
        settings = json.load(file)
        file.close()

        # Set individual values
        settings['camIx'] = camIx # Set the webcam index value
        settings['picFolder'] = picFolder # Set the picture folder
        settings['hResolution'] = hResolution # Set the horizontal resolution of the webcam
        settings['vResolution'] = vResolution # Set the vertical resolution of the webcam
        
        # Save settings
        file = open('settings.dat', 'w') 
        json.dump(settings, file)
        file.close()
        

    # Capture video: started by signal from captureButton
    def capture(self):
        videoThread.alive = True
        videoThread.start()
        videoThread.changePixmap.connect(self.setImage)
        self.captureButton.setEnabled(False) # Disable capture button
        

    def resetCam(self):
        self.captureButton.setEnabled(True) # Enable capture button 
        videoThread.stop() # Stop the video thread
        
    # Save curent frame as a JPG file: started by signal from stillButton
    def saveStill(self):
        file = open('productPictureSettings.dat', 'r') # Read all settings from the settings file
        settings = json.load(file)
        folderToSave = settings.get('picFolder') # Get the product picture folder name
        file.close()

        # The folder will be under users Pictures 
        relativeWorkingDirectory = '\Pictures' + '\\' + folderToSave

        # Get users profile path and join it with Pictures folder's path
        userProfilePath = os.path.expanduser('~')
        workingDirectory = userProfilePath + relativeWorkingDirectory

        # Create the folder if it does not exist
        if not os.path.exists(workingDirectory):
            os.mkdir(workingDirectory)

        # Create a pixmap to be saved
        stillImage = self.picture.pixmap()
        fileName = workingDirectory + '\\' + self.productCode.text() + '.jpg'

        # Check the length of the filename: must contain at least one chr and extension .jpg
        if len(self.productCode.text()) > 0:
            stillImage.save(fileName, 'jpg')

            # Read the file as pixmap for previewing
            landscapePixmap = QPixmap(fileName)

            # Transform the pixmap for the preview field (potrait)
            transformation = QTransform() # Create transformation object
            # transformation.scale(0.5, 0.5) # Scale to half size
            transformation.rotate(90) # Rotate to potrait
            potraitPixmap = landscapePixmap.transformed(transformation) # Run the transformation
            self.bigImage.setPixmap(potraitPixmap)
            # Create the barcode with Libre barcode 128 font
            productId = self.productCode.text()
            bCodeSymbols = code128Bcode.string2barcode(productId)
            self.barCode.setText(bCodeSymbols) # Show on  barcode label
            # Add picture to the list of pictures taken
            self.photoList.clear() # Clear list before adding items
            self.listItems.append(productId) # Add current picture
            self.photoList.addItems(self.listItems)

        else:
            # Show error message about the file name
            alarmWindow = QtWidgets.QMessageBox()
            alarmWindow.setIcon(QtWidgets.QMessageBox.Critical)
            alarmWindow.setWindowTitle('Virheellinen tai puuttuva tuotekoodi')
            alarmWindow.setText('Tuotekoodissa on oltava vähintään 1 merkki!')
            alarmWindow.exec_()
        # TODO: check for illegal characters in product code 
    
    # Print the product card
    def printCard(self):
        # Create a printer object as painter device, High resolution printing
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        # printer = QtPrintSupport.QPrinter() the low resolution alternative
        # Create a printer dialog object
        printDialog = QtPrintSupport.QPrintDialog(printer, self)

        # Check if user starts printing
        if printDialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:

            # Create a painter object for creating a page to print
            painter = QPainter()

            # Start creating an image to print from cardFrame in the UI
            painter.begin(printer) # Start the painter using the printer device
            card = self.productCard.grab() # Grab the UI element to print
            transformation = QTransform() # Create transformation object for scaling the image
            transformation.scale(4, 4) # Set resizing factors for credit card size, values according to test printer
            sizedCard = card.transformed(transformation) # Apply the transformation
            painter.drawPixmap(10, 10, sizedCard) # Create a pixmap to print
            painter.end() # Close the priter
    

    # Slot for receiving the video: signaled by videoThread
    @pyqtSlot(QImage) # @ decorator ie. function takes another function as argument and returns a function
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image))
        # self.captureButton.setEnabled(False)
        fileName = self.productCode.text() + '.jpg'
        if len(fileName) > 4:
            self.stillButton.setEnabled(True)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

if __name__ == '__main__':

    # Create a thread for video
    videoThread = VideoThread()
    
    # Create and run the application
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainwindow = App()
    mainwindow.productCode.setFocus() # Put the cursor into product id field
    app.exec_()