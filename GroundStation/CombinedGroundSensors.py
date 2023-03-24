import random
from itertools import count
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import XbeeReceive

class GroundSensors:
    def __init__(self):
        self.xbee = XbeeReceive.Xbee()
        
        self.plt1 = plt
        self.plt2 = plt
        
        style.use('fivethirtyeight')
        
        # Declares both graphs
        self.fig1, self.axl1 = self.plt1.subplots()
        self.axl1.set_title("Remote Sensor One")
        self.axl1.set_xlabel("Time")
        self.axl1.grid(True)
        
        self.fig2, self.axl2 = self.plt2.subplots()
        self.axl2.set_title("Remote Sensor Two")
        self.axl2.set_xlabel("Time")
        self.axl2.grid(True)
        
        self.gpsTimeList = []
        
        # data from remote sensor 1
        # temp, pressure, humidity, solar voltage
        self.g1Data = [[], [], [], []]
        self.g1DataLines = []
        for j in range(4):
            self.g1DataLines.append(self.axl1.plot([],[])[0])
            
        # self.axl1.legend()

        # data from remote sensor 2
        # temp, pressure, humidity, solar voltage
        self.g2Data = [[], [], [], []]
        self.g2DataLines = []
        for j in range(4):
            self.g2DataLines.append(self.axl2.plot([],[])[0])
            
        # self.axl2.legend()
    
    # Appends the data onto the lines
    def animate(self, i, gps, data, lines, ax):
        gps.append(xbee.returnGPSTime())
        
        data[0].append(xbee.returnSensData[0])
        data[1].append(xbee.returnSensData[1])
        data[2].append(xbee.returnSensData[2])
        data[3].append(xbee.returnSensData[3])
        
        for j in range(4):
            lines[j].set_data(gps, data[j])
            ax.relim()
            ax.autoscale_view()
        
    # Calls the animate function based on which remote sensor sent the data
    def animation(self):
        self.sensNumber = type(int(self.xbee.returnSensData[0]))
        self.state = type(int(self.xbee.returnState()))
        
        if self.state == 1 | self.state == 2:
            if self.sensNumber == 1:
                self.aniOne = FuncAnimation(self.fig1, self.animate, frames=None, cache_frame_data=False, fargs=(self.gpsTimeList, self.g1Data, self.g1DataLines, self.axl1))
            elif self.sensNumber == 2:
                self.aniTwo = FuncAnimation(self.fig2, self.animate, frames=None, cache_frame_data=False, fargs=(self.gpsTimeList, self.g2Data, self.g2DataLines, self.axl2))
        
    def returnGraphG1(self):
        return self.fig1

    def returnGraphG2(self):  
        return self.fig2