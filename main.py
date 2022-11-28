#imports
import sys
import pymysql
import matplotlib.pyplot as plt

#definitions
con=pymysql.connect(host="localhost",user="root", passwd="Shanjiv#1707")
cursor=con.cursor()

#functions
def graphfva():
    query="SELECT * from passengers"
    cursor.execute(query)
    data_p=cursor.fetchall()
    
    dict={}
    for i in data_p:
        dict[i[3]]=0
    for i in data_p:
        dict[i[3]] += 1

    x=list(dict.keys())
    y=list(dict.values())
    plt.bar(x,y)
    plt.xticks(range(0,101,10))
    plt.show()

def graphfvp():
    query="SELECT * from passengers"
    cursor.execute(query)
    data_p=cursor.fetchall()
    
    query="SELECT * from flights"
    cursor.execute(query)
    data_f=cursor.fetchall()
    dict={}
    for i in data_f:
        dict[i[1]]=0
    for i in data_p:
        fid=i[2]
        for j in data_f:
            if j[0]==fid:
                dict[j[1]] += 1

    x=list(dict.keys())
    y=list(dict.values())
    plt.bar(x,y)
    plt.show()

def graphmvf():
    query="SELECT * from passengers"
    cursor.execute(query)
    data_p=cursor.fetchall()
    male=0
    female=0
    ns=0
    for i in data_p:
        gen=i[5]
        if gen=='M':
            male += 1
        elif gen == 'F':
            female += 1
        else:
            ns += 1
    x=["Male", "Female", "Not Specified"]
    y=[male, female, ns]
    plt.bar(x,y)
    plt.show()

def delete(id):
    if ifexists(id):
        cursor.execute(f"DELETE FROM passengers WHERE ID={id}")
        con.commit()
    else:
        print("INVALID PASSENGER ID")
            
