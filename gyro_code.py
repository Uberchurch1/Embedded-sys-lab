#!/usr/bin/python
import tkinter as tk
from tkinter import *
from tkinter import ttk

import serial

ser = serial.Serial('/dev/ttyACM1', 115200, 8, 'N', 1, timeout=5)

root = Tk()

check_gyro = IntVar()
data_var = StringVar()
data_var.set('NO DATA')

frm = ttk.Frame(root, padding=10)
frm.grid()
root.title("Arduino Gyro Readings")
title_L = ttk.Label(frm, text="Gyro Vibration Reading")
title_L.grid(column=0, row=0)
data_E = ttk.Entry(frm, width=100, state='readonly', textvariable = data_var)
data_E.grid(column=0, row=1)

gyro_B = ttk.Button(frm, text="Start Data Check")
gyro_B.grid(column=1, row=0)
def startData():
    global data_E
    while True:
        if ser.in_waiting > 0:
            data_raw = ser.readline()
            data_ref0 = data_raw[0:-2]
            #print(data_ref0)
            data_var.set(data_ref0)
            root.update_idletasks()
gyro_B.config(command=startData)
data_E.insert(0, "no data")
root.mainloop()
