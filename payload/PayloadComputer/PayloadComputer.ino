#include <Adafruit_GPS.h>

//may be defined to incorrect serial ports rn, will fix
#define XbeeR Serial1
#define XbeeT Serial2
#define GPSSerial Serial3

// Connect to the GPS on the hardware port
Adafruit_GPS GPS(&GPSSerial);
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false

uint32_t timer = millis();

//State Estimation for rocket based on GPS Data
int currState = 0;
int prevlat = 0;
int launchPad = 0;
int takeoff = 1;
int ascent = 2;
int apogee = 3;
int descent = 4;
int landing = 5;


void setup() {
  //Start all serial ports
  Serial.begin(115200);
  XbeeR.begin(9600);
  //Serial.println("Xbee Receive Serial begun!");
  XbeeT.begin(9600);
  //Serial.println("Xbee Transmit Serial begun!");
  GPS.begin(9600);
  //Serial.println("GPS Serial begun!");

  
  // turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // Request updates on antenna status, comment out to keep quiet
  //GPS.sendCommand(PGCMD_ANTENNA);

  //get latitude once (used for state estimation)
  prevlat = GPS.latitude;
  delay(1000);

}


void loop() {

  // read data from the GPS in the 'main loop'
  char c = GPS.read();
  // if a sentence is received, we can check the checksum, parse it...
  if (GPS.newNMEAreceived()) {
    // a tricky thing here is if we print the NMEA sentence, or data
    // we end up not listening and catching other sentences!
    // so be very wary if using OUTPUT_ALLDATA and trying to print out data
    Serial.print(GPS.lastNMEA()); // this also sets the newNMEAreceived() flag to false
    if (!GPS.parse(GPS.lastNMEA())) // this also sets the newNMEAreceived() flag to false
      return; // we can fail to parse a sentence in which case we should just wait for another
  }
  //uncommented gps data that we probably don't need, may readd/delete late
  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 2000) {
    timer = millis(); // reset the timer

    //state estimation
    switch(currState){
      case 0:
      //launch?
      if(GPS.latitude - prevlat != 0){
        currState = 1;
       }
        break;
            
      case 1:
      //ascent?
      if(GPS.latitude != 0){
        currState = 2;
      }
        break;

      case 2:
      //apogee?
      if(GPS.latitude - prevlat == 0){
        currState = 3;
      }
        break;

      case 3:
      //descent?              
      if(GPS.latitude != 0){
        currState = 4;
      }
        break;

      case 4:
      //landing?
      if(GPS.latitude - prevlat == 0){
        currState = 5;
      }
        break;

      default:
        break;
      }

    if(currState = 4){
      if(XbeeR.available()){
        if(XbeeT.available()){
          //Transmits Remote Sensor Data
          XbeeT.print(XbeeR.read());
        
          //Transmits GPS Data
          XbeeT.println("Time: ");
          if (GPS.hour < 10) { XbeeT.print('0'); }
          XbeeT.print(GPS.hour, DEC); XbeeT.print(':');
          if (GPS.minute < 10) { XbeeT.print('0'); }
          XbeeT.print(GPS.minute, DEC); XbeeT.print(':');
          if (GPS.seconds < 10) { XbeeT.print('0'); }
          XbeeT.print(GPS.seconds, DEC); XbeeT.print('.');
          //XbeeT.print(GPS.milliseconds);
          //XbeeT.print("Date: ");
          //XbeeT.print(GPS.day, DEC); XbeeT.print('/');
          //XbeeT.print(GPS.month, DEC); XbeeT.print("/20");
          //XbeeT.println(GPS.year, DEC);
          //XbeeT.print("Fix: "); XbeeT.print((int)GPS.fix);
          //XbeeT.print(" quality: "); XbeeT.println((int)GPS.fixquality);
          if (GPS.fix) {
            XbeeT.print("Location: ");
            XbeeT.print(GPS.latitude, 4); XbeeT.print(GPS.lat);
            XbeeT.print(", ");
            XbeeT.print(GPS.longitude, 4); XbeeT.print(GPS.lon); //don't know why there's two prints
            XbeeT.print("Speed (knots): "); XbeeT.println(GPS.speed); //don't know why there's two prints
            XbeeT.print("Angle: "); XbeeT.println(GPS.angle);
            XbeeT.print("Altitude: "); XbeeT.println(GPS.altitude);
            XbeeT.print("Satellites: "); XbeeT.println((int)GPS.satellites);
            //XbeeT.print("Antenna status: "); XbeeT.println((int)GPS.antenna);
            prevlat = GPS.latitude;
          }
          XbeeT.println("Current State: " + currState);
        }
      }
    }  
  }
}
