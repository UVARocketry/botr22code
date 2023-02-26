int commaCounter = 0;
int currentIndexInBuffer = 0;
char remoteDataBuffer [40];
char buffer [120];
//String remoteData = "";


void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  
}

void loop() {
  //resets all the counters
  commaCounter = 0;
  currentIndexInBuffer = 0;
  remoteDataBuffer[0] = { 0 };
  buffer[0] = { 0 };

  remoteDataBuffer [0] = Serial1.read();
    //not sure if '1' or 1
    if(remoteDataBuffer[0] == '1' || '2'){
      while(commaCounter < 5){
        currentIndexInBuffer++;
        remoteDataBuffer [currentIndexInBuffer] = Serial1.read();
        if(remoteDataBuffer [currentIndexInBuffer] == ','){
          commaCounter++;
        }
      }
      //gets three chars more after the forth comma
      for(int i = 0; i < 3; i++){
        currentIndexInBuffer++;
        remoteDataBuffer [currentIndexInBuffer] == Serial1.read();
      }
    }
  //parses all the commas
  char *token1 = strtok(remoteDataBuffer, ",");
  char *token2 = strtok(NULL, ",");
  char *token3 = strtok(NULL, ",");
  char *token4 = strtok(NULL, ",");
  char *token5 = strtok(NULL, ",");
  char longitude[] = "400";
  char latitude[] = "500";
  char speed[] = "100";

  //concatenates the remote sensor and gps data
  char buffer [120];
  sprintf(buffer, "Sensor: %s, Pressure: %s, Temp: %s, Humidity: %s, SV: %s, Long: %s, Lat: %s, Speed: %s", 
  token1, token2, token3, token4, token5, longitude, latitude, speed);
  Serial.println(buffer);

  // if (counter == 4) {
  //   i++;
  //   remoteData += receive;

  //   if (i == 3) {
  //     counter = 0;
  //     i = 0;
  //     char remoteDataBuffer[40];
  //     remoteData.toCharArray(remoteDataBuffer, remoteData.length());
  //     Serial.println(remoteDataBuffer);
  //     remoteData = "";
  //   }

  // } else {

  //   if (receive == ',') {
  //     counter++;
  //   }

  //   remoteData += receive;
  // }

  // char remoteDataBuffer [] = "1,100.123,21.0,31,6.7";
  // char *token1 = strtok(remoteDataBuffer, ",");
  // char *token2 = strtok(NULL, ",");
  // char *token3 = strtok(NULL, ",");
  // char *token4 = strtok(NULL, ",");
  // char *token5 = strtok(NULL, ",");
  // char longitude[] = "400";
  // char latitude[] = "500";
  // char speed[] = "100";

  // char buffer [120];
  // sprintf(buffer, "Sensor: %s, Pressure: %s, Temp: %s, Humidity: %s, SV: %s, Long: %s, Lat: %s, Speed: %s", 
  // token1, token2, token3, token4, token5, longitude, latitude, speed);
  // Serial.println(buffer);
}

