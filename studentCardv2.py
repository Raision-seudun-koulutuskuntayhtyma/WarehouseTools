# APPLICATION FOR CREATING AND PRINTING STUDENT CARDS
# ---------------------------------------------------

# LIBRARIES AND MODULES
import sys # For accessing system parameters
import os # For directory and file handling
from PyQt5 import QtWidgets, uic , QtPrintSupport # For the UI and printing
from PyQt5.QtGui import QPixmap, QTransform, QPainter # For image handling

# CLASS DEFINITIONS

# The Application
class App(QtWidgets.QWidget):

    # Constructor
    def __init__(self):
        super().__init__()

        # Load the UI
        uic.loadUi('studentCardv2.ui', self)

        # UI elements 
        self.bCode = self.studentBarcode
        self.studentId = self.studentNumberEdit
        self.picture = self.pictureLabel
        self.nameInput = self.studentName
        self.birth = self.dateOfBirth
        self.study = self.studyName
        self.year = self.season
        self.loadPictureButton.setEnabled(False)

        # Signals
        self.studentId.textEdited.connect(self.starProcessing) # When edited activate Open Picture button
        self.loadPictureButton.clicked.connect(self.openPicture) # When clicked open Load Picture dialog
        self.printButton.clicked.connect(self.printCard) # When clicked print card and clear personal information
        
        # Set the Window Title and initialize the UI
        self.title = 'Opiskelijakortti'
        self.initUI()

    # Slots

    def starProcessing(self):
        self.loadPictureButton.setEnabled(True)

    def stopProcessing(self):
        self.loadPictureButton.setEnabled(False) # Disable loadpicture button
        # Clear all personal information but keep the course name and the season 
        self.studentId.clear()
        self.nameInput.clear()
        self.birth.clear()

        

    # Generate barcode from the student id
    def setBarcode(self):
        id = self.studentId.text()
        barCode = string2barcode(id)
        self.bCode.setText(barCode)
        


    def printCard(self):
        # Create a printer object as painter device, High resolution printing
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)

        # Create a printer dialog object
        printDialog = QtPrintSupport.QPrintDialog(printer, self)

        # Check if user starts printing
        if printDialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:

            # Create a painter object for creating a page to print
            painter = QPainter()

            # TODO: This should be tested with card printer with and without  HighResolution by using
            # printers own scaling options ie scale to fit found in print dialog. In the future put 
            # scaling parameters (resolution into UI's Options Menu) Also check margins now 10 dots

            # Start creating an image to print from cardFrame in the UI
            painter.begin(printer) # Start the painter using the printer device
            card = self.cardFrame.grab() # Grab the UI element to print
            transformation = QTransform() # Create transformation object for scaling the image
            transformation.scale(2.4, 2.4) # Set resizing factors for credit card size, values according to test printer
            sizedCard = card.transformed(transformation) # Apply the transformation
            painter.drawPixmap(10, 10, sizedCard) # Create a pixmap to print
            painter.end() # Close the priter

            # Disable Load Picture Button
            self.stopProcessing()

    def openPicture(self):
        relativeWorkingDirectory = '\Pictures'
        # Get users profile path and join it with Pictures folder's path
        userProfilePath = os.path.expanduser('~')
        workingDirectory = userProfilePath + relativeWorkingDirectory
        fileName, check = QtWidgets.QFileDialog.getOpenFileName(None, 'Valitse kuva', workingDirectory, 'Kuvatiedostot (*.jpg *.png)')
        if fileName:
            
            studentPhoto = QPixmap(fileName)
            self.picture.setPixmap(studentPhoto)

            self.setBarcode()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.show()

# FUNCTIONS FOR GENERATING BARCODES   

def string2barcode(text, codeType='B', fontShift='common'):
    """Generates a Code 128 barcode from given text string. For Libre 128 barcode font
    Args:
        text (str): The text to be encoded into a barcode
        codeType (str, optional): Version of the barcode. Defaults to 'B'.
        fontShift (str, optional): Character set used in the text string. Defaults to 'common'.

    Returns:
        str: character string presentation of the barcode
    """
    
    startCodeList = {'A' : 103, 'B' : 104, 'C' : 105} # Value of the start symbol in different variations
    fontPositionList = {'common' : 100, 'uncommon' : 105, 'barcodesoft' : 145} # Systems for presentingstart and stop symbols
    addedValue = fontPositionList.get(fontShift) # Get a value to shift symbols in the font
    startSymbolValue = startCodeList.get(codeType) # Choose start symbol value according to code type A, B or C
    stopSymbolValue = 106 # Allways 106
    stringToCode = text # A srting to be encoded into barcode
    cntr = 0 # Se counter to 0
    weightedSum = startSymbolValue # Add the value of the start symbol to weighted value

    # Handle all characters in the string
    for character in stringToCode:
        cntr += 1

        # Check if character more or less than or equal to 126
        if ord(character) < 127:            
            bCValue = ord(character) -32 # < 127 Original 7 bit ASCII allways subtract 32
        else:
            bCValue = ord(character) - addedValue # 8 bit charater subtract according to font shifting table

        weightedSum += bCValue * cntr # Calculate the position weighted sum

    chksum = weightedSum % 103 # Calculate modulo 103 checksum

    # Build the barcode 
    startSymbol = chr(startSymbolValue + addedValue) # Create a start symbol accordint ot the type
    stopSymbol = chr(stopSymbolValue + addedValue) # Create a stop symbol
    chkSymbol = chr(chksum + 32) # Create the checksum symbol
    barCode = startSymbol + stringToCode + chkSymbol + stopSymbol
    return barCode
    


# CREATING AND STARTING THE APPLICATION  
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainwindow = App()
    app.exec_()