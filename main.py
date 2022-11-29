

#importing all neccessary libraries
import sys
import pymysql
import matplotlib.pyplot as plt

print("\n\t\t\tWelcome to Airline Management System!")
try:
    #function to ask the user for database login credentials
    #this function had to be called first as this initializes the code by setting up the sql cursor
    def ask():
        print("Please enter SQL details to login")
        uname=input("Enter Username:")
        passwd=input("Enter Password:")
        return uname,passwd

    #initializing a check variable
    connected=False

    #Connecting to the SQL Database with error handling
    try:
        con=pymysql.connect(host="localhost",user="root", passwd="manager")
        cursor=con.cursor()
    except pymysql.err.OperationalError:
        connected=False
        while connected==False:
            dat=ask()
            try:
                con=pymysql.connect(host="localhost",user=f"{dat[0]}", passwd=f"{dat[1]}")
                cursor=con.cursor()
            except pymysql.err.OperationalError:
                connected=False
            else:
                connected=True

            if connected==True:   
                if cursor.connection:
                    connected=True
                    print("\tDatabase Connection Successful!")
                else:
                    print("\tDatabase connection Unsuccesful!")
            else:
                pass
    else:
        print("\tDataBase Connection Successful!")

    #functions

    #shows flights that are available a function to show start and destination is called by this function internally
    def showflights():
        places=showstndest()
        start=places[0]
        dest=places[1]
        cursor.execute(f"SELECT count(*) FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
        flightCount=int(cursor.fetchall()[0][0])
        if flightCount > 0:
            cursor.execute(f"SELECT * FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
            flights=cursor.fetchall()
            for i in flights:
                print(i)
            while True:
                try:
                    fid = int(input("Enter the Flight ID from the above table:"))
                except ValueError:
                    print("Enter VALID Option")
                else:
                    break
        else:
            print("No Flights Available")
            sys.exit()
        return fid

    #shows start and destinations places that are in service
    def showstndest():
        cursor.execute("SELECT * FROM places")
        places = cursor.fetchall()
        nofplaces=len(places)
        if nofplaces>0:
            print("(ID, Start Place)")
            for i in places:
                print(i)
            while True:
                try:
                    start = int(input("Enter Start ID from the above table:"))
                except ValueError:
                    print("Enter Valid Option")
                else:
                    if start>nofplaces:
                        print("Enter Option from Above list")
                        for i in places:
                            print(i)
                        try:
                            start = int(input("Enter Start ID from the above table:"))
                        except ValueError:
                            print("Enter Valid Option")
                        else:
                            break
                    else:
                        break

            print("(ID, Destination Place)")
            for i in places:
                print(i)
            while True:
                try:
                    dest = int(input("Enter Destination ID from the above table:"))
                except ValueError:
                    print("Enter Valid Option")
                else:
                    if dest>nofplaces:
                        print("Enter Option from Above list")
                        for i in places:
                            print(i)
                        try:
                            start = int(input("Enter Destination ID from the above table:"))
                        except ValueError:
                            print("Enter Valid Option")
                        else:
                            break
                    else:
                        break
        else:
            print("No places under service")
            
        return start,dest

    #asks a user for a their mobile number, had to seperate it because of recursion
    def askmob():
        while True:
            try:
                Mob=int(input("Enter Mobile Number:"))
            except ValueError:
                print("Enter VALID Details or enter Ctrl+C to exit the program")
            else:
                break

        return Mob

    #shows the graph of number of flyers versus their age
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

    #shows the graph of number of flyers versus their airline
    def graphfval():
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

    #shows the graph of number of male versus female flyers
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

    #function to delete a passenger
    def delete(id):
        if ifexists(id):
            cursor.execute(f"DELETE FROM passengers WHERE ID={id}")
            con.commit()
        else:
            print("INVALID PASSENGER ID")

    #fucntion to update passenger details            
    def update(id):
        if ifexists(id):
            while True:
                try:
                    print("You can change the following details of a passenger:\n1. Name\n2. Age\n3. Mobile Number\n4.Flight ID\n5.Gender\n")
                    ch=int(input("Which Data would you like to change?(Enter the corresponding number given above):"))
                except ValueError:
                    print("Enter Valid input")
                else:
                    break
            if ch==1:
                name=input("Enter Name:")
                cursor.execute(f"UPDATE passengers set Name='{name}' WHERE ID={id}")
                con.commit()
            elif ch==2:
                while True:
                    try:
                        age=int(input("Enter Age:"))
                    except ValueError:
                        print("Enter VALID Details or enter Ctrl+C to exit the program")
                    else:
                        break

                cursor.execute(f"UPDATE passengers set Age={age} WHERE ID={id}")
                con.commit()
            elif ch==3:
                Mob=askmob()
                while True:
                    if Mob<=999999999 or Mob>=9999999999:
                        print("ENTER VALID MOBILE NUMBER")
                    else:
                        break
                cursor.execute(f"UPDATE passengers set Mobile_Number='{str(Mob)}' WHERE ID={id}")
                con.commit()
            elif ch==4:
                fid=showflights()

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

    #fucntion to search passenger details
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

    #function to add a new passenger
    def addnewp():
        name = input("Enter Passenger Name:")

        data1=showstndest()
        start=data1[0]
        dest=data1[1]
        cursor.execute(f"SELECT count(*) FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
        flightCount = int(cursor.fetchall()[0][0])
        if flightCount > 0:
            cursor.execute(f"SELECT * FROM flights WHERE start_ID={start} AND Destination_ID={dest}")
            flights=cursor.fetchall()
            print("(Flight ID, Airline Name, Destination, Start, Time of Flight in mins, Price in Rs.)")
            for i in flights:
                print(i)
            while True:
                try:
                    fid = int(input("Enter the Flight ID from the above table:"))
                except ValueError:
                    print("Enter VALID Option")
                else:
                    break
        else:
            print("No Flights Available")
            main()
            sys.exit()
        while True:
            try:
                age=int(input("Enter Age:"))
            except ValueError:
                print("Enter VALID Details or enter Ctrl+C to exit the program")
            else:
                break
        Mob=askmob()
        while True:
            if Mob<=999999999 or Mob>9999999999:
                print("ENTER VALID MOBILE NUMBER")
                Mob=askmob()
            else:
                break
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
        cursor.execute(f"INSERT INTO passengers(Name, Flight_ID,Age, Mobile_Number, Gender) values('{name}',{fid},{age},'{str(Mob)}','{gnd}')")
        con.commit()
        cursor.execute(f"SELECT * FROM passengers WHERE Name='{name}'")

        pid = int(cursor.fetchone()[0])
        print(f"\t\t\tYour Passenger ID is {pid}, PLEASE REMEMBER FOR FUTURE REFERENCES")

    #fucntion to add a new flight
    def addnewf():
        aname = input("Enter Airline Name:")
        places=showstndest()
        start=places[0]
        dest=places[1]    
        while True:
            try:
                tof = int(input("Enter Time of Flight (mins):"))
            except ValueError:
                print("Enter Valid time (in integers)")
            else:
                break
        while True:
            try:
                price = int(input("Enter Price(in Rs.):"))
            except ValueError:
                print("Enter Valid Price (in integers)")
            else:
                break
        cursor.execute(f"INSERT INTO flights(Airline_Name, Start_ID, Destination_ID, Time_Of_Flight_mins, Price) values('{aname}', '{start}', '{dest}',{tof}, {price})")
        con.commit()

    #fucntion to parse through the request requested by the user
    def choices(choice):
        ch=choice
        if ch == 1:
            addnewp()
        elif ch == 2:
            while True:
                try:
                    id=int(input("Enter Passenger ID:"))
                except ValueError:
                    print("ENTER VALID ID")
                else:
                    break
            print()
            search(id)
            print()
        elif ch == 3:
            while True:
                try:
                    id=int(input("Enter Passenger ID:"))
                except ValueError:
                    print("ENTER VALID ID")
                else:
                    break
            update(id)
        elif ch == 4:
            while True:
                try:
                    id=int(input("Enter Passenger ID:"))
                except ValueError:
                    print("ENTER VALID ID")
                else:
                    break
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
                graphfval()
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
            print("Program exit successful!")
            sys.exit()
        else:
            print("Invalid Input")

    #function to check if the passenger exists using their ID
    def ifexists(id):
        cursor.execute(f"SELECT count(*) FROM passengers WHERE ID={id}")
        store=int(cursor.fetchall()[0][0])
        if store>0:
            return True
        else:
            return False

    #the main function
    def main():
        print()

        cursor.execute("CREATE DATABASE IF NOT EXISTS AIRLINES_MANAGEMENT_SYSTEM")
        con.commit()

        cursor.execute("USE AIRLINES_MANAGEMENT_SYSTEM")
        con.commit()
        #con=pms.connect(host="localhost",user="root", passwd="Shanjiv#1707", database="test3")
        cursor.execute("CREATE TABLE IF NOT EXISTS passengers(ID int AUTO_INCREMENT PRIMARY KEY, Name varchar(20),Flight_ID int REFERENCES flights.Flight_ID, Age INT, Mobile_Number varchar(10), Gender varchar(1))")
        con.commit()
        cursor.execute("CREATE TABLE IF NOT EXISTS flights(Flight_ID int AUTO_INCREMENT PRIMARY KEY, Airline_Name varchar(20), Start_ID int REFERENCES start.start_ID, Destination_ID int REFERENCES destination.Destination_ID, Time_Of_Flight_mins int, Price int)")
        con.commit()
        cursor.execute("CREATE TABLE IF NOT EXISTS places(Place_ID int AUTO_INCREMENT PRIMARY KEY, Place varchar(20))")
        con.commit()

        cursor.execute("SELECT * FROM places")
        starts = cursor.fetchall()
        nofplaces1=len(starts)
        while nofplaces1<2:
            print("Add atleast two places to start the service")
            print(f"Current number of places added: {nofplaces1}")
            placename = input("Enter Place Name:")
            cursor.execute(f"INSERT INTO places(Place) values('{placename}')")
            con.commit()
            cursor.execute("SELECT * FROM places")
            starts = cursor.fetchall()
            nofplaces1=len(starts)


        wtp=True
        while wtp==True:
            print("\nWhat do you want to do? (Type the number corresponding the action you wish to perform)")
            print("1. New Booking")
            print("2. View Passenger Information")
            print("3. Update Passenger Details")
            print("4. Delete Passenger Data")
            print("5. Get Visual Passenger Information")
            print("6. Add new Place")
            print("7. Add new flight")
            print("8. Exit")


            # Storing Passenger Choice as ch
            while True:
                try:
                    ch = int(input("Please enter here: "))
                except ValueError:
                    print("\nWhat do you want to do? (Type the number corresponding the action you wish to perform)")
                    print("1. New Booking")
                    print("2. View Passenger Information")
                    print("3. Update Passenger Details")
                    print("4. Delete Passenger Data")
                    print("5. Get Visual Passenger Information")
                    print("6. Add new Place")
                    print("7. Add new flight")
                    print("8. Exit")
                    print("\nEnter a Valid Number corresponding to what you would wish to do from the above options")
                else:
                    break
                
            choices(ch)
            print("Do you want to do something else?")
            yon=input("Type Y for yes and any other key to exit:").lower()
            if yon=='y':
                wtp=True
            else:
                wtp=False
                print("\n\t\t\tProgram exit successful!")
                sys.exit()

    #handling KeyboardInterrupt
    main()
except KeyboardInterrupt:
    print("\n\t\t\tProgram exit successful!")