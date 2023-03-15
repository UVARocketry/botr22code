//LIBRARY INCLUDES
#include <Adafruit_GPS.h>
#include <SPI.h>
#include <SD.h>

//COUNTERS FOR PARSING
int commaCounter = 0;
int currentIndexInBuffer = 0;

//What the data is read into
char remoteDataBuffer[40];
//What is written out
char buffer[160];

//Delay timer, can be changed as necessary
int timer = 25;

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
char c;
char gpsHour[2];
char gpsMin[2];
char gpsSec[2];
char gpsMSec[5];
char gpsLat[15];
char gpsLong[15];
char gpsSpeed[10];
char gpsAngle[10];
char gpsAltitude[10];
char gpsSatellites[10];
File payloadDataFile;

//VARIABLES USED FOR REASONABILITY CHECKS
float numSens;
float numTemp;
float numSV;

//SERIAL PORT DEFINITIONS
#define XbeeR Serial1
#define GPSSerial Serial2
#define XbeeT Serial3
#define LEDPIN 22
#define SD_CS_PIN 10

//DEBUG FLAGS
//set any of these to 'true' for status updates to be sent to the USB Serial Console
//alternatively, you could use the debugger
#define SERIAL_PORT_DEBUG false
#define GPS_DEBUG false
#define TRANSMIT_DEBUG true

//FUNCTION HEADERS
void transmitAllData();

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

  //SD SPI:
  SD.begin(SD_CS_PIN);
  payloadDataFile = SD.open("payloadData.txt", FILE_WRITE);
  payloadDataFile.println("Test Flight 1");
  payloadDataFile.close();

  delay(2000);  //give some time for all ports to open connection

  //GPS SETUP
  // turn on RMC (recommended minimum) and GGA (fix data) including altitude
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);  // 1 Hz update rate

  delay(3000);  //give some time for commands above to run

  //signal that payload is ready for flight
  //note that this does not mean that the Ground Station is ready
  digitalWrite(LEDPIN, LOW);
}


void loop() {
  // 1. Get total data packets counter
  // int data_counter = rs1_data_counter + rs2_data_counter + gps_data_counter;

  // 2. Receive Remote Sensor and GPS Data, save to variables
  // Get single char from GPS. Value will be 0, if nothing read.
  c = GPS.read();

  // check if new NMEA sentence is ready
  if (GPS.newNMEAreceived()) {
    GPS.lastNMEA();

    // print GPS data to USB Serial, if true
    if (GPS_DEBUG) {
      Serial.print("GPS DATA: ");
      Serial.println(GPS.lastNMEA());
    }

    // re-run loop() if GPS line parsing fails
    if (!GPS.parse(GPS.lastNMEA())) {
      return;
    }
  }

  commaCounter = 1;
  currentIndexInBuffer = 1;
  memset(remoteDataBuffer, 0, 40);
  memset(buffer, 0, 160);
  if (XbeeR.available()) {
    remoteDataBuffer[0] = XbeeR.read();
    delay(timer);
    remoteDataBuffer[1] = XbeeR.read();
    delay(timer);
  }

  if ((remoteDataBuffer[0] == '1' || remoteDataBuffer[0] == '2') && remoteDataBuffer[1] == ',') {
    while (commaCounter < 4) {
      currentIndexInBuffer++;

      if (XbeeR.available()) {
        remoteDataBuffer[currentIndexInBuffer] = XbeeR.read();
        if (remoteDataBuffer[currentIndexInBuffer] == ',') {
          commaCounter++;
        }
      }
      delay(timer);
    }

    //gets three chars more after the forth comma
    for (int i = 0; i < 4; i++) {
      currentIndexInBuffer++;

      if (XbeeR.available()) {
        remoteDataBuffer[currentIndexInBuffer] = XbeeR.read();
      }

      delay(timer);
    }

    //parses all the commas
    sensNum = strtok(remoteDataBuffer, ",");
    temp = strtok(NULL, ",");
    pressure = strtok(NULL, ",");
    humidity = strtok(NULL, ",");
    solarVolt = strtok(NULL, ",");

    //converts sensor number from string (char arrays) to to int values
    numSens = atoi(sensNum);
    //increment rs1/rs2 data counters
    if (numSens == 1) {
      rs1_data_counter++;
    }

    if (numSens == 2) {
      rs2_data_counter++;
    }

    // Converts gps data from float to string (character arrays)
    dtostrf(GPS.hour, 1, 0, gpsHour);
    dtostrf(GPS.minute, 1, 0, gpsMin);
    dtostrf(GPS.seconds, 1, 0, gpsSec);
    dtostrf(GPS.milliseconds, 1, 0, gpsMSec);
    dtostrf(GPS.latitude, 1, 4, gpsLat);
    dtostrf(GPS.longitude, 1, 4, gpsLong);
    dtostrf(GPS.speed, 1, 4, gpsSpeed);
    dtostrf(GPS.angle, 1, 4, gpsAngle);
    dtostrf(GPS.altitude, 1, 4, gpsAltitude);
    dtostrf(GPS.satellites, 1, 0, gpsSatellites);

    // increment gps data counter
    gps_data_counter++;

    //converts remote sensor temp and solar voltage from string (char arrays) to to float values (used for the reasonability checks)
    numTemp = atof(temp);
    numSV = atof(solarVolt);

    // 3. Transmit Data, if ready
    transmitAllData();
  }
}

//Transmitts all data using Xbee Radio
//Transmit time can be adjusted by changing the constant "timer" value
void transmitAllData() {
  if (!(numTemp > 40 || numTemp < 0 || numSV > 15 || numSV < 2)) {
    //concatenates the remote sensor and gps data
    sprintf(buffer, "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%i,%i,%i", sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, temp, pressure, humidity, solarVolt,
            rs1_data_counter, rs2_data_counter, gps_data_counter);
    //transmits all the data
    XbeeT.println(buffer);
    //data logging to SD Card
    payloadDataFile = SD.open("payloadData.txt", FILE_WRITE);
    payloadDataFile.println(buffer);
    payloadDataFile.close();
  }

  if (TRANSMIT_DEBUG) {
    //concatenates the remote sensor and gps data
    sprintf(buffer, "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%i,%i,%i", sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, temp, pressure, humidity, solarVolt,
            rs1_data_counter, rs2_data_counter, gps_data_counter);
    Serial.println(buffer);
  }
}