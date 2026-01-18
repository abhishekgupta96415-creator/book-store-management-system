import random
import mysql.connector
from config import DB_CONFIG

DB = mysql.connector.connect(**DB_CONFIG)
C = DB.cursor()

def ADD():
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    publisher = input("Enter Publisher: ")
    price = float(input("Enter Price: "))
    qty = int(input("Enter qty: "))
    no=random.randint(100, 10000)
    C.execute("INSERT INTO stock values('{}','{}','{}','{}','{}','{}')".format(no,title,author,publisher,price,qty))
    DB.commit()
    print("BOOK  ADDEDD SUCCESSFULLY !!")
 
def NewStaff():
    fname=str(input("Enter Fullname:--"))
    gender=str(input("Gender(M/F/O):---"))
    age=int(input("Age:---"))
    phno=int(input("Staff phone no.:--"))
    add=str(input("Address:---"))
    no=random.randint(100, 10000)
    C.execute(("INSERT INTO staff values('{}','{}','{}','{}','{}','{}')".format(no,fname,age,gender,phno,add)))
    DB.commit()
    print("STAFF IS SUCCESSFULLY ADDED")

def RemoveStaff():
    n=(input("Staff Name to Remove:-- "))
    C.execute("DELETE FROM staff WHERE Name=('{}') ".format(n)) 
    DB.commit()
    print("Above Employee is  deleted")
   
def StaffDetailfS():
    print("=="*60+"\tStaff List\t"=="+"*60)
    spl_statement= "Select * from staff"
    C.execute(spl_statement)
    output =C.fetchall()
    for x in output:
        printrow(x)
       
def AvailablefU():
    print("=="*60+"\tAvailable BOOK Stock\t"=="+"*60)
    query="select * from stock"
    C.execute(query)
    data=C.fetchall()
    for row in data:
        printrow(row)
                    
def Purchase():
    AvailablefU()
    phno=input("Enter Customer phone number:")
    C.execute("select cust_no from customer where cust_no='"+phno+"'")
    k=C.fetchone()
    query_billing_details=[]
    query_update_stock=[]
    total_amt=0
    confirm_to_bill='N'
    ex=0

    if k:
        print("Customer Already Registered, Data Found")
        no=random.randint(0, 10000)
        C.execute("INSERT INTO billing values('{}','{}')".format(no,phno))
        DB.commit()
        print("Bill Number Gened Successfully !!")
        
        while True:
            print("Current Billing Amount:- ",total_amt)
            bookno=int(input("Enter BOOK Number:- "))
            qty=int(input("Enter quantity:-"))
            qry="select price from stock where book_no="+str(bookno)+" and qty>="+str(qty)+";"
            C.execute(qry)
            sale_id=random.randint(0, 100000)

            if C!=None:
                print("BOOK Found")
                data=C.fetchone()
                total_amt=data[0]*qty+total_amt
                query_billing_details.append("INSERT INTO billing_details values('{}','{}','{}','{}','{}')".format(sale_id,bookno,no,data[0],qty))
                sale_id=sale_id+1
                query_update_stock.append("update stock set qty=qty-"+str(qty)+" where book_no="+str(bookno)+";")
                print("Data Added to Bill")
                ch=input("Do You Want To add More Items To Your Cart ? (Y/N):-")
                if ch in ['y','Y']:
                    continue
                else:
                    ex=1
                    break
                
            else:
                print("Either book not in database or check qty")
        
        if ex==1:
            for command in query_update_stock:
                C.execute(command)
                DB.commit()                
            for command in query_billing_details:
                C.execute(command)
                DB.commit()
                print("Data Billed! Bill No:-",no )
                printbill(no)
    else:
        print("New Customer, Please Provide The Following Data: -")
        customerentry()
        print("Initiate Purchse Operation Again !")
        
def printbill(n):
    print("Printing Bill for the Bill Number:-")
    C.execute("select book_no,price,qty,price*qty as 'Total' from billing_details where bill_no in(select bill_no cust_no from billing where bill_no="+str(n)+");")
    for row in C:
        printrow(row)
    print("Total Billing Amount:- ",end='')
    C.execute("select sum(price*qty) as 'Total' from billing_details where bill_no in(select bill_no cust_no from billing where bill_no="+str(n)+");")
    for row in C:
        printrow(row)
def UsingName():
    o=input("Enter Title of BOOK to search:")
    C.execute("select title from stock where title='"+o+"'")
    t=C.fetchone()
    if t != None:
        print("Match Found! ")
        C.execute("select * from stock where title='"+o+"'")
        data=C.fetchall()
        for row in data:
            printrow(row)
    else:
        print("Book by title "+o+" Not Found!, verify title")
       
def Usingauthor():
     g=input("Enter author to search:")
     C.execute("select author from stock where author= '"+g+"'")
     poll=C.fetchall()
     if poll != None:
         print("Match Found ! ")
         C.execute("select * from stock where author='"+g+"'")
         data=C.fetchall()
         for y in data:
             printrow(y)
     else:
         print("Book by "+g+" are not Available!, Verify Author")
        
