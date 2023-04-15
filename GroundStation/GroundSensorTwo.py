import random
from itertools import count
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import XbeeReceive

class GroundSensorTwo:
    def __init__(self, xbee):
        self.xbee = xbee
        
        self.plt2 = plt
        
        style.use('fivethirtyeight')
        
        self.fig2, self.axl2 = self.plt2.subplots()
        self.axl2.set_title("Remote Sensor Two")
        self.axl2.set_xlabel("Time")
        self.axl2.grid(True)
        
        self.gpsSecListTwo = []
        self.indexTwo = count()
        # data from remote sensor 2
        # pressure, temp, humidity, solar voltage
        self.g2Data = [[], [], [], []]
        self.g2DataLines = []
        for j in range(4):
            self.g2DataLines.append(self.axl2.plot([],[])[0])
        
    def animate(self, i, gps, data, lines, ax, index):
        if (int(self.xbee.sensNum) == 2):
            
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
            self.aniTwo = FuncAnimation(self.fig2, self.animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListTwo, self.g2Data, self.g2DataLines, self.axl2, self.indexTwo))
        
    def returnGraphG2(self):
        self.fig2.legend((self.g2DataLines[0], self.g2DataLines[1], self.g2DataLines[2], self.g2DataLines[3]), ('Temperature', 'Pressure', 'Humidity', 'Solar Voltage'), 'upper right')
        return self.fig2