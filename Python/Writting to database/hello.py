import mysql.connector
from datetime import date, datetime, timedelta

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ksiegarnia"
)

print(mydb)
print("\n")

print("Show databases:")
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
  print(x)
print("\n")
print("Conected to ksiegarnia")
print("\n")

mycursor.execute("SHOW TABLES")
print("Show tables:")
for x in mycursor:
  print(x)
print("\n")

name = 'Łukasz'
query = ("SELECT idksiazki FROM ksiazki "
         "WHERE imieautora = %s")
mycursor.execute(query, (name,))
myresult = mycursor.fetchone()
print(myresult)
print("\n")

actualDate = datetime.now().date()
actualHour = datetime.now().time()
formatedHour = actualHour.strftime("%H:%M:%S")
print("Aktualna data: ", actualDate, " ", formatedHour)
print("\n")

print("Insert")
idksiazki = myresult[0]
idklienta = 2
sql_insert_query = ("INSERT INTO `zamowienia` (`idklienta`, `idksiazki`, `data`, `godzina`) VALUES (%s,%s,%s,%s)")
insert_tuple = (idklienta, idksiazki, actualDate, formatedHour)
mycursor.execute(sql_insert_query, insert_tuple)
mydb.commit()
print(mycursor.rowcount, "record inserted.")
print("\n")