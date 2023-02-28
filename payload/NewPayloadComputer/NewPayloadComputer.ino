//LIBRARY INCLUDES
#include <Adafruit_GPS.h>
#include <SPI.h>
#include <SD.h>

//COUNTERS FOR PARSING
int commaCounter = 0;
int currentIndexInBuffer = 0;
char remoteDataBuffer[40];
char buffer[160];

// These are incremented whenever new, respective data is captured
// Note that data is still sent even when one or two of these is zero. The Ground Station should check for this case.
int rs1_data_counter = 0;
int rs2_data_counter = 0;
int gps_data_counter = 0;

//DATA VARIABLES
char *sensNum;
char *pressure;
char *temp;
char *humidity;
char *solarVolt;
char gpsHour[];
char gpsMin[];
char gpsSec[];
char gpsMSec[];
char gpsLat[];
char gpsLong[];
char gpsSpeed[];
char gpsAngle[];
char gpsAltitude[];
char gpsSatellites[];

//SERIAL PORT DEFINITIONS
#define XbeeR Serial1
#define GPSSerial Serial2
#define XbeeT Serial3
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
// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
#define GPSECHO false

void setup() {
  // indicate that the payload computer is not ready to fly
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, HIGH);



  //STARTING SERIAL PORTS
  //USB Serial
  Serial.begin(115200);
  if (SERIAL_PORT_DEBUG) Serial.println("USB Serial begun!");

  //Xbee Reciever Serial
  XbeeR.begin(9600);
  if (SERIAL_PORT_DEBUG) Serial.println("Xbee Receive Serial begun!");

  //Xbee Transmitter Serial
  XbeeT.begin(9600);
  if (SERIAL_PORT_DEBUG) Serial.println("Xbee Transmit Serial begun!");

  //GPS Serial
  GPS.begin(9600);
  if (SERIAL_PORT_DEBUG) Serial.println("GPS Serial begun!");

  //SD SPI: Change to the correct CS pin
  SD.begin(4);

  delay(2000);  //give some time for all ports to open connection

  //GPS SETUP
  // turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);  // 1 Hz update rate
  // Request updates on antenna status, comment out to keep quiet
  //GPS.sendCommand(PGCMD_ANTENNA);
  //Not sure if wait for gps fix function is implemented correctly
  waitGPSfix();

  delay(500);  //give some time for commands above to run

  //TODO: create functions here that run until RS data is being acquired and GPS has a fix

  //signal that payload is ready for flight
  //note that this does not mean that the Ground Station is ready
  digitalWrite(LEDPIN, LOW);
}


void loop() {
  // 1. Get total data packets counter
  int data_counter = rs1_data_counter + rs2_data_counter + gps_data_counter;

  // 2. Receive Remote Sensor and GPS Data, save to variables
  // Get single char from GPS. Value will be 0, if nothing read.
  char c = GPS.read();

  // check if new NMEA sentence is ready
  if (GPS.newNMEAreceived()) {
    // print GPS data to USB Serial, if true
    if (GPS_DEBUG) {
      Serial.print("GPS DATA: ");
      Serial.println(GPS.lastNMEA());
    }

    // re-run loop() if GPS line parsing fails
    if (!GPS.parse(GPS.lastNMEA())) return;

    // may need to do some checks for GPS.fix here

    // increment gps data counter
    gps_data_counter++;

    //resets all the remote sensor receive counters
    commaCounter = 1;
    currentIndexInBuffer = 1;
    memset(remoteDataBuffer, 0, 40);
    memset(buffer, 0, 160);
    remoteDataBuffer[0] = XbeeR.read();
    delay(100);
    remoteDataBuffer[1] = XbeeR.read();
    delay(100);

    if ((remoteDataBuffer[0] == '1' || remoteDataBuffer[0] == '2') && remoteDataBuffer[1] == ',') {
      remoteDataBuffer[1] = ',';

      while (commaCounter < 5) {
        currentIndexInBuffer++;
        remoteDataBuffer[currentIndexInBuffer] = Serial1.read();
        delay(100);
        if (remoteDataBuffer[currentIndexInBuffer] == ',') {
          commaCounter++;
        }

        // Serial.println(remoteDataBuffer);
      }
      //gets three chars more after the forth comma
      for (int i = 0; i < 4; i++) {
        currentIndexInBuffer++;
        remoteDataBuffer[currentIndexInBuffer] = Serial1.read();
        delay(100);

        // Serial.println(remoteDataBuffer);
      }

      // delay(500);
      // Serial.print("The original array: ");
      // Serial.println(remoteDataBuffer);

      //parses all the commas
      *sensNum = strtok(remoteDataBuffer, ",");
      *pressure = strtok(NULL, ",");
      *temp = strtok(NULL, ",");
      *humidity = strtok(NULL, ",");
      *solarVolt = strtok(NULL, ",");

      if (*sensNum == '1') {
        rs1_data_counter++;
      }

      if (*sensNum == '2') {
        rs2_data_counter++;
      }

      gpsHour[] = GPS.hour;
      gpsMin[] = GPS.minute;
      gpsSec[] = GPS.seconds;
      gpsMSec[] = GPS.milliseconds;
      gpsLat[] = GPS.latitude;
      gpsLong[] = GPS.longitude;
      gpsSpeed[] = GPS.speed;
      gpsAngle[] = GPS.angle;
      gpsAltitude[] = GPS.altitude;
      gpsSatellites[] = GPS.satellites;
      gps_data_counter++;

      // 3. Transmitt Data, if ready
      // get current total data packets, compare with previous total
      new_data_counter = rs1_data_counter + rs2_data_counter + gps_data_counter;
      if (new_data_counter > prev_data_counter) transmittAllData();
    }
  }

  //Transmitts all data using Xbee Radio
  //may need to check amount of time it takes to run this
  //if it is high (on the order of milliseconds), may need to find a more effecient method of printing
  //because this could limit the rate at which we poll the GPS and Radio for new data
  void transmittAllData() {
    //concatenates the remote sensor and gps data
    sprintf(buffer, "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",
            rs1_data_counter, rs2_data_counter, gps_data_counter, sensNum, pressure, temp, humidity, solarVolt, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLat, gpsLong, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites);
    XbeeT.println(buffer);

    //data logging to SD Card, adapter hasn't been acquired yet
    payloadDataFile = SD.open("payloadData.txt", FILE_WRITE);
    payloadDataFile.write(buffer);
    SD.close("payloadData.txt");

    if (TRANSMITT_DEBUG) {
      //concatenates the remote sensor and gps data
      sprintf(buffer, "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s",
              rs1_data_counter, rs2_data_counter, gps_data_counter, sensNum, pressure, temp, humidity, solarVolt, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLat, gpsLong, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites);
      XbeeT.println(buffer);
    }
  }

  //waits for a GPS fix to be acquired
  bool waitGPSfix() {
    while (!GPS.fix) {
      digitalWrite(LEDPIN, HIGH);
      XbeeT.println("Waiting for GPS Fix");
      delay(1000);
    }
    XbeeT.println("GPS Fix Successful");
    return;
  }
