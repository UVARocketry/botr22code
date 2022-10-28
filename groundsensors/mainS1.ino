/*
This is copy/pasted code from the ground sensor description provided in the competition material.
It HAS NOT been verified to work yet (delete this comment when it has been verified to work).
*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

Adafruit_BME280 bme;

void setup() {
    Serial.begin(115200);
    while(!Serial);
    Serial1.begin(9600);
    Wire.begin();
    unsigned status = bme.begin(0x76,&Wire);
    Serial.println("starting");
    Serial.println(status);
}

void loop() {
    float t = bme.readTemperature();
    float p = bme.readPressure();
    float h = bme.readHumidity();
    int an = analogRead(0);
    Serial.print(bme.readTemperature());
    Serial.print(",");
    Serial.print(bme.readPressure());
    Serial.print(",");
    Serial.println(bme.readHumidity());
    Serial1.print("1,"); // replace with 2 for the second sensor
    Serial1.print(bme.readTemperature());
    Serial1.print(",");
    Serial1.print(bme.readPressure());
    Serial1.print(",");
    Serial1.print(bme.readHumidity());
    Serial1.print(",");
    Serial1.println((float)an/1024.0 * 3.3);
    delay(2000);
}