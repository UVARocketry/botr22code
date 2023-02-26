#include <Adafruit_GPS.h>
//#include <SPI.h>
//#include <SD.h>

int commaCounter = 0;
int currentIndexInBuffer = 0;
char remoteDataBuffer [40];
char buffer [120];

//pay attention to correct ports
#define XbeeR Serial1
#define GPSSerial Serial2
#define XbeeT Serial3

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();

void setup() {
  //Start all serial ports
  Serial.begin(115200);
  XbeeR.begin(9600);
  //Serial.println("Xbee Receive Serial begun!");
  XbeeT.begin(9600);
  //Serial.println("Xbee Transmit Serial begun!");
  GPS.begin(9600);
  //Serial.println("GPS Serial begun!");

  //change to the correct cs pin
  //SD.begin(cspin);
  
  // turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // Request updates on antenna status, comment out to keep quiet
  //GPS.sendCommand(PGCMD_ANTENNA);

  delay(1000);

}


void loop() {

  commaCounter = 0;
  currentIndexInBuffer = 0;
  remoteDataBuffer[0] = { 0 };
  buffer[0] = { 0 };

  remoteDataBuffer [0] = XbeeR.read();
    //not sure if '1' or 1
    if(remoteDataBuffer[0] == '1' || '2'){
      while(commaCounter < 5){
        currentIndexInBuffer++;
        remoteDataBuffer [currentIndexInBuffer] = XbeeR.read();
        if(remoteDataBuffer [currentIndexInBuffer] == ','){
          commaCounter++;
        }
      }
      //gets three chars more after the forth comma
      for(int i = 0; i < 3; i++){
        currentIndexInBuffer++;
        remoteDataBuffer [currentIndexInBuffer] == XbeeR.read();
      }
    }
  //parses all the commas
  char *sensNum = strtok(remoteDataBuffer, ",");
  char *pressure = strtok(NULL, ",");
  char *temp = strtok(NULL, ",");
  char *humidity = strtok(NULL, ",");
  char *solarVolt = strtok(NULL, ",");
  //is timer necessary to prevent the processor from overloading?
  char gpsHour[] = GPS.hour;
  char gpsMin[] = GPS.minute;
  char gpsSec[] = GPS.seconds;
  char gpsMSec [] = GPS.milliseconds;
  char gpsLat [] = GPS.latitude;
  char gpsLong [] = GPS.longitude;
  char gpsSpeed [] = GPS.speed;
  char gpsAngle [] = GPS.angle;
  char gpsAltitude [] = GPS.altitude;
  char gpsSatellites [] = GPS.satellites;

  //concatenates the remote sensor and gps data
  char buffer [150];
  sprintf(buffer, "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s", 
  sensNum, pressure, temp, humidity, solarVolt, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLat, gpsLong, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites);
  XbeeT.println(buffer);

  //data logging
  //payloadDataFile = SD.open("payloadData.txt", FILE_WRITE);
  //payloadDataFile.write(buffer);
  //SD.close("payloadData.txt");


  //Will delete later: keep for reference
  //uncommented gps data that we probably don't need, may read/delete late
  // approximately every 2 seconds or so, print out the current stats
  // if (millis() - timer > 2000) {
  //   timer = millis(); // reset the timer
  //     if(XbeeR.available()){
  //       if(XbeeT.available()){
  //         //Transmits Remote Sensor Data
  //         XbeeT.print(XbeeR.read());
        
  //         //Transmits GPS Data
  //         XbeeT.println("Time: ");
  //         if (GPS.hour < 10) { XbeeT.print('0'); }
  //         XbeeT.print(GPS.hour, DEC); XbeeT.print(':');
  //         if (GPS.minute < 10) { XbeeT.print('0'); }
  //         XbeeT.print(GPS.minute, DEC); XbeeT.print(':');
  //         if (GPS.seconds < 10) { XbeeT.print('0'); }
  //         XbeeT.print(GPS.seconds, DEC); XbeeT.print('.');
  //         //XbeeT.print(GPS.milliseconds);
  //         //XbeeT.print("Date: ");
  //         //XbeeT.print(GPS.day, DEC); XbeeT.print('/');
  //         //XbeeT.print(GPS.month, DEC); XbeeT.print("/20");
  //         //XbeeT.println(GPS.year, DEC);
  //         //XbeeT.print("Fix: "); XbeeT.print((int)GPS.fix);
  //         //XbeeT.print(" quality: "); XbeeT.println((int)GPS.fixquality);
  //         if (GPS.fix) {
  //           XbeeT.print("Location: ");
  //           XbeeT.print(GPS.latitude, 4); XbeeT.print(GPS.lat);
  //           XbeeT.print(", ");
  //           XbeeT.print(GPS.longitude, 4); XbeeT.print(GPS.lon); //don't know why there's two prints
  //           XbeeT.print("Speed (knots): "); XbeeT.println(GPS.speed); //don't know why there's two prints
  //           XbeeT.print("Angle: "); XbeeT.println(GPS.angle);
  //           XbeeT.print("Altitude: "); XbeeT.println(GPS.altitude);
  //           XbeeT.print("Satellites: "); XbeeT.println((int)GPS.satellites);
  //           //XbeeT.print("Antenna status: "); XbeeT.println((int)GPS.antenna);
  //         }
  //       }
  //     }
  //   }  
  //}
}
