import tkinter as tk
from tkinter import *
from tkinter import ttk
from faster_whisperer import *

# Initialize Tkinter
root = Tk()
root.title("Airport Translator")

recArray = ["Stop Recording", "Start Recording"]
titleArray = ["Recording...", "Translator"]
recVar = 1

# UI Elements
frm = ttk.Frame(root, padding=10)
frm.grid()

title = ttk.Label(frm, text=titleArray[recVar])
title.grid(column=0, row=0)

quitBut = ttk.Button(frm, text="Quit", command=root.destroy)
quitBut.grid(column=3, row=3)

recBut = ttk.Button(frm, text="Start Recording")
recBut.grid(column=2, row=3)

subBut = ttk.Button(frm, text="Transcribe Audio")
subBut.grid(column=2, row=2)

def toggleRec():
    global recVar, recArray
    if recVar == 1:
        recVar = 0
        start_recording()
    else:
        recVar = 1
        stop_recording()
    recBut.config(text=recArray[recVar])
    title.config(text=titleArray[recVar])

def transcribe():
    """Creates a new window and displays the transcribed text."""
    textScript = transcribe_audio()  # Transcribe the last recorded audio

    top = Toplevel()
    top.title("Transcription")
    
    transcript_label = ttk.Label(top, text=textScript, wraplength=400, padding=10)
    transcript_label.pack(pady=10)

    # Add Copy Button
    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(textScript)
        root.update()
    
    copy_button = ttk.Button(top, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(pady=5)

subBut.config(command=transcribe)
recBut.config(command=toggleRec)

root.mainloop()
