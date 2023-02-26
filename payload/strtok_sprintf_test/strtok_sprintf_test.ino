void setup() {
  Serial.begin(9600);
  //Serial1.begin(9600);

}

void loop() {
  //char remoteDataBuffer[] = Serial1.read();

  char remoteDataBuffer [] = "1,100.123,21.0,31,6.7";
  char *token1 = strtok(remoteDataBuffer, ",");
  char *token2 = strtok(NULL, ",");
  char *token3 = strtok(NULL, ",");
  char *token4 = strtok(NULL, ",");
  char *token5 = strtok(NULL, ",");
  char longitude = 400;
  char latitude = 500;
  char speed = 100;

  char buffer [120];
  sprintf(buffer, "Sensor: %c, Pressure: %d, Temp: %d, Humidity: %d, SV: %d, Long: %d, Lat: %d, Speed: %d", 
  token1, token2, token3, token4, token5, longitude, latitude, speed);
  Serial.println(buffer);
  delay(500);
}
