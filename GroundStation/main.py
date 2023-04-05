#Tkinter Imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import sv_ttk
#from tkinter import filedialog
#from tkinter.filedialog import asksaveasfile

#Matplotlib Imports
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

#Other Imports
import random
from itertools import count
import pandas as pd

#Python File Imports
import XbeeReceive
import CombinedGroundSensors

#Xbee Import
import serial
import time

class MyGUI:
    #Main Method (Calls itself)
    def __init__(self):
        #Tkinter Portion of Program
        self.root = tk.Tk()

        #Default visual variables that can be changed
        self.root.geometry("2500x2500")
        self.root.title("UVA BOTR Ground Station V0.1")
        self.defaultfont = ('Arial', 18)
        
        #Main label for top of program, change for every flight test
        self.label = tk.Label(self.root, text = "BOTR Flight Test", font = self.defaultfont)
        self.label.pack(padx=10, pady=10)

        #graph frame for the four matplotlib graphs
        self.graphframe = tk.Frame(self.root)
        self.graphframe.columnconfigure(0, weight = 1)
        self.graphframe.columnconfigure(1, weight = 1)
        self.graphframe.columnconfigure(2, weight = 1)
        self.graphframe.columnconfigure(3, weight = 1)
        self.graphframe.columnconfigure(4, weight = 1)
        self.graphframe.columnconfigure(5, weight = 1)
        self.graphframe.columnconfigure(6, weight = 1)
        self.graphframe.columnconfigure(7, weight = 1)
        self.graphframe.columnconfigure(8, weight = 1)
        self.graphframe.columnconfigure(9, weight = 1)
        self.graphframe.columnconfigure(10, weight = 1)
        self.graphframe.columnconfigure(11, weight = 1)

        #Can use for testing but it doens't show the actual numbers
        self.space1 = tk.Label(self.graphframe, text = "State:", font = self.defaultfont)
        self.space1.grid(row = 0, column = 0, sticky = tk.W+tk.E)
        self.space2 = tk.Frame(self.graphframe, background="#99fb99", height=60)
        self.space2.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        self.space3 = tk.Label(self.graphframe, text = "Altitude:", font = self.defaultfont)
        self.space3.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        self.space4 = tk.Frame(self.graphframe, background="#99fb99", height=60)
        self.space4.grid(row = 0, column = 3, sticky = tk.W+tk.E)
        self.space5 = tk.Label(self.graphframe, text = "Apogee", font = self.defaultfont)
        self.space5.grid(row = 0, column = 4, sticky = tk.W+tk.E)
        self.space6 = tk.Frame(self.graphframe, background="#99fb99", height=60)
        self.space6.grid(row = 0, column = 5, sticky = tk.W+tk.E)
        self.space7 = tk.Label(self.graphframe, text = "Velocity:", font = self.defaultfont)
        self.space7.grid(row = 0, column = 6, sticky = tk.W+tk.E)
        self.space8 = tk.Frame(self.graphframe, background="#99fb99", height=60)
        self.space8.grid(row = 0, column = 7, sticky = tk.W+tk.E)
        self.space9 = tk.Label(self.graphframe, text = "Angle:", font = self.defaultfont)
        self.space9.grid(row = 0, column = 8, sticky = tk.W+tk.E)
        self.space10 = tk.Frame(self.graphframe, background="#99fb99", height=60)
        self.space10.grid(row = 0, column = 9, sticky = tk.W+tk.E)
        self.space11 = tk.Label(self.graphframe, text = "Satellites:", font = self.defaultfont)
        self.space11.grid(row = 0, column = 10, sticky = tk.W+tk.E)
        self.space12 = tk.Frame(self.graphframe, background="#99fb99", height=60)
        self.space12.grid(row = 0, column = 11, sticky = tk.W+tk.E)

        #Should show the actual numbers
        # space1 = tk.Label(self.graphframe, text = "State:", font = self.defaultfont)
        # space1.grid(row = 0, column = 0, sticky = tk.W+tk.E)
        # space2 = tk.Label(self.graphframe, text = self.xbeeG.currentState, background="#99fb99", font = self.defaultfont)
        # space2.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        # space3 = tk.Label(self.graphframe, text = "Altitude:", font = self.defaultfont)
        # space3.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        # space4 = tk.Label(self.graphframe, text = self.XbeeG.gpsAltitude, background="#99fb99", font = self.defaultfont)
        # space4.grid(row = 0, column = 3, sticky = tk.W+tk.E)
        # space5 = tk.Label(self.graphframe, text = "Apogee", font = self.defaultfont)
        # space5.grid(row = 0, column = 4, sticky = tk.W+tk.E)
        # space6 = tk.Label(self.graphframe, text = self.XBeeG.currentApogee, background="#99fb99", font = self.defaultfont)
        # space6.grid(row = 0, column = 5, sticky = tk.W+tk.E)
        # space7 = tk.Label(self.graphframe, text = "Velocity:", font = self.defaultfont)
        # space7.grid(row = 0, column = 6, sticky = tk.W+tk.E)
        # space8 = tk.Label(self.graphframe, text = self.XbeeG.gpsSpeed, background="#99fb99", font = self.defaultfont)
        # space8.grid(row = 0, column = 7, sticky = tk.W+tk.E)
        # space9 = tk.Label(self.graphframe, text = "Angle:", font = self.defaultfont)
        # space9.grid(row = 0, column = 8, sticky = tk.W+tk.E)
        # space10 = tk.Label(self.graphframe, text = self.XbeeG.gpsAngle, background="#99fb99", font = self.defaultfont)
        # space10.grid(row = 0, column = 9, sticky = tk.W+tk.E)
        # space11 = tk.Label(self.graphframe, text = "Satellites:", font = self.defaultfont)
        # space11.grid(row = 0, column = 10, sticky = tk.W+tk.E)
        # space12 = tk.Label(self.graphframe, text = self.XbeeG.gpsSatellites, background="#99fb99", font = self.defaultfont)
        # space12.grid(row = 0, column = 11, sticky = tk.W+tk.E)

        self.graphframe.pack(fill = 'x')
        # self.button = ttk.Button(self.root, text = "CLICK ME!")
        # self.button.pack(fill = 'x')
        
        #light/dark mode
        sv_ttk.set_theme("dark")
        
        #frames for the matplotlib graphs
        self.anotherFrame = tk.Frame(self.root)
        self.anotherFrame.columnconfigure(0, weight = 1)
        self.anotherFrame.columnconfigure(1, weight = 1)
        
        self.xbeeG = XbeeReceive.Xbee()
        self.xbeeG.openSerPort()
        
        self.groundSensors = CombinedGroundSensors.GroundSensors(self.xbeeG)

        #Raw data
        # self.rawDataArea = scrolledtext.ScrolledText(self.anotherFrame, font = self.defaultfont)
        # self.rawDataArea.grid(row = 1, column = 1, columnspan = 1, sticky = tk.W+tk.E)
        # self.rawDataArea.insert(tk.INSERT, self.xbeeG.returnRawData())

    def setUpGraphs(self):
        #Remote Sensor 1
        self.figure1 = self.groundSensors.returnGraphG1()
        self.graph1 = FigureCanvasTkAgg(self.figure1, self.anotherFrame)
        self.graph1.get_tk_widget().grid(row = 0, column = 0, columnspan = 1, sticky = tk.W+tk.E)
        
        #Remote Sensor 2
        self.figure2 = self.groundSensors.returnGraphG2()
        self.graph2 = FigureCanvasTkAgg(self.figure2, self.anotherFrame)
        self.graph2.get_tk_widget().grid(row = 0, column = 1, columnspan = 1, sticky = tk.W+tk.E)
        
        # #GPS Sensor
        # self.figure3 = self.GPSSensor.returnGraphG3()
        # self.graph3 = FigureCanvasTkAgg(self.figure3, self.anotherFrame)
        # self.graph3.get_tk_widget().grid(row = 1, column = 0, columnspan = 1, sticky = tk.W+tk.E)

        #animate those graphs and then pack to the tkinter gui
        self.groundSensors.animation()
        # self.GPSSensor.animation()
        self.anotherFrame.pack(fill = 'x')
    
    def mainLoop(self):
        # Don't know why this is necessary
        #self.groundSensors.xbeeReceive()
        self.setUpGraphs()
        
        while True:
            self.xbeeG.receive()
            print("is this working")
            
            # self.setUpXbee()

            # main loop and exit protocol
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.update_idletasks()
            self.root.update()
        # self.root.mainloop()
    
    #Closing Method (Asks user if they really want to close the window)
    def on_closing(self):
        if(messagebox.askyesno(title="Quit?", message="Do you really want to quit?")):
            self.root.destroy()
            self.xbeeG.closeSerPort()
    
gui = MyGUI()
gui.mainLoop()  