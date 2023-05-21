from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
import pymongo
expression = ""

con='mongodb://localhost:27017'

from pymongo import MongoClient
  
try:
    client = MongoClient(con)
except:
    print("Could not connect to MongoDB")
mydb = client["database"]
mycol = mydb["student"]



root=Tk()
root.geometry('400x350')
root.title("Student Details")

def add_course(): # new window definition
    def add_query():
        global root
        mydict = { "name": E1.get(), "id": E2.get() }
        x = mycol.insert_one(mydict)
        add.config(state=NORMAL)
        update.config(state=NORMAL)
        show.config(state=NORMAL)
        delete.config(state=NORMAL)
        newwin.destroy()
    newwin = Toplevel(root)
    newwin.geometry('400x350')
    add.config(state=DISABLED)
    newwin.title("Add New Student")
    L1 = Label(newwin, text="Student Name")
    L1.place(x=10,y=50)
    E1 = Entry(newwin, bd=5)
    E1.place(x=110,y=50)
    L2 = Label(newwin, text="Student Id")
    L2.place(x=10,y=100)
    E2 = Entry(newwin, bd=5)
    E2.place(x=100,y=100)
    sub=Button(newwin,text="Add",command=add_query)
    sub.place(x=120,y=250)

def update_data(): # new window definition
    def UPDD():
        global root
        myquery = { "id": E1.get() }
        newvalues = { "$set": { "name": E2.get()} }
        x = mycol.update_one(myquery, newvalues)
        add.config(state=NORMAL)
        newwin.destroy()

    newwin = Toplevel(root)
    newwin.geometry('400x350')
    newwin.title("Update Student")
    add.config(state=NORMAL)

    L1 = Label(newwin, text="Student id")
    L1.place(x=10,y=50)
    E1 = Entry(newwin, bd=5)
    E1.place(x=110,y=50)

    L2 = Label(newwin, text="Student Name")
    L2.place(x=10,y=100)
    E2 = Entry(newwin, bd=5)
    E2.place(x=100,y=100)


    sub=Button(newwin,text="Update",command=UPDD)
    sub.place(x=120,y=200)


def del_data():
    def delete():
        global root
        myquery = { "id": E1.get() }
        x = mycol.delete_one(myquery)
        add.config(state=NORMAL)
        newwin.destroy()

    newwin=Toplevel(root)
    newwin.geometry('400x350')
    newwin.title("Delete Student")
    add.config(state=NORMAL)
    L1 = Label(newwin, text="Student Id")
    L1.place(x=10, y=50)
    E1 = Entry(newwin,bd=5)
    E1.place(x=110, y=50)
    sub = Button(newwin, text="Delete Student", command=delete)
    sub.place(x=120, y=200)


def display():
    newwin=Toplevel(root)
    newwin.geometry('400x350')
    newwin.title("Student Details")

    L1=Label(newwin,text="Student Name")
    L1.grid(row=0,column=0)
    L2 = Label(newwin, text="Id")
    L2.grid(row=0, column=1)

    i=1
    for row in mycol.find():
        L1 = Label(newwin, text=row["name"])
        L1.grid(row=i, column=0)
        L2 = Label(newwin, text=row["id"])
        L2.grid(row=i, column=1)
        i+=1


add= Button(root,text='Add New Student',command=add_course)
delete= Button(root,text='Delete Student',command=del_data)
update= Button(root,text='Update Student Details',command=update_data)
show= Button(root,text='Show Student Details',command=display)
add.place(x=50,y=50)
delete.place(x=50,y=100)
update.place(x=200,y=50)
show.place(x=200,y=100)

root.mainloop()