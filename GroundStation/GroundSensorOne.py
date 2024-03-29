import random
from itertools import count
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import XbeeReceive

class GroundSensorOne:
    def __init__(self, xbee):
        self.xbee = xbee
        
        self.plt1 = plt
        
        style.use('fivethirtyeight')
        
        self.fig1, self.axl1 = self.plt1.subplots()
        self.axl1.set_title("Remote Sensor One")
        self.axl1.set_xlabel("Time")
        self.axl1.grid(True)
        
        self.gpsSecListOne = []
        self.indexOne = count()
        # data from remote sensor 1
        # pressure, temp, humidity, solar voltage
        self.g1Data = [[], [], [], []]
        self.g1DataLines = []
        for j in range(4):
            self.g1DataLines.append(self.axl1.plot([],[])[0])
        
    def animate(self, i, gps, data, lines, ax, index):
        if (int(self.xbee.sensNum) == 1):
            gps.append(next(index))
            
            data[0].append(float(self.xbee.returnSensData()[1]))
            data[1].append(float(self.xbee.returnSensData()[2]) / 1000)
            data[2].append(float(self.xbee.returnSensData()[3]))
            data[3].append(float(self.xbee.returnSensData()[4]))
            
            for j in range(4):
                lines[j].set_data(gps, data[j])
                ax.relim()
                ax.autoscale_view()
        
    def animation(self):
            self.aniOne = FuncAnimation(self.fig1, self.animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListOne, self.g1Data, self.g1DataLines, self.axl1, self.indexOne))
        
    def returnGraphG1(self):
        self.fig1.legend((self.g1DataLines[0], self.g1DataLines[1], self.g1DataLines[2], self.g1DataLines[3]), ('Temperature(C)', 'Pressure(kPa)', 'Humidity(%)', 'Solar Voltage(V)'), 'upper right')
        return self.fig1