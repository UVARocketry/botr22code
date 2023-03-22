import random
from itertools import count
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style

print("hello!!!")

def animate(i, gps, data, lines, ax):
    gps.append(next(index))
    
    print("how many damn times is this running")
    
    data[0].append(random.randint(9, 11))
    data[1].append(random.randint(15, 25))
    data[2].append(random.randint(4, 9))
    data[3].append(random.randint(5, 10))
    
    for j in range(4):
        lines[j].set_data(gps, data[j])
        ax.relim()
        ax.autoscale_view()

class GroundSensors:
    def __init__(self):
        self.plt1 = plt
        self.plt2 = plt
        
        style.use('fivethirtyeight')
        
        self.fig1, self.axl1 = self.plt1.subplots()
        self.axl1.set_ylim(ymin = 0, ymax = 30)
        self.axl1.set_title("Remote Sensor One")
        self.axl1.set_xlabel("Time")
        self.axl1.grid(True)
        
        self.fig2, self.axl2 = self.plt2.subplots()
        self.axl2.set_ylim(ymin = 0, ymax = 30)
        self.axl2.set_title("Remote Sensor Two")
        self.axl2.set_xlabel("Time")
        self.axl2.grid(True)
        
        self.gpsSecListOne = []
        self.indexOne = count()
        # data from remote sensor 1
        # pressure, temp, humidity, solar voltage
        self.g1Data = [[], [], [], []]
        self.g1DataLines = []
        for j in range(4):
            self.g1DataLines.append(self.axl1.plot([],[])[0])
            
        self.axl1.legend()
        
        self.gpsSecListTwo = []
        self.indexTwo = count()
        # data from remote sensor 2
        # pressure, temp, humidity, solar voltage
        self.g2Data = [[], [], [], []]
        self.g2DataLines = []
        for j in range(4):
            self.g2DataLines.append(self.axl2.plot([],[])[0], label='testlabel2')
            
        self.axl2.legend()
        
    def returnGraphG1(self):
        self.aniOne = FuncAnimation(self.fig1, animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListOne, self.g1Data, self.g1DataLines, self.axl1))
        
        return self.fig1

    def returnGraphG2(self):
        self.aniTwo = FuncAnimation(self.fig2, animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListTwo, self.g2Data, self.g2DataLines, self.axl2))   
        
        return self.fig2