from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
from logica.Interfaces import Observer 
from logica.Client import TCPClientNotifier
import sys, time, threading

class SelectorProtocolGUI(QMainWindow):

    def __init__(self, parent):
        super(SelectorProtocolGUI, self).__init__(parent)
        uic.loadUi('vista/selector.ui', self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.selectBtn.clicked.connect(self.select_protocolo)
        self.selected_protocol = "TCP"
        
    def select_protocolo(self):
        tcp = self.tcp.isChecked()
        udp = self.udp.isChecked()
        rmi = self.rmi.isChecked()
        if(tcp):
            self.selected_protocol = "TCP"
        elif(udp):
            self.selected_protocol = "UDP"
        else:
            self.selected_protocol = "RMI"
        self.hide()

    def get_selected_protocol(self):
        return self.selected_protocol


class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('vista/cliente.ui', self)
        self.configBtn.clicked.connect(self.select_protocolo)
        self.switch_btn.clicked.connect(self.activateAlarm)
        self.configBox = SelectorProtocolGUI(self)
        self.notifer = None
        self.show()  

    def select_protocolo(self):
        self.configBox.show()

    def __enable_buttons(self):
        self.configBtn.setEnabled(True)
        self.switch_btn.setEnabled(True)
    
    def __disable_buttons(self):
        self.configBtn.setEnabled(False)
        self.switch_btn.setEnabled(False)

    def __turnON(self):
        self.__disable_buttons()
        try:
            self.notifier = TCPClientNotifier()
            print("Activated Alarm")
            self.status_lbl.setText("Estado alarma: Activada")
            self.configBtn.setEnabled(False)
            self.switch_btn.setText("OFF")
            self.switch_btn.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(255, 99, 71);")
            self.notifer.attach(self)
            t = threading.Thread(target=self.notifer.run, daemon=True)
            t.start()
            #continua desde aqui :3
        except ConnectionRefusedError:
            print("No se pudo conectar")
        time.sleep(1)
        self.__enable_buttons()

    def activateAlarm(self):
        t = threading.Thread(target=self.__turnON, daemon=True)
        t.start()

    def __disableAlarm(self):
        print("Disable Alarm")
        self.status_lbl.setText("Estado alarma: Desactivada")
        self.configBtn.setEnabled(True)
        self.switch_btn.setText("ON")
        self.switch_btn.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(50, 205, 50);")
        t = threading.Thread(target=self.notifer.shutdown, daemon=True)
        t.start()
        time.sleep(1)

    def update(self, state):
        print("GUI UPDATED WITH: ", state)


app = QApplication(sys.argv)
gui = GUI()
app.exec_()