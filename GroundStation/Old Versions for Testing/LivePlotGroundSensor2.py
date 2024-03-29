import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class GroundSensorTwo:
    def __init__(self):
        plt.style.use('fivethirtyeight')

        self.gpsSecList = []
        # data from remote sensor 2
        self.pressureTwoList = []
        self.tempTwoList = []
        self.humidityTwoList = []
        self.solarVoltTwoList = []

        self.index = count()
    
    def animation(self):
        def animate2(i):
            self.gpsSecList.append(next(self.index))
            self.pressureTwoList.append(random.randint(9, 11))
            self.tempTwoList.append(random.randint(15, 25))
            self.humidityTwoList.append(random.randint(4, 9)) 
            self.solarVoltTwoList.append(random.randint(5, 10))
            
            plt.cla()
            plt.plot(self.gpsSecList, self.pressureTwoList, label='Pressure[*10kPa]')
            plt.plot(self.gpsSecList, self.tempTwoList, label='Temp[C]')
            plt.plot(self.gpsSecList, self.humidityTwoList, label='Humidity[:10%]')
            plt.plot(self.gpsSecList, self.solarVoltTwoList, label='Solar Voltage[V]')
            plt.xlabel('Time')
            plt.legend(loc='upper left')
            plt.title('Remote Sensor Two')
            plt.tight_layout()

        self.ani2 = FuncAnimation(plt.gcf(), animate2, frames=None, cache_frame_data=False, interval=1000)

    def returnGraphG2(self):
        return plt.gcf()
    
    def showGraph2(self):
        plt.show()

# g2 = GroundSensorTwo()
# g2.animation()
# g2.showGraph2()