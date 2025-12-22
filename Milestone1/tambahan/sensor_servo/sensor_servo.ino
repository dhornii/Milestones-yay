#include <ESP32Servo.h>
#include <Wire.h>
#include <VL53L0X.h>

VL53L0X sensor;
Servo servo;
int pin = 18;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  sensor.setTimeout(500);
  sensor.startContinuous();
  
  servo.attach(pin);
}

void loop() {
  uint16_t distance = sensor.readRangeContinuousMillimeters();
  if (sensor.timeoutOccurred()) {
    Serial.println("Timeout!");
  } else {
    Serial.println(distance/10);
  }

  delay(200);

  if (Serial.available() > 0) {
    int angle = Serial.parseInt();

    while(Serial.available() > 0) {
      Serial.read();
    }
  }

  delay(200);
}