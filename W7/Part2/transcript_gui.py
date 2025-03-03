import tkinter as tk
from tkinter import *
from tkinter import ttk
import time
import faster_whisperer.py as recpy
root = Tk()#initializes a tk GUI

recArray = ["Stop Recording", "Start Recording"]
titleArray = ["Recording...", "Translator"]
recVar = 1


name_var = tk.StringVar()
passw_var = tk.StringVar()
name = None
passw = None

frm = ttk.Frame(root, padding=10)#sets the padding around the border of the window
frm.grid()#sets the window to grid mode instead of place mode
title = ttk.Label(frm, text=titleArray[recVar])#creates a text label
title.grid(column=0, row=0)
quitBut = ttk.Button(frm, text="Quit", command=root.destroy)#creates a clickable button that closes the window
quitBut.grid(column=3, row=3)
recBut = ttk.Button(frm, text="Start Recording")
recBut.grid(column=2, row=3)

subBut = ttk.Button(frm, text="Transcribe Audio")
subBut.grid(column=2, row=2)


def toggleRec():
    global recVar, recArray, toggleBut, rec
    if recVar == 1:
        recVar = 0
        recpy.start_recording()
    else:
        recVar = 1
        recpy.stop_recording()
    recBut.config(text=recArray[recVar])

def transcribe():
    top = Toplevel()
    top.title("Transcription")
    top.mainloop()
    textScript = recpy.transcribe_audio()
    transcript = top.label(top, text=textScript)


subeBut.config(command=transcribe)
recBut.config(command=toggleRec)
root.mainloop()#runs window program
