from __future__ import annotations
import serial.tools.list_ports
from PyQt5.QtCore import QThread
from abc import ABCMeta, abstractmethod
from logica.Interfaces import Subject
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

class SerialArduino(Arduino, Subject):

    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.running = False
        self.serialCommunication = None
        self.estado_anterior = "LOCKED"
        self.observers: List[Observer] = []

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

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self.estado_anterior)

    def start_reading(self):
        self.running = True
        self.serialCommunication = serial.Serial(self.port, self.baud)
        while(self.running):
            info = self.serialCommunication.readline()
            data = str(info, 'ascii').split(";")[0]
            if(data != self.estado_anterior):
                self.estado_anterior = data
                if(data == "BREAK IN"):
                    print("NOTIFICA")
                    self.notify()        
                elif(data == "LOCKED"):
                    print("YA NO")
                    self.notify()
                else:
                    self.estado_anterior = "LOCKED"
            time.sleep(0.25)
        self.serialCommunication.close()

    def stop_reading(self):
        self.running = False

            



