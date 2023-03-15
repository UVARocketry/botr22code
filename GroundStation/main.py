#imports used for xbee receive
import serial
import time

#imports used for tkinter
import tkinter as tk
import sv_ttk
from tkinter import ttk
from tkinter import messagebox
#from tkinter import filedialog
#from tkinter.filedialog import asksaveasfile

#Global Variables For Parsing
sensNum = ""
gpsHour = ""
gpsMin = ""
gpsSec = ""
gpsMSec = ""
gpsLong = ""
gpsLat = ""
gpsSpeed = "200"
gpsAngle = "30"
gpsAltitude = "400"
gpsSatellites = "7"
tempOne = ""
pressureOne = ""
humidityOne = ""
solarVoltOne = ""
tempTwo = ""
pressureTwo = ""
humidityTwo = ""
solarVoltTwo = ""
currentApogee = "500"

#State Estimation
currentState = 0;
stateNotReadyForFlight = 0;
stateReadyForFlight = 1;
stateInFlight = 2;

ser = serial.Serial(port = "COM3", baudrate = 9600)
class MyGUI:
    #Main Method (Calls itself)
    def __init__(self):
        #Tkinter Portion of Program
        self.root = tk.Tk()

        #Default visual variables that can be changed
        self.root.geometry("500x500")
        self.root.title("UVA BOTR Ground Station V0.1")
        defaultfont = ('Arial', 18)

        #Main label for top of program, change for every flight test
        self.label = tk.Label(self.root, text = "BOTR Flight Test", font = defaultfont)
        self.label.pack(padx=10, pady=10)

        #graph frame for the four matplotlib graphs
        graphframe = tk.Frame(self.root)
        graphframe.columnconfigure(0, weight = 1)
        graphframe.columnconfigure(1, weight = 1)
        graphframe.columnconfigure(2, weight = 1)
        graphframe.columnconfigure(3, weight = 1)
        graphframe.columnconfigure(4, weight = 1)
        graphframe.columnconfigure(5, weight = 1)
        graphframe.columnconfigure(6, weight = 1)
        graphframe.columnconfigure(7, weight = 1)
        graphframe.columnconfigure(8, weight = 1)
        graphframe.columnconfigure(9, weight = 1)
        graphframe.columnconfigure(10, weight = 1)
        graphframe.columnconfigure(11, weight = 1)

        #background="#99fb99"
        space1 = tk.Label(graphframe, text = "State:", font = defaultfont)
        space1.grid(row = 0, column = 0, sticky = tk.W+tk.E)
        space2 = tk.Label(graphframe, text = currentState, background="#99fb99", font = defaultfont)
        space2.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        space3 = tk.Label(graphframe, text = "Altitude:", font = defaultfont)
        space3.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        space4 = tk.Label(graphframe, text = gpsAltitude, background="#99fb99", font = defaultfont)
        space4.grid(row = 0, column = 3, sticky = tk.W+tk.E)
        space5 = tk.Label(graphframe, text = "Apogee", font = defaultfont)
        space5.grid(row = 0, column = 4, sticky = tk.W+tk.E)
        space6 = tk.Label(graphframe, text = currentApogee, background="#99fb99", font = defaultfont)
        space6.grid(row = 0, column = 5, sticky = tk.W+tk.E)
        space7 = tk.Label(graphframe, text = "Velocity:", font = defaultfont)
        space7.grid(row = 0, column = 6, sticky = tk.W+tk.E)
        space8 = tk.Label(graphframe, text = gpsSpeed, background="#99fb99", font = defaultfont)
        space8.grid(row = 0, column = 7, sticky = tk.W+tk.E)
        space9 = tk.Label(graphframe, text = "Angle:", font = defaultfont)
        space9.grid(row = 0, column = 8, sticky = tk.W+tk.E)
        space10 = tk.Label(graphframe, text = gpsAngle, background="#99fb99", font = defaultfont)
        space10.grid(row = 0, column = 9, sticky = tk.W+tk.E)
        space11 = tk.Label(graphframe, text = "Satellites:", font = defaultfont)
        space11.grid(row = 0, column = 10, sticky = tk.W+tk.E)
        space12 = tk.Label(graphframe, text = gpsSatellites, background="#99fb99", font = defaultfont)
        space12.grid(row = 0, column = 11, sticky = tk.W+tk.E)

        graphframe.pack(fill = 'x')

        anotherFrame = tk.Frame(self.root)
        anotherFrame.columnconfigure(0, weight = 1)
        anotherFrame.columnconfigure(1, weight = 1)


        btn9 = tk.Button(anotherFrame, text = "1", font = defaultfont)
        btn9.grid(row = 1, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn10 = tk.Button(anotherFrame, text = "2", font = defaultfont)
        btn10.grid(row = 1, column = 1, sticky = tk.W+tk.E)

        btn11 = tk.Button(anotherFrame, text = "3", font = defaultfont)
        btn11.grid(row = 2, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        btn12 = tk.Button(anotherFrame, text = "4", font = defaultfont)
        btn12.grid(row = 2, column = 1, sticky = tk.W+tk.E)

        anotherFrame.pack(fill = 'x')
        
        #light/dark mode
        sv_ttk.set_theme("light")

        #main loop and exit protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    #Closing Method (Asks user if they really want to close the window)
    def on_closing(self):
        if(messagebox.askyesno(title="Quit?", message="Do you really want to quit?")):
            self.root.destroy()
            ser.close();

    #Xbee receive method, will receive and parse data when called
    def xbee_Receive(self):
        buffer = ser.readline().decode()
        #print(buffer)

        tempBuffer = buffer.split(',')
        sensNum = tempBuffer[0]
        gpsHour =  tempBuffer[1]
        gpsMin =  tempBuffer[2]
        gpsSec =  tempBuffer[3]
        gpsMSec =  tempBuffer[4]
        gpsLong =  tempBuffer[5]
        gpsLat = tempBuffer[6]
        gpsSpeed = tempBuffer[7]
        gpsAngle = tempBuffer[8]
        gpsAltitude = tempBuffer[9]
        gpsSatellites = tempBuffer[10]

        if sensNum == "1":
            #print("Sensor One Data Received")
            tempOne = tempBuffer[11]
            pressureOne = tempBuffer [12]
            humidityOne = tempBuffer[13]
            solarVoltOne = tempBuffer[14]
        if sensNum == "2":
            #print("Sensor Two Data Received")
            tempTwo = tempBuffer[11]
            pressureTwo = tempBuffer [12]
            humidityTwo = tempBuffer[13]
            solarVoltTwo = tempBuffer[14]

        
        rs1_data_counter = tempBuffer[15]
        rs2_data_counter = tempBuffer[16]
        gps_data_counter = tempBuffer[17]

        # if sensNum == "1":
        #print("sensNum: %s, gpsHour: %s, gpsMin: %s, gpsSec: %s, gpsMSec: %s, gpsLong: %s, gpsLat: %s, gpsSpeed: %s, gpsAngle: %s, gpsAltitude: %s, gpsSatellites: %s, temp: %s, pressure: %s, humidity: %s, solarVolt: %s, rs1_data_counter: %s, rs2_data_counter: %s, gps_data_counter: %s" 
        #% (sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, tempOne, pressureOne, humidityOne, solarVoltOne, rs1_data_counter, rs2_data_counter, gps_data_counter))

        # if sensNum == "2":
        #print("sensNum: %s, gpsHour: %s, gpsMin: %s, gpsSec: %s, gpsMSec: %s, gpsLong: %s, gpsLat: %s, gpsSpeed: %s, gpsAngle: %s, gpsAltitude: %s, gpsSatellites: %s, temp: %s, pressure: %s, humidity: %s, solarVolt: %s, rs1_data_counter: %s, rs2_data_counter: %s, gps_data_counter: %s" 
        #% (sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, tempTwo, pressureTwo, humidityTwo, solarVoltTwo, rs1_data_counter, rs2_data_counter, gps_data_counter))
        
        #Update current apogee if necessary
        if(gpsAltitude > currentApogee):
            currentApogee = gpsAltitude
        
        #Change parameters as necessary
        if gpsLong == 0 and sensNum == 0:
            #Current State = 0
            currentState = stateNotReadyForFlight
        elif gpsLong != 0 and sensNum != 0 and gpsSpeed < 10:
            #Current State = 1
            currentState = stateReadyForFlight
        else:
            #Current State = 2
            currentState = stateInFlight
        time.sleep(1)   
MyGUI()     