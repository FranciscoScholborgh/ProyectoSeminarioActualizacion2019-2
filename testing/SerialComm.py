import serial.tools.list_ports
import serial, time

ports = list(serial.tools.list_ports.comports())
foundFlag = False
arduino = None
while(not foundFlag and len(ports) > 0):
    portDescription = ports.pop(0)
    port = portDescription[0]
    arduino = serial.Serial(port, 9600)
    info = arduino.readline()
    data = str(info, 'ascii').split(";")[0]
    if(data == "Key"):
        print("Arduino: ", portDescription)
        break
    else:
        print(portDescription, "no es un prototipo valido")
        arduino.close()
    print(data)
    time.sleep(1)
