import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

gpsSecList = []
# data from gps
gpsLatList = [] # should be divided by 1000 from rawdata, likely 36-40
gpsLongList = [] # should be divided by 1000 from rawdata, likely 75-80

index = count()


def animate3(i):
    gpsSecList.append(next(index))
    gpsLatList.append(random.randint(36, 40))
    gpsLongList.append(random.randint(75, 80))
    plt.cla()
    plt.plot(gpsSecList, gpsLatList, label='Latitude')
    plt.plot(gpsSecList, gpsLongList, label='Longitude')
    plt.xlabel('Time')
    plt.legend(loc='upper left')
    plt.title('GPS')
    plt.tight_layout()


ani3 = FuncAnimation(plt.gcf(), animate3, frames=None, cache_frame_data=False, interval=1000)

plt.show()