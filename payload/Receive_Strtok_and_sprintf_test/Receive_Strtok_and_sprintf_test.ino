#include <Adafruit_GPS.h>


int commaCounter;
int currentIndexInBuffer;

//  What the data is read into
char remoteDataBuffer[40];

// What is written out
char buffer[250];

// Delay timer
int timer = 100;

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

  delay(30000);

  while(!GPS.fix){
    Serial.print("Not connected");
    delay(5000);
  }
}

char c;

void loop() {
  //resets all the counters
  
  c = GPS.read();

  // if (GPSECHO)
  //   if (c) Serial.print(c);

  if (GPS.newNMEAreceived()) {
    GPS.lastNMEA();
    if (!GPS.parse(GPS.lastNMEA())) {
      return;
    }
  }

  if (Serial1.available()) {
    Serial.write(Serial1.read());
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
    // ****SOMEHOW this does not work and the loop above just reads the next 3 values anyways
    for (int i = 0; i < 4; i++) {
      currentIndexInBuffer++;

      if (Serial1.available()) {
        remoteDataBuffer[currentIndexInBuffer] = Serial1.read();
      }

      delay(timer);
    }

    //parses all the commas
    sensNum = strtok(remoteDataBuffer, ",");
    pressure = strtok(NULL, ",");
    temp = strtok(NULL, ",");
    humidity = strtok(NULL, ",");
    solarVolt = strtok(NULL, ",");

    dtostrf(GPS.hour, 2, 0, gpsHour);
    dtostrf(GPS.minute, 2, 0, gpsMin);
    dtostrf(GPS.seconds, 2, 0, gpsMSec);
    dtostrf(GPS.latitude, 15, 6, gpsLat);
    dtostrf(GPS.longitude, 15, 6, gpsLong);
    dtostrf(GPS.speed, 10, 4, gpsSpeed);
    dtostrf(GPS.angle, 10, 4, gpsAngle);
    dtostrf(GPS.altitude, 10, 4, gpsAltitude);
    dtostrf(GPS.satellites, 10, 4, gpsSatellites);

    Serial.println(gpsHour);

    numTemp = atof(temp);
    numSV = atof(solarVolt);

    if (!(numTemp > 40 || numTemp < 0 || numSV > 15 || numSV < 2)) {
      //concatenates the remote sensor and gps data
      sprintf(buffer, "Sensor: %s, Time: %s:%s:%s:%s Long: %s, Lat: %s, Speed: %s, Angle: %s, Altitude: %s, Satellites: %s, Temp: %s, Pressure: %s, Humidity: %s, SV: %s", sensNum, gpsHour, gpsMin, gpsSec, gpsMSec, gpsLong, gpsLat, gpsSpeed, gpsAngle, gpsAltitude, gpsSatellites, temp, pressure, humidity, solarVolt);
      Serial.println(buffer);
    }
  }
}