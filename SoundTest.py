from tkinter import *
from tkinter import ttk, font

from Phidget22.Phidget import *
from Phidget22.Devices.SoundSensor import *

import time
import numpy as np
import matplotlib.pyplot as plt
import csv

fileNameString = "output file name"
serialNumberString = "12345"
duration = 10
samplingRate = 0.01

soundDataArray = []
sampleTimeArray = []

def runFunction():

    global serialNumberString
    global duration
    global samplingRate

    try:
        serialNumberString = SerialNumber_Box.get()
        duration = int(Duration_Box.get())
        samplingRate = float(samplingRate_Box.get())
    except Exception:
        print("ERROR: Invalid inputs. Values must be greater than zero and not empty.")
        return     
    
    if not ( (samplingRate < 30) or (samplingRate > 0.001) ):
        print("ERROR: Sampling rate must be less than 1 and greater than 1ms.")
        return    
    
    if not ( (duration < 30) or (duration > samplingRate) ):
        print("ERROR: Duration must be greater than the sampling rate and less than 30 seconds.")
        return    

    print("                      ")
    print("======================")
    print(" TEST CONFIGURATION   ")
    print("======================")
    print("                      ")
    print("Serial Number: " + str(serialNumberString))
    print("Duration:      " + str(duration))
    print("Sampling Rate: " + str(samplingRate))
    print("                      ")

    global testStartTime
    global fileNameString
    testStartTime = time.strftime('%Y-%m-%d %H-%M-%S')
    fileNameString = testStartTime + " " + 'SN' + str(serialNumberString)

    dataCollection()
    exportData()
    plotData()  

    return

def dataCollection():
    # Attempt to connect to Phidets
    try:
        SoundSensor0  = SoundSensor()
        SoundSensor0.setHubPort(0)
        SoundSensor0.openWaitForAttachment(5000)
        SoundSensor0.setDataRate(SoundSensor0.getMaxDataRate())

    except:
        print("ERROR: Phidgets not attached.")
        return
    
    global soundDataArray
    global sampleTimeArray
    global duration

    del soundDataArray[:]
    del sampleTimeArray[:]

    testStartTime = time.time()    

    currentTime = time.time()
    while currentTime - testStartTime < duration:
        soundDataArray.append(SoundSensor0.getdBA())
        sampleTimeArray.append(currentTime - testStartTime)
        time.sleep(samplingRate)
        currentTime = time.time()
    
    SoundSensor0.close()
    return

def exportData():

    global soundDataArray
    global sampleTimeArray
    global fileNameString

    f = open(fileNameString + " Data.csv", "w", newline='', encoding='utf-8')
    c = csv.writer(f)

    header = ['Sample', 'Elapsed', 'dbA']
    c.writerow(header)
    
    Sample = 0

    for index, item in enumerate(sampleTimeArray):
        data = [Sample,sampleTimeArray[index],soundDataArray[index]]
        c.writerow(data)
        Sample = Sample + 1
        
    f.close()
    return

def plotData():

    global soundDataArray
    global sampleTimeArray
    global fileNameString
    
    plt.close('all')                                     # Close existing plots for subsequent runs
    plt.figure(figsize=(8,4),num="Output Data Plot")     # Set size and title
    
    # plot our data    
    plt.plot(sampleTimeArray,soundDataArray)

    # Format
    plt.title('SN' + str(serialNumberString) + ' Output Data Plot')
    plt.xlabel('Time')
    plt.ylabel('dbA')
    
    plt.tight_layout()
    plt.savefig(fileNameString+'.png')
    plt.show()
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
    Duration_Box.insert(0,duration)
    
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