def update(id):
    if ifexists(id):
        print("You can change the following details of a passenger:\n 1. Name \n 2. Age \n3. Mobile Number \n4. Flight ID \n5. Gender\n")
        ch=int(input("Which Data would you like to change?(Enter the corresponding number given above):"))
        if ch==1:
            name=input("Enter Name:")
            cursor.execute(f"UPDATE passengers set Name='{name}' WHERE ID={id}")
            con.commit()
        elif ch==2:
            age=int(input("Enter Age:"))
            cursor.execute(f"UPDATE passengers set Age={age} WHERE ID={id}")
            con.commit()
        elif ch==3:
            Mob=int(input("Enter Mobile Number:"))
            if Mob/999999999<1:
                print("ENTER VALID MOBILE NUMBER")
                sys.exit()
            else:
                pass
            cursor.execute(f"UPDATE passengers set Mobile_Number={Mob} WHERE ID={id}")
            con.commit()
        elif ch==4:
            cursor.execute("SELECT * FROM places")
            starts=cursor.fetchall()
            print("(ID, Start Place")
            for i in starts:
                print(i)
            start=input("Enter Start ID from the above table:")

            cursor.execute("SELECT * FROM places")
            dests=cursor.fetchall()
            print("(ID, Destination Place")
            for i in dests:
                print(i)
            dest=input("Enter Destination ID from the above table:")

            cursor.execute(f"SELECT count(*) FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
            flightCount=int(cursor.fetchall()[0][0])
            if flightCount > 0:
                cursor.execute(f"SELECT * FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
                flights=cursor.fetchall()
                for i in flights:
                    print(i)
                fid = int(input("Enter the Flight ID from the above table:"))
            else:
                print("No Flights Available")
                sys.exit()

            cursor.execute(f"UPDATE passengers set Flight_ID={fid} WHERE ID={id}")
            con.commit()
        elif ch==5:
            gnd=input("Select your Gender\n M for Male\n F for Female\n P if you prefer not to say\n :")
            if gnd=='M':
                pass
            elif gnd=='F':
                pass
            elif gnd == 'P':
                pass
            else:
                print("INVALID ENTRY")

            cursor.execute(f"UPDATE passengers set Gender='{gnd}' where ID={id}")
            con.commit()
        else:
            print("Invalid Entry")
    else:
        print("INVALID PASSENGER ID")

def search(id):
    if ifexists(id):
        cursor.execute(f"SELECT * FROM passengers WHERE ID={id}")
        store=cursor.fetchall()[0]
        print(f"\tPassenger Name: {store[1]}")
        cursor.execute(f"SELECT * FROM flights WHERE Flight_ID={store[2]}")
        store1=cursor.fetchall()[0]
        print(f"\tAirline Name: {store1[1]}")
        cursor.execute(f"SELECT * FROM places WHERE PLACE_ID={store1[2]}")
        store2=cursor.fetchall()[0]
        print(f"\tStart: {store2[1]}")
        cursor.execute(f"SELECT * FROM places WHERE PLACE_ID={store1[3]}")
        store3=cursor.fetchall()[0]
        print(f"\tDestination: {store3[1]}")
        print(f"\tAge: {store[3]}")
        print(f"\tMobile Number: {store[4]}")
        if store[5]=='M':
            gender='Male'
        elif store[5]=='F':
            gender="Female"
        else:
            gender="Not Specified"

        print(f"\tGender: {gender}")
    else:
        print("INVALID PASSENGER")

def addnewp():
    name = input("Enter Passenger Name:")

    cursor.execute("SELECT * FROM places")
    starts = cursor.fetchall()
    print("(ID, Start Place)")
    for i in starts:
        print(i)
    start = input("Enter Start ID from the above table:")

    cursor.execute("SELECT * FROM places")
    dests = cursor.fetchall()
    print("(ID, Destination Place)")
    for i in dests:
        print(i)
    dest = input("Enter Destination ID from the above table:")

    cursor.execute(
        f"SELECT count(*) FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
    flightCount = int(cursor.fetchall()[0][0])
    if flightCount > 0:
        cursor.execute(f"SELECT * FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
        flights=cursor.fetchall()
        print("(Flight ID, Airline Name, Destination, Start, Time of Flight in mins)")
        for i in flights:
            print(i)
        fid = int(input("Enter the Flight ID from the above table:"))
    else:
        print("No Flights Available")
        sys.exit()
    age = int(input("Enter your age:"))
    mob = int(input("Enter your mobile number:"))
    if mob/999999999<1:
        print("ENTER VALID MOBILE NUMBER")
        sys.exit()
    else:
        pass
    gnd = input("Select your Gender\n M for Male\n F for Female\n P if you prefer not to say\n :")
    if gnd == 'M':
        pass
    elif gnd == 'F':
        pass
    elif gnd == 'P':
        pass
    else:
        print("INVALID ENTRY")
        sys.exit()
    cursor.execute(f"INSERT INTO passengers(Name, Flight_ID,Age, Mobile_Number, Gender) values('{name}',{fid},{age},{mob},'{gnd}')")
    con.commit()
    cursor.execute(f"SELECT * FROM passengers WHERE Name='{name}'")

    pid = int(cursor.fetchone()[0])
    print(f"Your Passenger ID is {pid}")

def addnewf():
    aname = input("Enter Airline Name:")
    cursor.execute("SELECT * FROM places")
    starts = cursor.fetchall()
    print("(ID, Start Place)")
    for i in starts:
        print(i)
    start = input("Enter Start ID from the above table:")

    cursor.execute("SELECT * FROM places")
    dests = cursor.fetchall()
    print("(ID, Destination Place)")
    for i in dests:
        print(i)
    dest = input("Enter Destination ID from the above table:")
    tof = int(input("Enter Time of Flight:"))
    cursor.execute(f"INSERT INTO flights(Airline_Name, Start_ID, Destination_ID, Time_Of_Flight_mins) values('{aname}', '{start}', '{dest}',{tof})")
    con.commit()

def choices(choice):
    ch=choice
    if ch == 1:
        addnewp()
    elif ch == 2:
        id = int(input("Enter Passenger ID:"))
        print()
        search(id)
        print()
    elif ch == 3:
        id = int(input("Enter Passenger ID:"))
        update(id)
    elif ch == 4:
        id = int(input("Enter Passenger ID:"))
        delete(id)
    elif ch == 5:
        print("Which graph do you want to see?")
        print("1. Graph between Male and Female flyers")
        print("2. Graph between Flyers and Flights")
        print("3. Graph between Flyers and Age")
        choi = int(input(":"))
        if choi == 1:
            graphmvf()
        elif choi == 2:
            graphfvp()
        elif choi == 3:
            graphfva()
        else:
            print("INVALID CHOICE")
            sys.exit()

    elif ch == 6:
        placename = input("Enter Place Name:")
        cursor.execute(f"INSERT INTO places(Place) values('{placename}')")
        con.commit()
    elif ch == 7:
        addnewf()
    elif ch == 8:
        sys.exit()
    else:
        print("Invalid Input")

def ifexists(id):
    cursor.execute(f"SELECT count(*) FROM passengers WHERE ID={id}")
    store=int(cursor.fetchall()[0][0])
    if store>0:
        return True
    else:
        return False

#main
def main():
    print("Welcome Airline Management System!")
    print()

    cursor.execute("CREATE DATABASE IF NOT EXISTS AIRLINE_MANAGEMENT_SYSTEM")
    con.commit()

    cursor.execute("USE AIRLINE_MANAGEMENT_SYSTEM")
    con.commit()
    #con=pms.connect(host="localhost",user="root", passwd="Shanjiv#1707", database="test3")
    cursor.execute("CREATE TABLE IF NOT EXISTS passengers(ID int AUTO_INCREMENT PRIMARY KEY, Name varchar(20),Flight_ID int REFERENCES flights.Flight_ID, Age INT, Mobile_Number int(10), Gender varchar(1))")
    con.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS flights(Flight_ID int AUTO_INCREMENT PRIMARY KEY, Airline_Name varchar(20), Start_ID int REFERENCES start.start_ID, Destination_ID int REFERENCES destination.Destination_ID, Time_Of_Flight_mins int)")
    con.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS places(Place_ID int AUTO_INCREMENT PRIMARY KEY, Place varchar(20))")
    con.commit()
    #functions
    while True:
        print("What do you want to do? (Type the number corresponding the action you wish to perform)")
        print("1. New Booking")
        print("2. View Passenger Information")
        print("3. Update Passenger Details")
        print("4. Delete Passenger Data")
        print("5. Get Visual Passenger Information")
        print("6. Add new Place")
        print("7. Add new flight")
        print("8. Exit")


        # Storing Passenger Choice as ch
        ch = int(input("Please enter here: "))
        choices(ch)

main()
