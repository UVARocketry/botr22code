#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp;

void setup() {
    Serial.begin(115200);
    while(!Serial);
    Serial1.begin(9600);
    unsigned status = bmp.begin();
    Serial.println("starting");
    Serial.println(status);
}

void loop() {
    Serial.print(bmp.readTemperature());
    Serial.print(",");
    Serial.print(bmp.readPressure());
    Serial.print(",");
    Serial.print(0.90);
    Serial.print(",");
    Serial.println(9.00);
    

    Serial1.print("1,");
    Serial1.print(bmp.readTemperature());
    Serial1.print(",");
    Serial1.print(bmp.readPressure());
    Serial1.print(",");
    Serial1.print(0.90);
    Serial1.print(",");
    Serial1.println(9.00);
    
    delay (2000);
}