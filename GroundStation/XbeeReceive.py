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
        self.tempOne = ""
        self.pressureOne = ""
        self.humidityOne = ""
        self.solarVoltOne = ""
        self.tempTwo = ""
        self.pressureTwo = ""
        self.humidityTwo = ""
        self.solarVoltTwo = ""
        self.currentApogee = 0
        
        self.currentState = 0
        self.stateNotReadyForFlight = 0
        self.stateReadyForFlight = 1
        self.stateInFlight = 2
    
    def receive(self):
        self.buffer = ser.readline().decode()
        #print(buffer)

        self.tempBuffer = buffer.split(',')
        self.sensNum = tempBuffer[0]
        self.gpsHour =  tempBuffer[1]
        self.gpsMin =  tempBuffer[2]
        self.gpsSec =  tempBuffer[3]
        self.gpsMSec =  tempBuffer[4]
        self.gpsLong =  tempBuffer[5]
        self.gpsLat = tempBuffer[6]
        self.gpsSpeed = tempBuffer[7]
        self.gpsAngle = tempBuffer[8]
        self.gpsAltitude = tempBuffer[9]
        self.gpsSatellites = tempBuffer[10]

        if self.sensNum == "1":
            #print("Sensor One Data Received")
            self.tempOne = tempBuffer[11]
            self.pressureOne = tempBuffer [12]
            self.humidityOne = tempBuffer[13]
            self.solarVoltOne = tempBuffer[14]
        if self.sensNum == "2":
            #print("Sensor Two Data Received")
            self.tempTwo = tempBuffer[11]
            self.pressureTwo = tempBuffer [12]
            self.humidityTwo = tempBuffer[13]
            self.solarVoltTwo = tempBuffer[14]

        
        self.rs1_data_counter = tempBuffer[15]
        self.rs2_data_counter = tempBuffer[16]
        self.gps_data_counter = tempBuffer[17]
        
        if(self.gpsAltitude > self.currentApogee):
            self.currentApogee = self.gpsAltitude
        
        #Change parameters as necessary
        if self.gpsLong == 0 and self.sensNum == 0:
            #Current State = 0
            self.currentState = self.stateNotReadyForFlight
        elif self.gpsLong != 0 and self.sensNum != 0 and self.gpsSpeed < 10:
            #Current State = 1
            self.currentState = self.stateReadyForFlight
        else:
            #Current State = 2
            self.currentState = self.stateInFlight
        time.sleep(1) 
        
    def returnState(self):
        return self.currentState
    
    