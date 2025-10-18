// radar_system.ino
// ESP32 ultrasonic + servo sweep radar
// Author: weLTon (adapted)
// License: MIT

#include <ESP32Servo.h>

#define TRIG_PIN 5
#define ECHO_PIN 18
#define SERVO_PIN 19

Servo myServo;

// Get distance in centimeters using HC-SR04-like ultrasonic sensor
// Timeout set roughly for max 40 cm (~2.5 ms). pulseIn timeout in microseconds.
float getDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(3);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // timeout in microseconds (4000 us = 4 ms)
  long duration = pulseIn(ECHO_PIN, HIGH, 4000);
  if (duration == 0) return 0.0f; // no echo (timeout)

  // speed of sound ~ 34300 cm/s -> 0.0343 cm/us
  float distance = (duration * 0.0343f) / 2.0f;

  // filter: only keep values between 2 cm and 40 cm
  if (distance < 2.0f || distance > 40.0f) return 0.0f;

  return distance;
}

void setup() {
  Serial.begin(9600);
  // Attach servo (default min/max). If your servo needs calibration, use attach(pin, minPulse, maxPulse).
  myServo.attach(SERVO_PIN);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  digitalWrite(TRIG_PIN, LOW);
  delay(100);

  Serial.println("Radar system initialized");
}

void loop() {
  // Sweep from 0 to 180 degrees (step 2)
  for (int angle = 0; angle <= 180; angle += 2) {
    myServo.write(angle);
    delay(8); // faster sweep speed

    float distance = 0.0f;
    // average of 3 readings to reduce noise
    for (int i = 0; i < 3; i++) {
      distance += getDistanceCm();
      delay(5);
    }
    distance /= 3.0f;

    // print as: angle,distance.
    // trailing dot is intentional (parser expects dot-terminated lines)
    Serial.print(angle);
    Serial.print(",");
    Serial.print(distance, 2);
    Serial.println(".");
    delay(25);
  }

  // Sweep back from 180 to 0
  for (int angle = 180; angle >= 0; angle -= 2) {
    myServo.write(angle);
    delay(8);

    float distance = 0.0f;
    for (int i = 0; i < 3; i++) {
      distance += getDistanceCm();
      delay(5);
    }
    distance /= 3.0f;

    Serial.print(angle);
    Serial.print(",");
    Serial.print(distance, 2);
    Serial.println(".");
    delay(25);
  }
}
