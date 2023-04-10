import random
from itertools import count
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style
import XbeeReceive
import datetime

class GPS:
    def __init__(self, xbee):
        self.xbee = xbee
        self.plt3 = plt

        style.use('fivethirtyeight')
        
        # Declares gps graph
        # Don't know if subplots are necessary for the gps graph
        self.fig3, self.axl3 = self.plt3.subplots()
        self.axl3.set_title("GPS Data")
        self.axl3.set_xlabel("Time")
        self.axl3.grid(True)

        self.gpsTimeList = []

        # data from gps
        self.indexThree = count()
        self.g3Data = [[], []]
        self.g3DataLines = []
        for j in range(2):
            self.g3DataLines.append(self.axl3.plot([],[])[0])

    def animate(self, i, gps, data, lines, ax, index):
        gps.append(next(index))
        
        data[0].append(float(self.xbee.returnGPSData()[0]) / 100)
        data[1].append(float(self.xbee.returnGPSData()[1]) / 100)
        
        for j in range(2):
            lines[j].set_data(gps, data[j])
            ax.relim()
            ax.autoscale_view()

    def animation(self):
        # self.state = int(float(self.xbee.returnState()))
        
        # if ((self.state == 1) | (self.state == 2)):
            self.aniThree = FuncAnimation(self.fig3, self.animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsTimeList, self.g3Data, self.g3DataLines, self.axl3, self.indexThree))
    
    def returnGraphG3(self):
        self.fig3.legend((self.g3DataLines[0], self.g3DataLines[1]), ('Longitude', 'Latitude'), 'upper right')
        return self.fig3