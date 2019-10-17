from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sys

class SelectorProtocolGUI(QMainWindow):

    def __init__(self, parent):
        super(SelectorProtocolGUI, self).__init__(parent)
        uic.loadUi('vista/selector.ui', self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.selectBtn.clicked.connect(self.select_protocolo)
        
    def select_protocolo(self):
        tcp = self.tcp.isChecked()
        udp = self.udp.isChecked()
        rmi = self.rmi.isChecked()
        self.hide()

class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('vista/cliente.ui', self)
        self.configBtn.clicked.connect(self.select_protocolo)
        self.configBox = SelectorProtocolGUI(self)
        self.show()  

    def select_protocolo(self):
        self.configBox.show()


app = QApplication(sys.argv)
gui = GUI()
app.exec_()