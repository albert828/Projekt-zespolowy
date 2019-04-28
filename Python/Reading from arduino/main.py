import serial
#import serial.tools.list_ports as port_list

#ports = list(port_list.comports())
#for p in ports: 
#    print(p)

ser = serial.Serial('com4', 115200)
while True:
    arduinoData = str(ser.readline())
    splitedData = (arduinoData[2:][:-5]).split()
    sensorName = splitedData[0]
    sensorValue = int(splitedData[1])
    print(sensorName, sensorValue)
    #print("\n")