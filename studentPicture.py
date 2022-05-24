# SIMPLE APP FOR TAKING SQUARE PICTURES FOR STUDENT CARDS
# -------------------------------------------------------

# LIBRARIES AND MODULES
import cv2 # For OpenCV video and picture manipulation for reading Web camera
import sys # For accessing system parameters
import os # For file paht handling
from PyQt5 import QtWidgets, uic # For the UI
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot # For creating multiple threads and signaling between UI and Video thread
from PyQt5.QtCore import Qt, QRect # For image scaling and cropping
from PyQt5.QtGui import QImage, QPixmap, QTransform # For image handling

# SEPARATE THREAD FOR VIDEO CAPTURE
class VideoThread(QThread):

    # Create signal to change the image field in the UI
    changePixmap = pyqtSignal(QImage)

    # The runner function (starts the thread, name of the function must be run)
    def run(self):

        # Create a videocapture object and set capture dimensions to 1280 x 720
        # Mika's work computer cameras 0:Cannon, 1:ThinkPad Internal, 2:Logitech external
        # Cam indexes may shift ie 1 can be external and 2 internal when external cam is
        # unplugged and plugged again wihtout booting the computer. Cannon is always 0
        videoStream = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        videoStream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        videoStream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # Produce video image from the camera
        while True:
            ret, frame = videoStream.read()
            if ret:
                # Mirror the video and convert video to UI
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # BGR -> RGB
                height, width, channels = rgbImage.shape # Image size & number of channels
                bytesPerLine = channels * width # Calculate how many bytes per video line
                inQtFormat = QImage(rgbImage.data, width, height, bytesPerLine, QImage.Format_RGB888) # Change format
                mirroredImage = inQtFormat.mirrored() # Mirror the video to help putting face to correct position
                transformatation = QTransform() # Create a transformation object
                transformatation.rotate(180) # Mirrored image is upside down so it must be rotated
                videoOut= mirroredImage.transformed(transformatation) # Do the transformation
                self.changePixmap.emit(videoOut) # Signal out the video

# APPLICATION CLASS FOR THE UI
class App(QtWidgets.QWidget):
    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi('StudentPicture.ui', self)

        # UI elements (Direct assignment to properties)
        self.picture = self.videoImage
        self.student = self.studentId
        self.preview = self.photoPreview
        self.captureButton.setEnabled(True)
        
        # Start Capture button signal to capture slot -> call capture function
        self.captureButton.clicked.connect(self.capture)

        # Save image to a file with still button 
        self.stillButton.clicked.connect(self.saveStill)

        # Set the Window Title and initialize the UI
        self.title = 'Student picture from video'
        self.initUI()

    # SLOTS

    # Capture video: started by signal from captureButton
    def capture(self):
        videoThread = VideoThread(self) # Create a new thread object
        videoThread.changePixmap.connect(self.setImage) # When signaled call slot function
        videoThread.start() # Start the thread
        
    # Save and crop the curent frame as a JPG file: started by signal from stillButton
    def saveStill(self):
        relativeWorkingDirectory = '\Pictures'
        # Get users profile path and join it with Pictures folder's path
        userProfilePath = os.path.expanduser('~')
        workingDirectory = userProfilePath + relativeWorkingDirectory
        stillImage = self.picture.pixmap() # Create a pixmap to be saved
        transformation = QTransform() # Create a transformation object
        transformation.scale(0.5, 0.5) # Set scale for transformation object
        scaledImage = stillImage.transformed(transformation) # Run the transformation
        cropArea = QRect(0, 0, 360, 360) # Define cropping box
        squarePixmap = scaledImage.copy(cropArea) # Copy the cropped image pixels
        fileName = self.student.text() + '.jpg' # File name is the student number
        fullPathFileName = os.path.join(workingDirectory, fileName) # Build a path to the file in Pictures folder
        # Check the length of the filename: must contain at least one chr and extension .jpg
        if len(fileName) > 4:
            squarePixmap.save(fullPathFileName, 'jpg')
            # Read the file as pixmap for previewing
            self.preview.setPixmap(squarePixmap) # Set the label

    # Slot for receiving the video: signaled by videoThread
    @pyqtSlot(QImage) # @ decorator ie. function takes another function as argument and returns a function
    def setImage(self, image):
        self.picture.setPixmap(QPixmap.fromImage(image)) # Create a pixmap for the label
        self.captureButton.setEnabled(False)
        fileName = self.student.text() + '.jpg' # Student number will be the filename

        # Activate button if there is a student number in the studentId field
        if len(fileName) > 4:
            self.stillButton.setEnabled(True)

    # Function for initialising the UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

# RUN THE APPLICATION
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) # Create the application object
    app.setStyle('Fusion') # Set Window style to non native
    mainwindow = App() # Create the main window
    app.exec_() # Start the application
