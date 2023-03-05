#include <Adafruit_GPS.h>

#define GPSECHO false

int commaCounter;
int currentIndexInBuffer;

//  What the data is read into
char remoteDataBuffer[40];

// What is written out
char buffer[250];

// Delay timer
int timer = 25;

char *sensNum;
char *pressure;
char *temp;
char *humidity;
char *solarVolt;
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

float numTemp;
float numSV;

Adafruit_GPS GPS(&Serial2);

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600);
  Serial2.begin(9600);

  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  // Set the update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);

  delay(3000);
}

char c;

void loop() {
  c = GPS.read();

  if (GPS.newNMEAreceived()) {
    GPS.lastNMEA();
    if (!GPS.parse(GPS.lastNMEA())) {
      return;
    }
  }

  commaCounter = 1;
  currentIndexInBuffer = 1;
  memset(remoteDataBuffer, 0, 40);
  memset(buffer, 0, 160);
  if (Serial1.available()) {
    remoteDataBuffer[0] = Serial1.read();
    delay(timer);
    remoteDataBuffer[1] = Serial1.read();
    delay(timer);
  }

  if ((remoteDataBuffer[0] == '1' || remoteDataBuffer[0] == '2') && remoteDataBuffer[1] == ',') {
    while (commaCounter < 4) {
      currentIndexInBuffer++;

      if (Serial1.available()) {
        remoteDataBuffer[currentIndexInBuffer] = Serial1.read();
        if (remoteDataBuffer[currentIndexInBuffer] == ',') {
          commaCounter++;
        }
      }

      delay(timer);
    }

    //gets three chars more after the forth comma
    for (int i = 0; i < 4; i++) {
      currentIndexInBuffer++;

      if (Serial1.available()) {
        remoteDataBuffer[currentIndexInBuffer] = Serial1.read();
      }

      delay(timer);
    }

    //parses all the commas
    sensNum = strtok(remoteDataBuffer, ",");
    temp = strtok(NULL, ",");
    pressure = strtok(NULL, ",");
    humidity = strtok(NULL, ",");
    solarVolt = strtok(NULL, ",");

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

    //converts remote sensor temp and solar voltage from string (char arrays) to to float values (used for the reasonability checks)
    numTemp = atof(temp);
    numSV = atof(solarVolt);

    //reasonability checks for temp and solar voltage
    if (!(numTemp > 40 || numTemp < 0 || numSV > 15 || numSV < 2)) {
      //concatenates the remote sensor and gps data
      sprintf(buffer, "Sensor: %s, Time: %s:%s:%s:%s Long: %s, Lat: %s, Speed: %s, Angle: %s, Altitude: %s, Satellites: %s, Temp: %s, Pressure: %s, Humidity: %s, SV: %s", sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, temp, pressure, humidity, solarVolt);
      //prints it all out to the serial monitor
      Serial.println(buffer);
    }
  }
}