from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import tkinter as tk
import sv_ttk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import random
from itertools import count
import pandas as pd

import XbeeReceive
import GroundSensorOne
import GroundSensorTwo
import GPSSensor
import time

class MyGUI:
    #Main Method (Calls itself)
    def __init__(self):
        self.xbee = XbeeReceive.Xbee()
        
        #Tkinter Portion of Program
        self.root = tk.Tk()

        #Default visual variables that can be changed
        self.root.geometry("2500x2500")
        self.root.title("UVA BOTR Ground Station V0.2")
        # self.root.iconbitmap('uvarocketrylogo.ico')
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

        # self.space1 = tk.Label(self.graphframe, text = "State:", font = self.defaultfont)
        # self.space1.grid(row = 0, column = 0, sticky = tk.W+tk.E)
        # self.space2 = tk.Frame(self.graphframe, text=self.xbee.returnState(), font = self.defaultfont)
        # self.space2.grid(row = 0, column = 1, sticky = tk.W+tk.E)
        self.space3 = tk.Label(self.graphframe, text = "Altitude:", font = self.defaultfont)
        self.space3.grid(row = 0, column = 2, sticky = tk.W+tk.E)
        self.space5 = tk.Label(self.graphframe, text = "Satellites:", font = self.defaultfont)
        self.space5.grid(row = 0, column = 4, sticky = tk.W+tk.E)
        self.space7 = tk.Label(self.graphframe, text = "Velocity:", font = self.defaultfont)
        self.space7.grid(row = 0, column = 6, sticky = tk.W+tk.E)
        self.space9 = tk.Label(self.graphframe, text = "Angle:", font = self.defaultfont)
        self.space9.grid(row = 0, column = 8, sticky = tk.W+tk.E)
        self.space11 = tk.Label(self.graphframe, text = "Save:", font = self.defaultfont)
        self.space11.grid(row = 0, column = 10, sticky = tk.W+tk.E)
        self.saveButton = tk.Button(self.graphframe, text = 'Save Data', command= lambda: self.save_file(), background="#99fb99", font = self.defaultfont)
        self.saveButton.grid(row = 0, column = 11, sticky = tk.W+tk.E)

        self.graphframe.pack(fill = 'x')
        
        self.anotherFrame = tk.Frame(self.root)
        self.anotherFrame.columnconfigure(0, weight = 1)
        self.anotherFrame.columnconfigure(1, weight = 1)
        
        self.anotherFrame.pack(fill = 'x')

        self.g1 = GroundSensorOne.GroundSensorOne(self.xbee)
        self.g2 = GroundSensorTwo.GroundSensorTwo(self.xbee)
        self.gps = GPSSensor.GPS(self.xbee)

        #light/dark mode
        sv_ttk.set_theme("dark")
        
    def setUpTopLabels(self):
        self.space4 = tk.Label(self.graphframe, text=self.xbee.returnRawData()[9] + "m", font=self.defaultfont)
        self.space4.grid(row = 0, column = 3, sticky = tk.W+tk.E)
        
        self.space6 = tk.Label(self.graphframe, text=self.xbee.returnRawData()[10] + "m/s", font=self.defaultfont)
        self.space6.grid(row = 0, column = 5, sticky = tk.W+tk.E)
        
        self.space8 = tk.Label(self.graphframe, text=self.xbee.returnRawData()[7] , font=self.defaultfont)
        self.space8.grid(row = 0, column = 7, sticky = tk.W+tk.E)
        
        self.space10 = tk.Label(self.graphframe, text=self.xbee.returnRawData()[8] + "°", font=self.defaultfont)
        self.space10.grid(row = 0, column = 9, sticky = tk.W+tk.E)

    def setUpGSGraphs(self):
        self.figure1 = self.g1.returnGraphG1()
        self.graph1 = FigureCanvasTkAgg(self.figure1, self.anotherFrame)
        self.graph1.get_tk_widget().grid(row = 0, column = 0, columnspan = 1, sticky = tk.W+tk.E)
        
        self.figure2 = self.g2.returnGraphG2()
        self.graph2 = FigureCanvasTkAgg(self.figure2, self.anotherFrame)
        self.graph2.get_tk_widget().grid(row = 0, column = 1, columnspan = 1, sticky = tk.W+tk.E)
        
        self.g1.animation()
        self.g2.animation()
        
        self.anotherFrame.pack(fill = 'x')
        
    def setUpGPSGraph(self):
        self.figure3 = self.gps.returnGraphG3()
        self.graph3 = FigureCanvasTkAgg(self.figure3, self.anotherFrame)
        self.graph3.get_tk_widget().grid(row=1, column=1, columnspan=1, sticky=tk.W+tk.E)
        
        self.gps.animation()
        
        self.anotherFrame.pack(fill='x')
        
    def setUpRawData(self):
        self.textWidget = scrolledtext.ScrolledText(self.anotherFrame, font=self.defaultfont, width='10')
        self.textWidget.grid(row=1, column=0, columnspan=1, sticky = tk.W+tk.E)
        self.anotherFrame.pack(fill = 'x')
    
    def save_file(self):
        file = filedialog.asksaveasfilename(title = "Save Flight Data", filetypes=[('Text File', '*.txt'), ('CSV File', '*.csv')], defaultextension = '.txt')
        
        if(file):
            fob= open(file, "w")
            fob.write(self.textWidget.get('1.0', tk.END))
            fob.close()
        else:
            print("No file Chosen")

    def mainLoop(self):
        self.counter = 0
        self.xbee.openSerPort()
        # Sets up the scroll text widget
        self.setUpRawData()
        # Sets up GPS graphs and adds the Lat and Long to the graph
        self.setUpGPSGraph()
        
        while True:
            # Receive xbee data (this has a current one second delay)
            self.xbee.receive()
            if (self.counter < 10):
                # Sets up graphs and adds new points to the line
                self.setUpGSGraphs()
            
            # Inserts raw data every iteration and autoscrolls
            self.textWidget.insert(tk.INSERT, ' '.join([str(elem) for elem in self.xbee.returnRawData()]) + '\n')
            self.textWidget.yview(tk.END)
            # Updates the top labels
            self.setUpTopLabels()
            
            # exit protocol
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            # This basically delays the update to keep it at 30 fps so the loop doesn't go too fast and break everything
            self.windowUpdate(fps=30)
            self.counter += 1
        
    def windowUpdate(self, fps=30):
        time.sleep(1/fps)
        self.root.update()
    
    #Closing Method (Asks user if they really want to close the window)
    def on_closing(self):
        if(messagebox.askyesno(title="Quit?", message="Do you really want to quit?")):
            self.root.destroy()
            self.xbee.closeSerPort()

gui = MyGUI()
gui.mainLoop()  