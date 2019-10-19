from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic
from logica.Interfaces import Observer 
from logica.Client import TCPClientNotifier, UDPClientNotifier
import sys, time, threading, winsound

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
        self.warning = False
        self.show()  

    def isWarning(self):
        return self.warning

    def setWaring(self, state):
        self.warning = state

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
            protocol = self.configBox.get_selected_protocol()
            if(protocol == "TCP"):
                self.notifer = TCPClientNotifier()
            elif(protocol == "UDP"):
                print("I TRIED?")
                self.notifer = UDPClientNotifier()
            print("Activated Alarm")
            print("Notifier: ", self.notifer)
            self.status_lbl.setText("Estado alarma: Activada")
            self.configBtn.setEnabled(False)
            self.switch_btn.setText("OFF")
            self.switch_btn.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(255, 99, 71);")
            self.notifer.attach(self)
            print("BUQUEE DE GUERAAAA")
            t = threading.Thread(target=self.notifer.run, daemon=True)
            t.start()
            self.switch_btn.clicked.disconnect(self.activateAlarm)
            self.switch_btn.clicked.connect(self.__disableAlarm)
        except:
            print("No se pudo conectar")
        time.sleep(1)
        self.__enable_buttons()

    def __turnOFF(self):
        self.__disable_buttons()
        self.status_lbl.setText("Estado alarma: Desactivada")
        self.configBtn.setEnabled(True)
        self.switch_btn.setText("ON")
        self.switch_btn.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(50, 205, 50);")
        t = threading.Thread(target=self.notifer.shutdown, daemon=True)
        t.start()
        time.sleep(1)
        self.__enable_buttons()
        self.switch_btn.clicked.disconnect(self.__disableAlarm)
        self.switch_btn.clicked.connect(self.activateAlarm)

    def activateAlarm(self):
        t = threading.Thread(target=self.__turnON, daemon=True)
        t.start()
        #self.__turnON()
        

    def __disableAlarm(self):
        self.warning = False
        t = threading.Thread(target=self.__turnOFF, daemon=True)
        t.start()

    def notify_trespass(self):
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)
        self.warning = True
        while (self.warning):
            winsound.Beep(frequency, duration)
            
    def update(self, state):
        if(state == "BREAK IN"):
            self.status_lbl.setText("Estado alarma: Intrusión detectada")
            t = threading.Thread(target=self.notify_trespass, daemon=True)
            t.start()       
        elif(state == "SHUTDOWN"):
            self.status_lbl.setText("Estado alarma: Señal perdida")  
            t = threading.Thread(target=self.notify_trespass, daemon=True)
            t.start()
            #self.__disableAlarm()
        else:
            self.status_lbl.setText("Estado alarma: Activada")  
            self.warning = False


app = QApplication(sys.argv)
gui = GUI()
app.exec_()