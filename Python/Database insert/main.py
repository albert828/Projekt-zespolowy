#Na początku należy uzupełnić dane do bazy
#oraz dane do serial portu
import serial
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
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database=dbName
)
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
ser = serial.Serial('com4', 115200)
while True:
    #wczytanie linijki z arduino czeka na dane i rzutowanie na string
    arduinoData = str(ser.readline())
    #rozdzielenie danych po spacjach
    splitedData = (arduinoData[2:][:-5]).split()
    roomName = splitedData[0]
    sensorName = splitedData[1]
    sensorValue = int(splitedData[2])
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
