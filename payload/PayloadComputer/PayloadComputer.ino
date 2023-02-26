//LIBRARY INCLUDES
#include <Adafruit_GPS.h>

//SERIAL PORT DEFINITIONS
//may be defined to incorrect serial ports rn, will fix
#define XbeeR Serial1
#define XbeeT Serial2
#define GPSSerial Serial3
#define LEDPIN 13

//DEBUG FLAGS
//set any of these to 'true' for status updates to be sent to the USB Serial Console
//alternatively, you could use the debugger
#define SERIAL_PORT_DEBUG true
#define GPS_DEBUG false
#define TRANSMITT_DEBUG true

//FUNCTION HEADERS
void transmittAllData();
bool waitGPSfix();

//Initializing GPS Object using hardware serial port
Adafruit_GPS GPS(&GPSSerial);

//Ran once by microcontroller
void setup()
{
  // indicate that the payload computer is not ready to fly
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, HIGH);

  //STARTING SERIAL PORTS
  //USB Serial
  Serial.begin(115200);
  if(SERIAL_PORT_DEBUG) Serial.println("USB Serial begun!");

  //Xbee Reciever Serial
  XbeeR.begin(9600);
  if(SERIAL_PORT_DEBUG) Serial.println("Xbee Receive Serial begun!");

  //Xbee Transmitter Serial
  XbeeT.begin(9600);
  if(SERIAL_PORT_DEBUG) Serial.println("Xbee Transmit Serial begun!");

  //GPS Serial
  GPS.begin(9600);
  if(SERIAL_PORT_DEBUG) Serial.println("GPS Serial begun!");

  delay(2000); //give some time for all ports to open connection

  //GPS SETUP
  // turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ); // 1 Hz update rate
  // Request updates on antenna status, comment out to keep quiet
  //GPS.sendCommand(PGCMD_ANTENNA);

  delay(500); //give some time for commands above to run

  //TODO: create functions here that run until RS data is being acquired and GPS has a fix

  //signal that payload is ready for flight
  //note that this does not mean that the Ground Station is ready
  digitalWrite(LEDPIN, LOW);
}


// two read sources: GPS and XbeeR
// need to poll both
// once acceptable amount of data is read for any sources, transmitt all in csv format

/**
  Data is sent in csv format below:
  "rs1_data_counter, rs2_data_counter, gps_data_counter, RS1_DATA (expand), RS2_DATA (expand), GPS_DATA (expand)"

  RS1_DATA, RS2_DATA => sensor_num, pressure, temperature, humidity, solar_voltage
  GPS_DATA => latitude, longitude, altitude, hour, minute, seconds, milliseconds


  GPS Data is updated at 1 Hz (as set in the setup() function).
  Both RS Data is updated at 2 Hz.
**/

// These are incremented whenever new, respective data is captured
// Note that data is still sent even when one or two of these is zero. The Ground Station should check for this case. 
int rs1_data_counter = 0;
int rs2_data_counter = 0;
int gps_data_counter = 0;

// Ran over and over by microcontroller:
// 1. Save data packet counters
// 2. Check for GPS, RS data. Get data, possibly through multiple loops.
// 3. Once new data packet for any source is received, transmmit all data
void loop()
{

  // 1. Get total data packets counter
  int data_counter = rs1_data_counter + rs2_data_counter + gps_data_counter;

  // 2.
  // ---- GPS DATA HANDLING ----
  // Get single char from GPS. Value will be 0, if nothing read. 
  char c = GPS.read();

  // check if new NMEA sentence is ready
  if (GPS.newNMEAreceived())
  {
    // print GPS data to USB Serial, if true
    if (GPS_DEBUG)
    {
      Serial.print("GPS DATA: ");
      Serial.println(GPS.lastNMEA());
    }

    // re-run loop() if GPS line parsing fails
    if(!GPS.parse(GPS.lastNMEA())) return;

    // may need to do some checks for GPS.fix here

    // increment gps data counter
    gps_data_counter++;
  }

  // ---- REMOTE SENSOR DATA HANDLING ----
  



  // 3. Transmitt Data, if ready
  // get current total data packets, compare with previous total
  new_data_counter = rs1_data_counter + rs2_data_counter + gps_data_counter;
  if (new_data_counter > prev_data_counter) transmittAllData();
}



//Transmitts all data using Xbee Radio
//may need to check amount of time it takes to run this
//if it is high (on the order of milliseconds), may need to find a more effecient method of printing
//because this could limit the rate at which we poll the GPS and Radio for new data
void transmittAllData()
{
  //PACKET NUMBER
  //rs1_data_counter, rs2_data_counter, gps_data_counter
  XbeeT.print(rs1_data_counter); XbeeT.print(",");
  XbeeT.print(rs2_data_counter); XbeeT.print(",");
  XbeeT.print(gps_data_counter); XbeeT.print(",");


  //REMOTE SENSOR 1 


  //REMOTE SENSOR 2


  //  GPS
  //latitude (deg), longitude (deg), altitude (meters), hour, minute, seconds, milliseconds
  XbeeT.print(GPS.latitude_fixed); XbeeT.print(",");
  XbeeT.print(GPS.longitude_fixed); XbeeT.print(",");
  XbeeT.print(GPS.altitude); XbeeT.print(",");
  XbeeT.print(GPS.hour); XbeeT.print(",");
  XbeeT.print(GPS.minute); XbeeT.print(",");
  XbeeT.print(GPS.seconds); XbeeT.print(",");
  XbeeT.print(GPS.milliseconds); XbeeT.println();

  if(TRANSMITT_DEBUG)
  {
    Serial.print("Transmitting: ")
    Serial.print(rs1_data_counter); Serial.print(",");
    Serial.print(rs2_data_counter); Serial.print(",");
    Serial.print(gps_data_counter); Serial.print(",");
    //rs1 data
    //rs2 data
    //see https://github.com/adafruit/Adafruit_GPS/blob/master/src/Adafruit_GPS.h#L178 for why / 1000000.0
    Serial.print(GPS.latitude_fixed / 1000000.0); Serial.print(","); 
    Serial.print(GPS.longitude_fixed) / 1000000.0; Serial.print(",");
    Serial.print(GPS.altitude); Serial.print(",");
    Serial.print(GPS.hour); Serial.print(",");
    Serial.print(GPS.minute); Serial.print(",");
    Serial.print(GPS.seconds); Serial.print(",");
    Serial.print(GPS.milliseconds); Serial.println();
  }
}


//waits for a GPS fix to be acquired
bool waitGPSfix()
{
  while(!GPS.fix){
    //do something
  }
}

