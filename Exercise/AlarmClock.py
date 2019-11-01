#coding:gbk

import time
from tkinter import messagebox

def Message_Box(title, msg, status):
    if status == "info":
        messagebox.showinfo(title, msg)
    elif status == "warning":
        messagebox.showwarning(title, msg)
    elif status == "error":
        messagebox.showerror(title, msg)

Times = time.strftime("%M", time.localtime())

while True:
    if Times == '57':
        Message_Box("闹钟","body","info")
        break
    else:
        Times = time.strftime("%M", time.localtime())
        # print (time.strftime("%S",time.localtime()))
        time.sleep(1)