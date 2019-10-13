from PyQt5 import QtWidgets, uic
import sys

class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('vista/cliente.ui', self) # Load the .ui file
        self.show() # Show the GUI

app = QtWidgets.QApplication(sys.argv)
gui = GUI()
app.exec_()