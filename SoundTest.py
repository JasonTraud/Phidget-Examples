from tkinter import *
from tkinter import ttk, font

from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.DigitalOutput import *

import time
import numpy as np
import matplotlib.pyplot as plt
import csv

fileNameString = "output file name"
serialNumberString = "12345"
testTime = 10
samplingRate = 0.01

def runFunction():
    return

def callback (input) :
    if input.isdigit() and float(input)<=100 and float(input)>0:
        return True    
    elif input == "":
        return True
    else:
        return False    

if __name__=="__main__":
    window = Tk()
    window.geometry("400x225")
    window.title("Data Acquisition")
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    mainframe = ttk.Frame(window, padding="12 12 12 12")
    mainframe.grid(column=0, row=0)

    ttk.Label(mainframe,text="Serial Number",font=("Arial",16),width=15,justify=LEFT).grid(row=1,column=1)
    ttk.Label(mainframe,text="Test Duration",font=("Arial",16),width=15,justify=LEFT).grid(row=2,column=1)
    ttk.Label(mainframe,text="Sampling Rate",font=("Arial",16),width=15,justify=LEFT).grid(row=3,column=1)

    SerialNumber_Box = Entry(mainframe, width=10, font=("Arial", 16))
    SerialNumber_Box.grid(row=1, column=2)
    SerialNumber_Box.insert(0,serialNumberString)

    Duration_Box = Entry(mainframe, width=10, font=("Arial", 16))
    Duration_Box.grid(row=2, column=2)
    Duration_Box.insert(0,testTime)
    
    samplingRate_Box = Entry(mainframe, width=10, font=("Arial", 16))
    samplingRate_Box.grid(row=3, column=2)
    samplingRate_Box.insert(0,samplingRate)
    
    ttk.Label(mainframe,text="",font=("Arial",15),width=20,justify=LEFT).grid(row=6,column=1,columnspan=2)

    f = font.Font(weight="bold",size=18,family="Arial")
    btn = Button(mainframe, text="RUN", command=runFunction,width=20,bg="green",fg="white",activebackground="white",activeforeground="green")
    btn['font'] = f
    btn.grid(row=7,column=1,columnspan=2)

    ttk.Label(mainframe,text="",font=("Arial",16),width=15,justify=LEFT).grid(row=8,column=1,columnspan=2)

    window.mainloop()