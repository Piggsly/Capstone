import tkinter as tk
from tkinter import *
from tkinter import messagebox
import hashlib
import sqlite3
import os
import popup

class MyGUI:

    def __init__(self):
    
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.configure(background='black')

        self.root.title("Locker")
        self.root.iconbitmap("Locker_icon.ico")

        self.login_Screen()

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def create_Screen(self): ##create a profile
        self.forget()
        self.root.unbind("<KeyPress>") ##unbinding from login screen

        self.lbl1 = tk.Label(self.root, text="Username", bg="black", fg="white")
        self.lbl1.grid(row=0, column=0)

        self.user = tk.Entry(self.root)
        self.user.grid(row=0, column=1)

        self.lbl2 = tk.Label(self.root, text="Password", bg="black", fg="white")
        self.lbl2.grid(row=1, column=0)

        self.pas = tk.Entry(self.root)
        self.pas.grid(row=1, column=1)

        self.lbl3 = tk.Label(self.root, text="Re-enter Pass", bg="black", fg="white")
        self.lbl3.grid(row=2, column=0)

        self.reEnter = tk.Entry(self.root)
        self.reEnter.grid(row=2, column=1)

        self.but = tk.Button(self.root, text="back", command=self.login_Screen)
        self.but.grid(row=3, column=1, sticky="E")

        self.root.bind("<Return>", self.register)


    def login_Screen(self): ## log into a profile
        self.user = ''
        self.root.geometry("")
        self.forget()
        self.root.config(bg="BLACK")

        self.lbl1 = tk.Label(self.root, text="Username", bg="black", fg="white")
        self.lbl1.grid(row=0, column=0)

        
        self.user = tk.Entry(self.root)
        self.user.grid(row=0, column=1)

        self.lbl2 = tk.Label(self.root, text="Password", bg="black", fg="white")
        self.lbl2.grid(row=1, column=0)

        self.pas = tk.Entry(self.root)
        self.pas.grid(row=1, column=1)

        self.lbl = tk.Label(self.root, text="Dont have an account?", bg="black", fg="white")
        self.lbl.grid(row=3, column=0, sticky="E")

        self.but = tk.Button(self.root, text="register", command=self.create_Screen)
        self.but.grid(row=3, column=1, sticky="W")

        self.root.bind("<Return>", self.valid)
        pass



    def register(self, event):##register account in database
        self.root.title("Register")
        h = hashlib.sha256()
        if(self.pas.get()==self.reEnter.get()):
            connection = sqlite3.connect('./capData.db')
            cursor = connection.cursor()
            if(len(cursor.execute(f"SELECT user FROM cred WHERE user= ?",(self.user.get(),),).fetchall())==0):
                if(self.pas.get()==self.reEnter.get()):
                    ##username does not exist
                    os.makedirs(os.getcwd()+'\\Users\\'+self.user.get())
                    salt1 = os.urandom(64)
                    salt1 = salt1.hex()
                    salt2 = os.urandom(64)
                    salt2 = salt2.hex()
                    password = bytes(self.pas.get()+salt1, 'utf-8')
                    h.update(password)
                    cursor.execute(f"INSERT INTO cred VALUES (?, ?, ?, ?)",(self.user.get(), h.hexdigest(), salt1, salt2,),)
                    connection.commit()
                    messagebox.showinfo(message="Profile Successfully Created!")
                    self.login_Screen()
            else:
                messagebox.showinfo(message="Username Already Taken")
                ##username exists

    ##password auth
    def valid(self, event):
        h = hashlib.sha256()
        connection = sqlite3.connect('./capData.db')
        cursor = connection.cursor()
        if(cursor.execute(f"SELECT user FROM cred WHERE user = ?",(self.user.get(),),).fetchall()): ##checks if user exists
            salt = cursor.execute("SELECT salt1 FROM cred WHERE user = ?",(self.user.get(),),).fetchall()
            h.update(bytes(self.pas.get()+salt[0][0], 'utf-8'))
            if(h.hexdigest() == (cursor.execute(f"SELECT pass FROM cred WHERE user = ?",(self.user.get(),),).fetchall())[0][0]): ##validates password
                salt2 = cursor.execute("SELECT salt2 FROM cred WHERE user = ?",(self.user.get(),),).fetchall()
                h.update(bytes(salt2[0][0], 'utf-8')) ## adds another salt on top and hashes
                self.user = self.user.get()
                self.key = h.hexdigest()
                self.explorer()
            else:
                messagebox.showinfo(message="Incorrect Username or Password")
        else:
            messagebox.showinfo(message="Incorrect Username or Password")
            

    def forget(self): ## clears screen of widgets
            for widget in self.root.winfo_children():
                widget.destroy()
            pass

    ##window for closing
    def close(self):
        if messagebox.askyesno(message="are you sure you want to close?"):
            self.root.destroy()
        pass

    def explorer(self):
        self.forget()
        self.root.geometry("500x300")
        self.root.config(bg="WHITE")
        self.lbl = tk.Label(text=self.user)
        self.lbl.place(x=0, y=0)
        self.signButt = tk.Button(text="Sign Out", command=self.login_Screen)
        self.signButt.pack(anchor="ne")
        self.createButt = tk.Button(text="Create", command= lambda: popup.create(self.user))
        self.createButt.place(x=130, y=0)

        self.path = os.getcwd()+'\\Users\\'+self.user

        self.scroll = tk.Scrollbar(self.root)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.myList = Listbox(self.root, yscrollcommand=self.scroll.set)

        self.myList.place(x=0, y=25, height=275, width=485)

        self.scroll.config(command=self.myList.yview)

        self.myList.bind("<Button-3>", self.options)
        self.root.bind("<FocusIn>", self.refresh)
        self.root.unbind("<KeyPress>")
        self.root.bind("<Return>", self.open)

    def open(self, event):
        popup.Editor(f"{os.getcwd()}\\Users\\{self.user}\\{self.myList.get(ANCHOR)}", self.key)

    def options(self, event): ##options menu opens (just a widget)
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Rename", command= lambda: popup.rename(self.user, self.myList.get(ANCHOR)))
        self.menu.add_command(label="Delete", command=self.delete)
        self.menu.tk_popup(event.x_root, event.y_root, 0)

    def delete(self):
        os.remove(self.path+'\\'+self.myList.get(ANCHOR))
        self.myList.delete(ANCHOR)

    def refresh(self, event):
        self.myList.delete(0, END)    
        for file in os.listdir(self.path):
            self.myList.insert(END, file)


GUI = MyGUI()
