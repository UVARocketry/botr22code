int commaCounter;
int currentIndexInBuffer;
char remoteDataBuffer[40];
char buffer[160];

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
}

char *token1;
char *token2;
char *token3;
char *token4;
char *token5;
char longitude[] = "400";
char latitude[] = "500";
char speed[] = "100";

void loop() {
  //resets all the counters
  commaCounter = 1;
  currentIndexInBuffer = 1;
  memset(remoteDataBuffer, 0, 40);
  memset(buffer, 0, 160);
  remoteDataBuffer[0] = Serial1.read();
  delay(100);
  remoteDataBuffer[1] = Serial1.read();
  delay(100);

  // if (remoteDataBuffer[0] != '1' && remoteDataBuffer[0] != '2') {
  //   memset(remoteDataBuffer, 0, 40);
  // }

  if ((remoteDataBuffer[0] == '1' || remoteDataBuffer[0] == '2') && remoteDataBuffer[1] == ',') {
    remoteDataBuffer[1] = ',';

    // delay(500);
    // Serial.print("Original array1: ");
    // Serial.println(remoteDataBuffer);

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
    token1 = strtok(remoteDataBuffer, ",");
    token2 = strtok(NULL, ",");
    token3 = strtok(NULL, ",");
    token4 = strtok(NULL, ",");
    token5 = strtok(NULL, ",");

    // Sprintf not problem
    // Serial.print("Sensor: ");
    // Serial.print(token1);
    // Serial.print(",");
    // Serial.print("Temp: ");
    // Serial.print(token2);
    // Serial.print(",");
    // Serial.print("Pressure: ");
    // Serial.print(token3);
    // Serial.print(",");
    // Serial.print("Humidity: ");
    // Serial.print(token4);
    // Serial.print(",");
    // Serial.print("SV: ");
    // Serial.println(token5);


    //concatenates the remote sensor and gps data
    // char buffer[120];
    sprintf(buffer, "Sensor: %s, Long: %s, Lat: %s, Speed: %s, Temp: %s, Pressure: %s, Humidity: %s, SV: %s", token1, longitude, latitude, speed, token2, token3, token4, token5);
    Serial.println(buffer);
  }


  // Testing putting data in array and clearing array
  // for (int i = 0; i < 26; i++) {
  //   buffer[i] = Serial1.read();
  //   delay(50);
  // }

  // Serial.println(buffer);

  // memset(buffer, 0, 26);

  // Serial.println(buffer[7]);

  // delay(1000);
}