from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sys

class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('vista/server.ui', self)
        self.show()

app = QApplication(sys.argv)
gui = GUI()
app.exec_()