import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

gpsSecList = []
# data from remote sensor 1
pressureOneList = [] # should be divided by 10000 from rawdata, likely 9-11
tempOneList = [] # likely 15-25
humidityOneList = [] # multiply by 10 from rawdata, likely 4-9
solarVoltOneList = [] # likely 5-10

index = count()


def animate(i):
    gpsSecList.append(next(index))
    pressureOneList.append(random.randint(9, 11))
    tempOneList.append(random.randint(15, 25))
    humidityOneList.append(random.randint(4, 9)) 
    solarVoltOneList.append(random.randint(5, 10))  
    plt.cla()
    plt.plot(gpsSecList, pressureOneList, label='Pressure[*10kPa]')
    plt.plot(gpsSecList, tempOneList, label='Temp[C]')
    plt.plot(gpsSecList, humidityOneList, label='Humidity[:10%]')
    plt.plot(gpsSecList, solarVoltOneList, label='Solar Voltage[V]')
    plt.xlabel('Time')
    plt.legend(loc='upper left')
    plt.title('Remote Sensor One')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, frames=None, cache_frame_data=False, interval=1000)

plt.show()