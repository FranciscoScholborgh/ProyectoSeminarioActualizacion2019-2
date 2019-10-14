import serial.tools.list_ports
from PyQt5.QtCore import QThread
from abc import ABCMeta, abstractmethod
import time

class ArduinoDetector():

    __instance = None
    
    @staticmethod 
    def getInstance():
      if ArduinoDetector.__instance is None:
          ArduinoDetector()
      return ArduinoDetector.__instance

    def __init__(self):
        if(ArduinoDetector.__instance is not None):
            raise Exception("This class is a singleton!")
        else:
            ArduinoDetector.__instance = self

    def detectarPrototipo(self):
        ports = list(serial.tools.list_ports.comports())
        foundFlag = False
        arduino = None
        while(not foundFlag and len(ports) > 0):
            portDescription = ports.pop(0)
            port = portDescription[0]
            arduino = serial.Serial(port, 9600)
            info = arduino.readline()
            data = str(info, 'ascii').split(";")[0]
            arduino.close()
            if(data == "Key"):
                print("Arduino: ", portDescription)
                arduino_instance = SerialArduino(port, 9600)
                return arduino_instance
        return None

class Arduino(metaclass=ABCMeta):

    @abstractmethod
    def start_reading(self):
        pass

    @abstractmethod
    def stop_reading(self):
        pass

class SerialArduino(Arduino):

    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.running = False
        #self.serialCommunication = serial.Serial(port, baud)

    def getPort(self):
        return self.port

    def getBaud(self):
        return self.baud

    def isRunning(self):
        return self.running

    def setPort(self, port):
        print("unsuported operation")

    def setBaud(self, baud):
        print("unsuported operation")

    def setRunning(self, state):
        self.running = state

    def start_reading(self):
        self.running = True
        while(self.running):
            print("Reading arduino")
            time.sleep(2)

    def stop_reading(self):
        self.running = False

            



