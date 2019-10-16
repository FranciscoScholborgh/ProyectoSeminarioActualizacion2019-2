from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QDir
from PyQt5 import uic
import sys
from logica.Arduino import ArduinoDetector
import threading, time, os, inspect
from logica.Server import TCPServer

class GUI(QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('vista/server.ui', self)
        self.stateBtn.clicked.connect(self.runServer)
        self.show()  

    def setting_server(self):
        self.stateBtn.setEnabled(False)
        tcp = self.tcp.isChecked()
        udp = self.udp.isChecked()
        rmi = self.rmi.isChecked()
        if(not tcp and not udp and not rmi):
            print("Seleccione un opcion, no sea prro :V")
        else:
            selected_protocol = None
            self.server = None
            if(tcp):
                selected_protocol = "TCP"
                print("TCP SERVER")
                self.server = TCPServer()
            elif(udp):
                selected_protocol = "UDP"
                print("UDP SERVER")
            else:
                selected_protocol = "RMI"
                print("RMI SERVER")
            ardDetector = ArduinoDetector.getInstance()
            self.arduino = ardDetector.detectarPrototipo()
            if(self.arduino is not None):
                print("do something")
                self.stateBtn.clicked.disconnect(self.runServer)
                self.stateLbl.setText("Estado Servidor: Activo(" + selected_protocol + ")")
                self.stateBtn.setText("Stop")
                icon = QIcon(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + QDir.separator() +  "vista/stopicon.png")
                self.stateBtn.setIcon(icon)
                self.stateBtn.setIconSize(QSize(30, 30))
                self.stateBtn.clicked.connect(self.stopServer)
                self.arduino.attach(self.server)
                t = threading.Thread(target=self.arduino.start_reading, daemon=True)
                t.start()
                server_thread = threading.Thread(target=self.server.run_server, daemon=True)
                server_thread.start()
            else:
                print("No ha sido encontrado el dispositivo de alarma")
        time.sleep(1)
        self.stateBtn.setEnabled(True)

    def shutdown_server(self):
        self.arduino.stop_reading()
        self.server.shutdown_server()
        self.stateBtn.clicked.disconnect(self.stopServer)
        self.stateBtn.setEnabled(False)
        self.stateLbl.setText("Estado Servidor: Inactivo")
        self.stateBtn.setText("Run")
        icon = QIcon(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + QDir.separator() +  "vista/runicon.png")
        self.stateBtn.setIcon(icon)
        self.stateBtn.setIconSize(QSize(30, 30))
        time.sleep(1)
        self.stateBtn.setEnabled(True)
        self.stateBtn.clicked.connect(self.runServer)

    def runServer(self):
        t = threading.Thread(target=self.setting_server, daemon=True)
        t.start()

    def stopServer(self):
        print("STOPPED")
        t = threading.Thread(target=self.shutdown_server, daemon=True)
        t.start()
        
app = QApplication(sys.argv)
gui = GUI()
app.exec_()