import serial
import time

#
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
temp = ""
pressure =  ""
humidity = ""
solarVolt = ""
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
    temp = tempBuffer[11]
    pressure = tempBuffer [12]
    humidity = tempBuffer[13]
    solarVolt = tempBuffer[14]
    rs1_data_counter = tempBuffer[15]
    rs2_data_counter = tempBuffer[16]
    gps_data_counter = tempBuffer[17]

    if sensNum == "1":
        print("Sensor One Data Received")
        tempOne = temp;
        pressureOne = pressure;
        humidityOne = humidity;
        solarVoltOne = solarVolt;
    if sensNum == "2":
        print("Sensor Two Data Received")
        tempTwo = temp;
        pressureTwo = pressure;
        humidityTwo = humidity;
        solarVoltTwo = solarVolt;
    
    print("sensNum: %s, gpsHour: %s, gpsMin: %s, gpsSec: %s, gpsMSec: %s, gpsLong: %s, gpsLat: %s, gpsSpeed: %s, gpsAngle: %s, gpsAltitude: %s, gpsSatellites: %s, temp: %s, pressure: %s, humidity: %s, solarVolt: %s, rs1_data_counter: %s, rs2_data_counter: %s, gps_data_counter: %s" 
    % (sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, temp, pressure, humidity, solarVolt, rs1_data_counter, rs2_data_counter, gps_data_counter))

    time.sleep(1)

    if(keyboard.is_pressed('q')):
        print("User needs to quit")
        break

ser.close()
