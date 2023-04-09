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

#State Estimation
currentState = 0
stateNotReadyForFlight = 0
stateReadyForFlight = 1
stateInFlight = 2


ser = serial.Serial(port = "COM7", baudrate = 9600)

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

    #Change parameters as necessary
    # if gpsLong == 0 and sensNum == 0:
    #     #Current State = 0
    #     currentState = stateNotReadyForFlight
    # elif gpsLong != 0 and sensNum != 0 and gpsSpeed < 10:
    #     #Current State = 1
    #     currentState = stateReadyForFlight
    # else:
    #     #Current State = 2
    #     currentState = stateInFlight
    time.sleep(1)

    if currentState == 0:
        print("Not Ready for flight")
        #If not ready for flight, then the graphs don't have to be shown/timer doesn't start yet
    elif currentState == 1:
        print("Ready for flight")
        #If ready for flight, graphs can start to be shown/timer can start
    else:
        print("In Flight")
        #If in flight, graph can continue to be shown/timer can continue to run

#ser.close()