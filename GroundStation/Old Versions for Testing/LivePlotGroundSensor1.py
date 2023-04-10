import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GroundSensorOne:
    def __init__(self):
        plt.style.use('fivethirtyeight')

        self.gpsSecList = []
        # data from remote sensor 1
        self.pressureOneList = [] # should be divided by 10000 from rawdata, likely 9-11
        self.tempOneList = [] # likely 15-25
        self.humidityOneList = [] # multiply by 10 from rawdata, likely 4-9
        self.solarVoltOneList = [] # likely 5-10

        self.index = count()

    def animation(self):
        def animate(i):
            self.gpsSecList.append(next(self.index))
            self.pressureOneList.append(random.randint(9, 11))
            self.tempOneList.append(random.randint(15, 25))
            self.humidityOneList.append(random.randint(4, 9)) 
            self.solarVoltOneList.append(random.randint(5, 10)) 
            
            # Why does this need to be in the animate function???
            plt.cla()
            plt.plot(self.gpsSecList, self.pressureOneList, label='Pressure[*10kPa]')
            plt.plot(self.gpsSecList, self.tempOneList, label='Temp[C]')
            plt.plot(self.gpsSecList, self.humidityOneList, label='Humidity[:10%]')
            plt.plot(self.gpsSecList, self.solarVoltOneList, label='Solar Voltage[V]')
            plt.xlabel('Time')
            plt.legend(loc='upper left')
            plt.title('Remote Sensor One')
            plt.tight_layout() 
        
        self.ani = FuncAnimation(plt.gcf(), animate, frames=None, cache_frame_data=False, interval=1000)

    def returnGraphG1(self):
        return plt.gcf()
    
    def showGraph1(self):
        plt.show()
        
# g1 = GroundSensorOne()
# g1.animation()
# g1.showGraph1()
# plt.show()