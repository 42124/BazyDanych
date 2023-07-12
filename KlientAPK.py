import sqlite3
import datetime
from geopy.geocoders import Nominatim
from time import sleep
import random
import math
import pandas as pd

geolocator=Nominatim(user_agent="2")
db = sqlite3.connect("Pogoda.db")
cursor = db.cursor()
cursor.execute('''PRAGMA foreign_keys = ON''')
print("Połączono z bazą.")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stacje(
        ID INTEGER NOT NULL PRIMARY KEY,
        Szerokosc REAL NOT NULL,
        Dlugosc REAL NOT NULL,
        Kraj CHAR,
        Miasto CHAR
        )
    ''')
db.commit()
cursor.execute('''
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
db.commit()

def AddEntryStacja():
    try:
        a=int(input("ID: "))
        b=input("Szerokosc: ")
        c=input("Dlugosc: ")
        d=""
        e=""
        location = geolocator.reverse(b+","+c,language='en')
        address = location.raw['address']
        print(address)
        if "country" in address:
            d=address["country"]
        if "town" in address:
            e=address["town"]
        elif "city" in address:
            e=address["city"]
        b=float(b)
        c=float(c)
        cursor.execute(f'''
        INSERT INTO Stacje(ID,Szerokosc,Dlugosc,Kraj,Miasto)
        VALUES(?,?,?,?,?)''',
        (a,b,c,d,e))
        db.commit()
    except:
        print("Cos poszlo nie tak.")

def AddEntryPomiar():
    try:
        a=int(input("ID: "))
        b=float(input("Temperatura: "))
        c=float(input("Wiatr: "))
        d=float(input("Cisnienie: "))
        e=float(input("Wilgotnosc: "))
        cursor.execute(f'''
        INSERT INTO Pomiary(ID_stacji,Temperatura,Wiatr,Cisnienie,Wilgotnosc,Czas_Pomiaru)
        VALUES(?,?,?,?,?,?)''',
        (a,b,c,d,e,datetime.datetime.now()))
        db.commit()
    except:
        print("Cos poszlo nie tak.")

def RemoveEntry():
    try:
        option=int(input('Wybierz:\n1.Stacja.\n2.Pomiar.\n'))
        if(option==1):
            id=int(input("Podaj ID stacji: "))
            sql="DELETE FROM Pomiary WHERE ID_stacji = '%d'" % (id)
            cursor.execute(sql)
            db.commit()
            sql="DELETE FROM Stacje WHERE ID= '%d'" % (id)
            cursor.execute(sql)
            db.commit()

        elif(option==2):
            id=int(input("Podaj ID stacji: "))
            TimeD=int(input("Podaj dzien pomiaru: "))
            TimeH=int(input("Podaj godzine pomiaru: "))
            TimeM=int(input("Podaj minute pomiaru:"))
            TimeMo=datetime.date.today().month
            TimeY=datetime.date.today().year
            time1=datetime.datetime(TimeY,TimeMo,TimeD,TimeH,TimeM,0,0)
            time2=datetime.datetime(TimeY,TimeMo,TimeD,TimeH,TimeM,59,999999)
            cursor.execute(f'''
            DELETE FROM Pomiary WHERE ID_stacji=? AND Czas_Pomiaru >= ? AND Czas_Pomiaru < ?''',
            (id,time1,time2))
            db.commit()
    except:
        print("Cos poszlo nie tak.")


def ChangeEntry():
    try:
        id=int(input("Podaj ID stacji: "))
        TimeD=int(input("Podaj dzien pomiaru: "))
        TimeH=int(input("Podaj godzine pomiaru: "))
        TimeM=int(input("Podaj minute pomiaru:"))
        TimeMo=datetime.date.today().month
        TimeY=datetime.date.today().year
        time1=datetime.datetime(TimeY,TimeMo,TimeD,TimeH,TimeM,0,0)
        time2=datetime.datetime(TimeY,TimeMo,TimeD,TimeH,TimeM,59,999999)
        b=float(input("Temperatura: "))
        c=float(input("Wiatr: "))
        d=float(input("Cisnienie: "))
        e=float(input("Wilgotnosc: "))
        cursor.execute(f'''
        UPDATE Pomiary SET Temperatura = ?, Wiatr = ?, Cisnienie = ?, Wilgotnosc = ?
        WHERE ID_stacji=? AND Czas_Pomiaru >= ? AND Czas_Pomiaru < ?''',
        (b,c,d,e,id,time1,time2))
        db.commit()
    except:
        print("Cos poszlo nie tak.")

def Losuj():
        option=int(input('Wybierz:\n1.Stacje.\n2.Pomiary.\n'))
        if(option==1):
            ilosc=int(input("Ile stacji?: "))
            ocean=0
            for i in range(ilosc):
                while True:
                    a=random.randint(1,1000)
                    b=str(random.uniform(-90,90))
                    c=str(random.uniform(-180,180))
                    print(b)
                    print(c)
                    d=""
                    e=""
                    location = geolocator.reverse(b+","+c,language='en')
                    try:
                        address = location.raw['address']
                    except:
                        continue
                    if "country" in address:
                        d=address["country"]
                    else:
                        ocean=ocean+1
                    if ocean<(ilosc/4) or d!="":
                        break
                if "town" in address:
                    e=address["town"]
                elif "city" in address:
                    e=address["city"]
                b=float(b)
                c=float(c)
                try:
                    cursor.execute(f'''
                    INSERT INTO Stacje(ID,Szerokosc,Dlugosc,Kraj,Miasto)
                    VALUES(?,?,?,?,?)''',
                    (a,b,c,d,e))
                    db.commit()
                except:
                    i=i-1
        elif(option==2):
            id=int(input("Wybierz stacje: "))
            A=random.randint(10,30)
            O=random.randint(1,10)
            for i in range(144):
                b=(A*math.sin(math.pi*i/144)+O)
                c=random.normalvariate(0,10)
                d=random.normalvariate(1000,20)
                e=random.uniform(40,60)
                time=datetime.datetime.now()
                f=time.replace(minute=int(((0+10*i)%60)),hour=int(10*i/60))
                try:
                    cursor.execute(f'''
                    INSERT INTO Pomiary(ID_stacji,Temperatura,Wiatr,Cisnienie,Wilgotnosc,Czas_Pomiaru)
                    VALUES(?,?,?,?,?,?)''',
                    (id,b,c,d,e,f))
                    db.commit()
                except:
                    i=i-1





def DeleteAll():
    try:
        cursor.execute('''
        DROP TABLE Pomiary;
        ''')
        cursor.execute('''
        DROP TABLE Stacje;
        ''')
        db.commit()  
    except:
        print("Cos poszlo nie tak.")




while(True):
    option=int(input('Wybierz:\n1.Dodaj stacje.\n2.Dodaj pomiar ze stacji.\n3.Usun.\n4.Zmien pomiar.\n5.Losuj.\n6.Usun wszystko.\n7.Zapisz do CSV\n8.Wyjdz.\n'))
    if(option==1):
        AddEntryStacja()
    elif(option==2):
        AddEntryPomiar()
    elif(option==3):
        RemoveEntry()
    elif(option==4):
        ChangeEntry()
    elif(option==5):
        Losuj()
    elif(option==6):
        DeleteAll()
    elif(option==7):
        clients=pd.read_sql('SELECT * FROM Stacje',db)
        clients.to_csv('stacje.csv',index=False)
        clients=pd.read_sql('SELECT * FROM Pomiary',db)
        clients.to_csv('pomiary.csv',index=False)
    elif(option==8):
        cursor.close()
        db.close()
        exit()

