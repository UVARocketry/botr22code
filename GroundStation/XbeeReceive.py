import serial
import time

class Xbee:
    def __init__(self):
        self.sensNum = "0"
        self.gpsHour = ""
        self.gpsMin = ""
        self.gpsSec = ""
        self.gpsMSec = ""
        self.gpsLong = ""
        self.gpsLat = ""
        self.gpsSpeed = ""
        self.gpsAngle = ""
        self.gpsAltitude = ""
        self.gpsSatellites = ""
        self.temp = ""
        self.pressure = ""
        self.humidity = ""
        self.solarVolt = ""
        self.currentApogee = 0
        
        self.currentState = 0
        self.stateNotReadyForFlight = 0
        self.stateReadyForFlight = 1
        self.stateInFlight = 2
    
    def receive(self):
        self.buffer = self.ser.readline().decode()
        print(self.buffer)

        self.tempBuffer = self.buffer.split(',')
        self.sensNum = self.tempBuffer[0]
        self.gpsHour =  self.tempBuffer[1]
        self.gpsMin =  self.tempBuffer[2]
        self.gpsSec =  self.tempBuffer[3]
        self.gpsMSec =  self.tempBuffer[4]
        self.gpsLong =  self.tempBuffer[5]
        self.gpsLat = self.tempBuffer[6]
        self.gpsSpeed = self.tempBuffer[7]
        self.gpsAngle = self.tempBuffer[8]
        self.gpsAltitude = self.tempBuffer[9]
        self.gpsSatellites = self.tempBuffer[10]
        self.temp = self.tempBuffer[11]
        self.pressure = self.tempBuffer [12]
        self.humidity = self.tempBuffer[13]
        self.solarVolt = self.tempBuffer[14]
        self.rs1_data_counter = self.tempBuffer[15]
        self.rs2_data_counter = self.tempBuffer[16]
        self.gps_data_counter = self.tempBuffer[17]
        
        if float(self.gpsAltitude) > self.currentApogee:
            self.currentApogee = float(self.gpsAltitude)
        
        #Change parameters as necessary
        if float(self.gpsLong) == 0 and int(float(self.sensNum)) == 0:
            #Current State = 0
            self.currentState = self.stateNotReadyForFlight
        elif float(self.gpsLong) != 0 and int(float(self.sensNum)) != 0 and int(float(self.gpsSpeed)) < 10:
            #Current State = 1
            self.currentState = self.stateReadyForFlight
        else:
            #Current State = 2
            self.currentState = self.stateInFlight
        time.sleep(1) 

    def returnSensData(self):
        return [self.sensNum, self.temp, self.pressure, self.humidity, self.solarVolt]
    
    def returnGPSTime(self):
        return self.gpsHour + ":" + self.gpsMin + ":" + self.gpsSec

    def returnGPSData(self):
        return [self.gpsLong, self.gpsLat]

    def returnRawData(self):
        return [self.sensNum, self.gpsHour, self.gpsMin, self.gpsSec, self.gpsMSec, self.gpsLong, self.gpsLat, self.gpsSpeed, self.gpsAngle, self.gpsAltitude, self.gpsSatellites, self.temp, self.pressure, self.humidity, self.solarVolt, self.rs1_data_counter, self.rs2_data_counter, self.gps_data_counter]

    def returnState(self):
        return self.currentState
    
    def openSerPort(self):
        self.ser = serial.Serial(port = "COM3", baudrate = 9600)
    
    def closeSerPort(self):
        self.ser.close()
    
# xbee = Xbee()

# while True:
#     xbee.receive()
#     print(xbee.returnRawData())
#     print(xbee.returnSensData())
#     print(xbee.returnState())