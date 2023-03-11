import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

gpsSecList = []
# data from remote sensor 2
pressureTwoList = []
tempTwoList = []
humidityTwoList = []
solarVoltTwoList = []

index = count()


def animate2(i):
    gpsSecList.append(next(index))
    pressureTwoList.append(random.randint(9, 11))
    tempTwoList.append(random.randint(15, 25))
    humidityTwoList.append(random.randint(4, 9)) 
    solarVoltTwoList.append(random.randint(5, 10))  
    plt.cla()
    plt.plot(gpsSecList, pressureTwoList, label='Pressure[*10kPa]')
    plt.plot(gpsSecList, tempTwoList, label='Temp[C]')
    plt.plot(gpsSecList, humidityTwoList, label='Humidity[:10%]')
    plt.plot(gpsSecList, solarVoltTwoList, label='Solar Voltage[V]')
    plt.xlabel('Time')
    plt.legend(loc='upper left')
    plt.title('Remote Sensor Two')
    plt.tight_layout()


ani2 = FuncAnimation(plt.gcf(), animate2, frames=None, cache_frame_data=False, interval=1000)

plt.show()