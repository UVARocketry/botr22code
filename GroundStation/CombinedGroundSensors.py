import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i, gps, pressure, temp, humidity, solar, index, plt):
    # make sure to do next(self.index1 or self.index2) before calling this
    gps.append(next(index))
    pressure.append(random.randint(9, 11))
    temp.append(random.randint(15, 25))
    humidity.append(random.randint(4, 9))
    solar.append(random.randint(5, 10))

    plt.cla()
    plt.plot(gps, pressure,
             label='Pressure[*10kPa]')
    plt.plot(gps, temp, label='Temp[C]')
    plt.plot(gps, humidity, label='Humidity[:10%]')
    plt.plot(gps, solar, label='Solar Voltage[V]')
    plt.xlabel('Time')
    plt.legend(loc='upper left')
    plt.title('Remote Sensor One')
    plt.tight_layout()

    # self.gpsSecListTwo.append(next(self.indexTwo))
    # self.pressureTwoList.append(random.randint(9, 11))
    # self.tempTwoList.append(random.randint(15, 25))
    # self.humidityTwoList.append(random.randint(4, 9))
    # self.solarVoltTwoList.append(random.randint(5, 10))

    # self.plt2.cla()
    # self.plt2.plot(self.gpsSecListTwo, self.pressureTwoList, label='Pressure[*10kPa]')
    # self.plt2.plot(self.gpsSecListTwo, self.tempTwoList, label='Temp[C]')
    # self.plt2.plot(self.gpsSecListTwo, self.humidityTwoList, label='Humidity[:10%]')
    # self.plt2.plot(self.gpsSecListTwo, self.solarVoltTwoList, label='Solar Voltage[V]')
    # self.plt2.xlabel('Time')
    # self.plt2.legend(loc='upper left')
    # self.plt2.title('Remote Sensor Two')
    # self.plt2.tight_layout()

class GroundSensors:
    def __init__(self):
        self.plt1 = plt
        self.plt2 = plt
        
        self.plt1.style.use('fivethirtyeight')
        self.plt2.style.use('fivethirtyeight')
        
        self.gpsSecListOne = []
        # data from remote sensor 1
        self.pressureOneList = [] # should be divided by 10000 from rawdata, likely 9-11
        self.tempOneList = [] # likely 15-25
        self.humidityOneList = [] # multiply by 10 from rawdata, likely 4-9
        self.solarVoltOneList = [] # likely 5-10
        self.indexOne = count()
        
        self.gpsSecListTwo = []
        # data from remote sensor 2
        self.pressureTwoList = []
        self.tempTwoList = []
        self.humidityTwoList = []
        self.solarVoltTwoList = []
        self.indexTwo = count()
        
    # def animation(self):
    #     self.aniOne = FuncAnimation(self.plt1.gcf(), animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListOne, self.pressureOneList, self.tempOneList, self.humidityOneList, self.solarVoltOneList, self.indexOne, self.plt1))
        
    #     self.aniTwo = FuncAnimation(self.plt2.gcf(), animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListTwo, self.pressureTwoList, self .tempTwoList, self.humidityTwoList, self.solarVoltTwoList, self.indexTwo, self.plt2))   
        
    def returnGraphG1(self):
        self.aniOne = FuncAnimation(self.plt1.gcf(), animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListOne, self.pressureOneList, self.tempOneList, self.humidityOneList, self.solarVoltOneList, self.indexOne, self.plt1))
        
        return self.plt1.gcf()

    def returnGraphG2(self):
        self.aniTwo = FuncAnimation(self.plt2.gcf(), animate, frames=None, cache_frame_data=False, interval=1000, fargs=(self.gpsSecListTwo, self.pressureTwoList, self .tempTwoList, self.humidityTwoList, self.solarVoltTwoList, self.indexTwo, self.plt2))   
        
        return self.plt2.gcf()