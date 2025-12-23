#include <ESP32Servo.h>

Servo servo;
int pin_servo = 18;

void setup() {
  Serial.begin(115200);
  
  servo.attach(pin_servo);
}

void loop() {
  if (Serial.available() > 0) {
    int angle = Serial.parseInt();

    if (angle >= 0 && angle <= 180) {
      servo.write(angle);
    }

    while(Serial.available() > 0) {
      Serial.read();
    }
  }
}
