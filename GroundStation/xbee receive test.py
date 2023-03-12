import serial
import time

#Global Variables For Parsing
sensNum = ""
gpsHour = ""
gpsMin = ""
gpsSec = ""
gpsMSec = ""
gpsLong = ""
gpsLat = ""
gpsSpeed = ""
gpsAngle = ""
gpsAltitude = ""
gpsSatellites = ""
tempOne = ""
pressureOne = ""
humidityOne = ""
solarVoltOne = ""
tempTwo = ""
pressureTwo = ""
humidityTwo = ""
solarVoltTwo = ""

ser = serial.Serial(port = "COM3", baudrate = 9600)

while True:

    buffer = ser.readline().decode()
    print(buffer)

    tempBuffer = buffer.split(',')
    sensNum = tempBuffer[0]
    gpsHour =  tempBuffer[1]
    gpsMin =  tempBuffer[2]
    gpsSec =  tempBuffer[3]
    gpsMSec =  tempBuffer[4]
    gpsLong =  tempBuffer[5]
    gpsLat = tempBuffer[6]
    gpsSpeed = tempBuffer[7]
    gpsAngle = tempBuffer[8]
    gpsAltitude = tempBuffer[9]
    gpsSatellites = tempBuffer[10]

    if sensNum == "1":
        #print("Sensor One Data Received")
        tempOne = tempBuffer[11]
        pressureOne = tempBuffer [12]
        humidityOne = tempBuffer[13]
        solarVoltOne = tempBuffer[14]
    if sensNum == "2":
        #print("Sensor Two Data Received")
        tempTwo = tempBuffer[11]
        pressureTwo = tempBuffer [12]
        humidityTwo = tempBuffer[13]
        solarVoltTwo = tempBuffer[14]

    rs1_data_counter = tempBuffer[15]
    rs2_data_counter = tempBuffer[16]
    gps_data_counter = tempBuffer[17]

    # if sensNum == "1":
    #     print("sensNum: %s, gpsHour: %s, gpsMin: %s, gpsSec: %s, gpsMSec: %s, gpsLong: %s, gpsLat: %s, gpsSpeed: %s, gpsAngle: %s, gpsAltitude: %s, gpsSatellites: %s, temp: %s, pressure: %s, humidity: %s, solarVolt: %s, rs1_data_counter: %s, rs2_data_counter: %s, gps_data_counter: %s" 
    #     % (sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, tempOne, pressureOne, humidityOne, solarVoltOne, rs1_data_counter, rs2_data_counter, gps_data_counter))

    # if sensNum == "2":
    #     print("sensNum: %s, gpsHour: %s, gpsMin: %s, gpsSec: %s, gpsMSec: %s, gpsLong: %s, gpsLat: %s, gpsSpeed: %s, gpsAngle: %s, gpsAltitude: %s, gpsSatellites: %s, temp: %s, pressure: %s, humidity: %s, solarVolt: %s, rs1_data_counter: %s, rs2_data_counter: %s, gps_data_counter: %s" 
    #     % (sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, tempTwo, pressureTwo, humidityTwo, solarVoltTwo, rs1_data_counter, rs2_data_counter, gps_data_counter))

    time.sleep(1)

#ser.close()