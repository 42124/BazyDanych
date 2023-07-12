import simplejson
import psycopg
import datetime
import matplotlib.pyplot as plt

with open("dane_log.json") as db_con_file:
    creds=simplejson.loads(db_con_file.read())
conn = psycopg.connect(
    host=creds['host_name'],
    user=creds['user_name'],
    dbname=creds['db_name'],
    password=creds['password'],
    port=creds['port_number']
)
cursor=conn.cursor()

def WyswietlDane():
    try:
        id=int(input("Podaj ID stacji: "))
        option=int(input('Wybierz:\n1.Temperatura.\n2.Wiatr.\n3.Cisnienie.\n4.Wilgotnosc.\n'))
        wybor=["Temperatura","Wiatr","Cisnienie","Wilgotnosc"]
        query = f"SELECT {wybor[option-1]}, Czas_Pomiaru FROM POMIARY WHERE ID_Stacji = %s"
        cursor.execute(query, (id,))
        dane = cursor.fetchall()
        values = [row[0] for row in dane]
        timestamps = [datetime.datetime.combine(datetime.date.today(), row[1]) for row in dane]
    
        if(option==1):
            plt.figure(figsize=(20,20))
            plt.plot(timestamps, values)
            plt.xlabel("Czas pomiaru")
            plt.ylabel(wybor[option-1])
            plt.title("Wykres")
        else:
            plt.hist(values,10)
            plt.show()
    except:
        print("Cos poszło nie tak")
                     
    
    
    
def ZnajdzMax():
    try:
        option=int(input('Wybierz:\n1.Temperatura.\n2.Wiatr.\n3.Cisnienie.\n4.Wilgotnosc.\n'))
        wybor=["Temperatura","Wiatr","Cisnienie","Wilgotnosc"]
        kraj=input("Kraj?")
        query = f"SELECT * FROM Pomiary WHERE "
        if(kraj!=""):
            query2=f"SELECT * FROM Stacje WHERE KRAJ = %s"
            cursor.execute(query2,(kraj,))
            dane = cursor.fetchall()
            ids = [row[0] for row in dane]
            query = query+f"Id_Stacji IN("+','.join(map(str, ids)) + ") AND"
        query = query+f"({wybor[option-1]}) =(SELECT MAX({wybor[option-1]}) FROM Pomiary WHERE Id_Stacji IN("+','.join(map(str, ids)) + ") )"
        cursor.execute(query)
        dane = cursor.fetchall()
        print(dane)
        query = f"SELECT * FROM Stacje WHERE ID = ({dane[0][0]})"
        cursor.execute(query)
        dane = cursor.fetchall()
        print(dane)
    except:
        print("Cos poszło nie tak")
    

def ZnajdzMin():
    try:
        option=int(input('Wybierz:\n1.Temperatura.\n2.Wiatr.\n3.Cisnienie.\n4.Wilgotnosc.\n'))
        wybor=["Temperatura","Wiatr","Cisnienie","Wilgotnosc"]
        query = f"SELECT * FROM Pomiary WHERE ({wybor[option-1]}) = (SELECT MIN({wybor[option-1]}) FROM Pomiary)"
        cursor.execute(query)
        dane = cursor.fetchall()
        print(dane)
        query = f"SELECT * FROM Stacje WHERE ID = ({dane[0][0]})"
        cursor.execute(query)
        dane = cursor.fetchall()
        print(dane)
    except:
        print("Cos poszło nie tak")
    
def Ile():
    try:
        option=int(input('Wybierz:\n1.Stacje.\n2.Pomiary ze stacji.\n'))
        if(option==1):
            query=f"SELECT COUNT(*) FROM Stacje"
            cursor.execute(query)
            dane = cursor.fetchall()
            print("Stacji pomiarowych jest: "+str(dane[0][0]))
        elif(option==2):
            id=int(input("Podaj ID stacji"))
            query=f"SELECT COUNT(*) FROM Pomiary WHERE ID_Stacji = ({id})"   
            cursor.execute(query)
            dane = cursor.fetchall()
            print("Pomiarów ze stacji "+str(id) +" jest " +str(dane[0][0]))
    except:
        print("Cos poszło nie tak")

def ZKraju():
    try:
        kraj=input("Kraj?")
        query=f"SELECT * FROM Stacje WHERE KRAJ = %s"
        cursor.execute(query,(kraj,))
        dane = cursor.fetchall()
        ids = [row[0] for row in dane]
        print("ID stacji w " +kraj +" to:")
        print(ids)
    except:
        print("Coś poszło nie tak")
    
while(True):
    option=int(input('Wybierz:\n1.Wyswietl dane.\n2.Znajdz maksmimum.\n3.Znajdz minimum.\n4.Sprawdź ile.\n5.Z kraju.\n6.Wyjdź.\n'))
    if(option==1):
        WyswietlDane()
    elif(option==2):
        ZnajdzMax()
    elif(option==3):
        ZnajdzMin()
    elif(option==4):
        Ile()
    elif(option==5):
        ZKraju()
    elif(option==6):
        cursor.close()
        conn.close()
        exit()
       
