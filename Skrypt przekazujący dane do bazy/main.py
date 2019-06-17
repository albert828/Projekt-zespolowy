import socket 
import mysql.connector
from datetime import date, datetime, timedelta

def update_command(roomName, sensorName, command):
  """!@brief Funkcja odświeża komunikaty z zalecanymi czynnościami dla użytkownika.
  @param[in] roomName  Nazwa pokoju w którym komunikat ma być odświeżony
  @param[in] sensorName Nazwa czujnika dla którego komunikat ma być odświeżony
  @param[in] command Komunikat w postaci stringu
  """
  query = ("UPDATE rooms SET " + sensorName + " = '" + command + "' WHERE name = '" + roomName + "';")
  return query

##przechowuje nazwę bazy danych z którą ma się łączyć
dbName = "microclimate"

#dane do połączenia
##przechowuje uchwyt do bazy danych
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
##kursor do wykonywania poleceń
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
##IP na którym nasłuchujemy. 0.0.0.0 oznacza że od wszystkich
UDP_IP = "0.0.0.0"
##port na którym nasłuchujemy
UDP_PORT = 32998
##gniazdo do połączenia udp
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    #wczytanie linijki z arduino czeka na dane i rzutowanie na string
    ##przechowuje adres IP z którego otrzymaliśmy dane przez UDP
    addr = ""
    data, addr = sock.recvfrom(1024)
    ##dane otrzymane przez UDP
    data = data[:-2]
    data = data.decode('utf-8')
    print(data)

    #rozdzielenie danych po spacjach
    ##przechowuje wektor z rozdzielonymi danycmi
    splitedData = data.split()
    ##przechowuje nazwę pokoju dla którego wykonujemy pomiary
    roomName = splitedData[0]
    ##przechowuje nazwę czujnika dla którego wykonujemy pomiary
    sensorName = splitedData[1]
    ##przechowuje wartość aktualnego pomiaru dla czujnika
    sensorValue = int(float(splitedData[2]))
    ##przechowuje aktualny komunikat użytkownika
    command = ""
    for x in range (3, len(splitedData)):
      command += (splitedData[x] + " ")

    #żądanie sql
    query = update_command(roomName, sensorName, command)
    mycursor.execute(query)
    ##przechowuje aktualne zapytanie do bazy danych
    query = ("SELECT sensor_id FROM sensors "
            "WHERE name = %s")
    # %s wczyta sensorName
    mycursor.execute(query, (sensorName,))
    #pobranie jednego rekordu
    ##przechowuje ID czujnika dla którego wykonujemy pomiary
    sensorId = mycursor.fetchone()
    #pobranie id
    sensorId = sensorId[0]
    #analogicznie jw
    query = ("SELECT room_id FROM rooms "
            "WHERE name = %s")
    mycursor.execute(query, (roomName,))
    ##przechowuje ID pokoju dla którego wykonujemy pomiary
    roomId = mycursor.fetchone()
    roomId = roomId[0]
    #pobranie aktualnej daty
    ##przechowuje aktualną datę
    actualDate = datetime.now()
    #formatowanie do bazy
    ##przechowuje sformatowaną datę
    formatedDate = actualDate.strftime('%Y-%m-%d %H:%M:%S')
    
    #wstawienie rekordu
    ##przechowuje zapytania typu instert
    sql_insert_query = ("INSERT INTO `measurement` (`sensor_id`, `value`,`room_id`, `date`) VALUES (%s,%s,%s,%s)")
    ##lista paramatrów do zapytania typu insert
    insert_tuple = (sensorId, sensorValue, roomId, formatedDate)
    mycursor.execute(sql_insert_query, insert_tuple)
    #potwierdzenie zmian
    mydb.commit()

