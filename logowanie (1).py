import simplejson
import psycopg2
import csv
import datetime

with open("dane_log.json") as db_con_file:
    creds=simplejson.loads(db_con_file.read())
conn = psycopg2.connect(
    host=creds['host_name'],
    user=creds['user_name'],
    dbname=creds['db_name'],
    password=creds['password'],
    port=creds['port_number']
)

cursor=conn.cursor()

def ImportCSV():
    with open("stacje.csv",'r',newline="") as file:
        reader=csv.reader(file)
        next(reader)
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Stacje(
        ID INTEGER NOT NULL PRIMARY KEY,
        SZEROKOSC REAL NOT NULL,
        DLUGOSC REAL NOT NULL,
        KRAJ text,
        MIASTO text
        )
        ''')
        conn.commit() 
        for row in reader:
            cursor.execute('''
            INSERT INTO Stacje (ID,SZEROKOSC,DLUGOSC,KRAJ,MIASTO) VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT DO NOTHING''',
                           (row))
            conn.commit() 
            
            
            
            
            
    with open("pomiary.csv",'r',newline="") as file:
        reader=csv.reader(file)
        next(reader)
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS Pomiary(
        ID_stacji INTEGER NOT NULL,
        Temperatura REAL,
        Wiatr REAL,
        Cisnienie REAL,
        Wilgotnosc REAL,
        Czas_Pomiaru TIME NOT NULL,
        FOREIGN KEY(ID_stacji) REFERENCES Stacje(ID)
        )
        ''')
        conn.commit() 
        for row in reader:
            cursor.execute('''
            INSERT INTO Pomiary (ID_stacji,Temperatura,Wiatr,Cisnienie,Wilgotnosc,Czas_Pomiaru) VALUES (%s,%s,%s,%s,%s,%s)
            ON CONFLICT DO NOTHING''',
                           (row))
            conn.commit() 

            
def Drop():
    cursor.execute('''DROP TABLE Pomiary''')        
    conn.commit()
    cursor.execute('''DROP TABLE Stacje''')        
    conn.commit() 

def AddEntryPomiar():
    try:
        a=int(input("ID: "))
        b=float(input("Temperatura: "))
        c=float(input("Wiatr: "))
        d=float(input("Cisnienie: "))
        e=float(input("Wilgotnosc: "))
        cursor.execute(f'''
        INSERT INTO Pomiary(ID_stacji,Temperatura,Wiatr,Cisnienie,Wilgotnosc,Czas_Pomiaru)
        VALUES(%s,%s,%s,%s,%s,%s)''',
        (a,b,c,d,e,datetime.datetime.now()))
        conn.commit()
    except:
        print("Cos poszlo nie tak.")

        
while(True):
    option=int(input('Wybierz:\n1.Załaduj CSV.\n2.Dodaj pomiar ze stacji.\n3.Usun.\n4.Wyjdz.\n'))
    if(option==1):
        ImportCSV()
    elif(option==2):
        AddEntryPomiar()
    elif(option==3):
        Drop()
    elif(option==4):
        cursor.close()
        conn.close()
        exit()