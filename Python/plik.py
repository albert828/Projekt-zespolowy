#Na początku należy uzupełnić dane do bazy
#oraz dane do serial portu
import socket 
import mysql.connector
from datetime import date, datetime, timedelta
#import serial.tools.list_ports as port_list


def update_command(roomName, sensorName, command):
  query = ("UPDATE rooms SET " + sensorName + " = '" + command + "' WHERE name = '" + roomName + "';")
  #print(query)
  return query

#ports = list(port_list.comports())
#for p in ports: 
#    print(p)
#nazwa bazy
dbName = "microclimate"
#dane do połączenia
mydb = mysql.connector.connect(host='127.0.0.1',
                                   database='database',
                                   user='user',
                                   password='password')

# wyświetlenie połączenia
print("Conected to: ", dbName)
print("\n")

print("Show databases:")
#wyświetlenie dostępnych baz
#ustawienie wskaźnika na bazę
mycursor = mydb.cursor()
#wykonanie żądania wyświetlenia
mycursor.execute("SHOW DATABASES")
#wyświetlenie linsty baz
for x in mycursor:
  print(x)
print("\n")

#wysłanie żądania wyświetlenia tabel w bazie
mycursor.execute("SHOW TABLES")
print("Show tables:")
for x in mycursor:
  print(x)
print("\n")

#otwarcie Serial portu
UDP_IP = "0.0.0.0"
UDP_PORT = 32998
  
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    #wczytanie linijki z arduino czeka na dane i rzutowanie na string
    data, addr = sock.recvfrom(1024)

    data = data[:-2]
    data = data.decode('utf-8')

    print(data)
    #rozdzielenie danych po spacjach
    splitedData = data.split()
    roomName = splitedData[0]
    sensorName = splitedData[1]
    sensorValue = int(float(splitedData[2]))
    command = ""
    for x in range (3, len(splitedData)):
      command += (splitedData[x] + " ")
    #print(sensorName, sensorValue, roomName)
    #print("\n")
    #żądanie sql
    query = update_command(roomName, sensorName, command)
    mycursor.execute(query)

    query = ("SELECT sensor_id FROM sensors "
            "WHERE name = %s")
    # %s wczyta sensorName
    mycursor.execute(query, (sensorName,))
    #pobranie jednego rekordu
    sensorId = mycursor.fetchone()
    #pobranie id
    sensorId = sensorId[0]
    #print("Sensor id:",sensorId)
    #print("\n")
    #analogicznie jw
    query = ("SELECT room_id FROM rooms "
            "WHERE name = %s")
    mycursor.execute(query, (roomName,))
    roomId = mycursor.fetchone()
    roomId = roomId[0]
    #pobranie aktualnej daty
    actualDate = datetime.now()
    #actualHour = datetime.now().time()
    #formatowanie do bazy
    formatedDate = actualDate.strftime('%Y-%m-%d %H:%M:%S')
    #print("Aktualna data:", actualDate, formatedHour)
    #print("\n")

    #print("Insert", sensorName, "ID =", sensorId, "Value =", sensorValue, "czas:",actualDate, formatedHour, "pokoj", roomName, "Id pokoju", roomId)
    #wstawienie rekordu
    sql_insert_query = ("INSERT INTO `measurement` (`sensor_id`, `value`,`room_id`, `date`) VALUES (%s,%s,%s,%s)")
    insert_tuple = (sensorId, sensorValue, roomId, formatedDate)
    mycursor.execute(sql_insert_query, insert_tuple)
    #potwierdzenie zmian
    mydb.commit()
    #print(mycursor.rowcount, "record inserted.")
    #print("\n")

