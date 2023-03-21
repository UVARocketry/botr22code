import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
        
    def animation(self, isGraphOne):
        def animate(i):
            if (isGraphOne):
                self.gpsSecListOne.append(next(self.indexOne))
                self.pressureOneList.append(random.randint(9, 11))
                self.tempOneList.append(random.randint(15, 25))
                self.humidityOneList.append(random.randint(4, 9)) 
                self.solarVoltOneList.append(random.randint(5, 10))
                
                self.plt1.cla()
                self.plt1.plot(self.gpsSecListOne, self.pressureOneList, label='Pressure[*10kPa]')
                self.plt1.plot(self.gpsSecListOne, self.tempOneList, label='Temp[C]')
                self.plt1.plot(self.gpsSecListOne, self.humidityOneList, label='Humidity[:10%]')
                self.plt1.plot(self.gpsSecListOne, self.solarVoltOneList, label='Solar Voltage[V]')
                self.plt1.xlabel('Time')
                self.plt1.legend(loc='upper left')
                self.plt1.title('Remote Sensor One')
                self.plt1.tight_layout() 
            else:
                self.gpsSecListTwo.append(next(self.indexTwo))
                self.pressureTwoList.append(random.randint(9, 11))
                self.tempTwoList.append(random.randint(15, 25))
                self.humidityTwoList.append(random.randint(4, 9)) 
                self.solarVoltTwoList.append(random.randint(5, 10))
                
                self.plt2.cla()
                self.plt2.plot(self.gpsSecListTwo, self.pressureTwoList, label='Pressure[*10kPa]')
                self.plt2.plot(self.gpsSecListTwo, self.tempTwoList, label='Temp[C]')
                self.plt2.plot(self.gpsSecListTwo, self.humidityTwoList, label='Humidity[:10%]')
                self.plt2.plot(self.gpsSecListTwo, self.solarVoltTwoList, label='Solar Voltage[V]')
                self.plt2.xlabel('Time')
                self.plt2.legend(loc='upper left')
                self.plt2.title('Remote Sensor Two')
                self.plt2.tight_layout()
        if (isGraphOne):
            self.aniOne = FuncAnimation(self.plt1.gcf(), animate, frames=None, cache_frame_data=False, interval=1000)
        else:
            self.aniTwo = FuncAnimation(self.plt2.gcf(), animate, frames=None, cache_frame_data=False, interval=1000)
        
    def returnGraphG1(self):
        return self.plt1.gcf()

    def returnGraphG2(self):
        return self.plt2.gcf()