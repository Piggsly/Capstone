import tkinter as tk
import os
from cryptography.fernet import Fernet

def create(user):
    def docreate():
        f = open(f"{os.getcwd()}\\Users\\{user}\\{ent.get()}.txt", "x")
        window.destroy()
    
    window = tk.Toplevel()
    window.iconbitmap("Locker_icon.ico")
    window.geometry("150x50")
    window.resizable(False, False)
    lbl = tk.Label(window, text="Input Name")
    lbl.pack()
    ent = tk.Entry(window)
    ent.pack()
    window.bind("<Return>", lambda event: docreate())
    window.mainloop()


def rename(user, name):
    def dorename():
        os.rename(f"{os.getcwd()}\\Users\\{user}\\{name}", f"{os.getcwd()}\\Users\\{user}\\{ent.get()}.txt")
        window.destroy()
    
    window = tk.Toplevel()
    window.iconbitmap("Locker_icon.ico")
    window.geometry("150x50")
    window.resizable(False, False)
    lbl = tk.Label(window, text="Input New Name")
    lbl.pack()
    ent = tk.Entry(window)
    ent.pack()
    window.bind("<Return>", lambda event: dorename())
    window.mainloop()


def Editor(path, key):
    def save(event):
        s = open(path, 'w')
        s.write(t.get("1.0", tk.END))
        print("saved")
    window = tk.Toplevel()
    window.iconbitmap("Locker_icon.ico")
    window.geometry("600x400")
    t = tk.Text(window)
    f = open(path, 'r')
    for l in f:
        t.insert('1.0', l)
    ##for loop which reads file line by line, translates is then puts it on the textbox
    t.pack(expand=True, fill="both")
    window.bind("<Control-s>", save)
    window.mainloop()


'''create("")
rename("", "")
Editor(f"{os.getcwd()}\\Users\\Piggsly\\test.txt", "")'''