def Usingpublisher():
     g=input("Enter Publisher Name to search:")
     query="select * from stock where publisher like '"+g+"%'"
     C.execute(query)
     poll=C.fetchone()
     if poll != None:
         print("Match Found ! ")
         query="select * from stock where publisher like'"+g+"%'"
         C.execute(query) 
         for y in C:
             printrow(y)
     else:
         print("Book by publisher  "+g+" are not Available!, Verify publisher Name")
def printrow(row):
    i=len(row)
    for j in range (0,i,1):
        print("\t",row[j],end="")
    print()

def mainmenu():
    
    print("~"*30+"\tWELCOME TO BOOK STORE \t"+"~"*30)
    print (" enter 1 for BOOK Operations :-->")
    print (" enter 2 for staff operation :-->")
    print (" enter 3 for selling operation :-->")
    print (" enter 4 for Customer operation :-->")
    print (" enter other to exit :-->")
    a=int(input("Enter your choice  :--> "))
    return a
    
def bookmenu():
    print("+"*30+"\tWelcome To book Operations\t"+"+"*30)
    print (" 1 for New book Addition to database")
    print (" 2 for To Display All books")
    print (" 3 for To Search book")
    print (" 4 for To Sell A book")
    print (" Other  for exit")
    try:
        b=int(input("Enter your choice  :--> "))
        return b
    except ValueError:
        print("Input Error ") 
    
def booksearch():
    print("^"*30+"\tWelcome To book Search Operations\t"+"^"*30)
    print (" 1 for Search by name ")
    print (" 2 for Search by author ")
    print (" 3 for Search by publisher")
    print (" Any Other To Exit From Book Search Operations")
    try:
        c=int(input("Enter your choice  :--> "))
        return c
    except ValueError:
        print("Input Error ")  
           
    
def staffmenu():
    print("^"*30+"\tWelcome To Staff Operations\t"+"^"*30)
    print (" 1 for add new staff")
    print (" 2 for remove staff")
    print (" 3 for staff details")
    print (" other to exit staff operation")
    d=int(input("Enter your choice :--> "))
    return d      
    
def salesmenu():
    print("+"*30+"\tWelcome To Sales Operations\t"+"+"*30)
    print(" 1 for Billing")
    print(" 2 for  Printing A Bill")
    print (" other to exit selling operation ")
    e=int(input(" enter your choice  :-->"))
    return e

def custmenu():
    print(" 1 for Insertion Customer record")
    print(" 2 for  Display Customer record")
    e=int(input(" enter your choice  :-->"))
    return e

def customerentry():
    name=str(input("Enter Customer Name:- "))
    no=int(input("Enter Contact Number:-")) 
    address=input("Enter Address:-")
    C.execute("INSERT INTO customer values('{}','{}','{}')".format(no,name,address))
    DB.commit()
    print("Customer Added successfully !!")
    
def customerdisplay():
    print("+"*60+"\tCustomer List\t"+"+"*60)
    spl_statement= "Select * from Customer"
    C.execute(spl_statement)
    output =C.fetchall()
    for x in output:
        printrow(x)

while True:
    mch=mainmenu()
    if mch==1:#enter 1 for book operation
        while True:
            boperation=bookmenu()#Displaying Main Menu
            if boperation==1:
                print("Add New book")
                ADD()# Inserting New book Into the Database
            elif boperation==2:
                AvailablefU()#Show Stock    
            elif boperation==3:
                while True:
                    bsearch=booksearch()#Displaying Search Menu
                    if bsearch==1:
                        print("Search By Name")
                        UsingName()
                    elif bsearch==2:
                        print("Search By author")
                        Usingauthor()
                    elif bsearch==3:
                        print("Search By publisher")
                        Usingpublisher()
                    else:
                        print("Exiting From book Search Operations, Thank You !")
                        break
            elif boperation==4:
                Purchase()
            else:
                print("Exiting from book Operations, Thank You !")
                break
    elif mch==2:#enter 2 for staff operation
        print("Staff Operation")
        while True:
            staffchoice=staffmenu()
            if staffchoice==1:
                print("\t Add New Staff   ")
                NewStaff()

            elif staffchoice==2:
                print("Staff Removal")
                RemoveStaff()    

            elif staffchoice==3:
                print("Staff Display")
                StaffDetailfS()

            else:
                print("Exiting from staff Operations, Thank You!")
                break
        
    elif mch==3:#enter 3 for selling operation
        while True:
            print("Sell Operation")
            op=salesmenu()
            if op==1:
                Purchase()
            elif op==2:
                n=int(input("Enter Billno:-"))
                printbill(n)
            else:
                print("Exiting from Sales Operations, Thank You!")
                break
                
    elif mch==4:
        while True:
            custchoice=custmenu()
            if custchoice==1:
                customerentry()
            elif custchoice==2:
                customerdisplay()
            else:
                print("Exiting From Customer Operations, Thank You !")
                break
                
    else:
        print("Exiting from BOOK Main Menu, Program Will Now Terminate, Thank You !")                
        break
