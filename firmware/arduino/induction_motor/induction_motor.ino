#include <Arduino.h>
// Maintain AI: Induction Motor
// Sensors: temperature, vibration(ADXL), current(INA/ACS), load, rpm(Hall/encoder)
#define TEMP_PIN A0
#define VIBRATION_PIN A1
#define CURRENT_PIN A2
#define RPM_PIN 2
const unsigned long SAMPLE_MS=5000; unsigned long lastSample=0; volatile unsigned long pulses=0;
void pulse(){pulses++;}
void send(const char*t,float v,const char*u){Serial.print("{\"reading_type\":\"");Serial.print(t);Serial.print("\",\"value\":");Serial.print(v,3);Serial.print(",\"unit\":\"");Serial.print(u);Serial.println("\"}");}
void setup(){Serial.begin(115200);pinMode(RPM_PIN,INPUT_PULLUP);attachInterrupt(digitalPinToInterrupt(RPM_PIN),pulse,RISING);}
void loop(){if(millis()-lastSample<SAMPLE_MS)return;lastSample=millis();noInterrupts();auto p=pulses;pulses=0;interrupts();send("temperature",analogRead(TEMP_PIN),"raw");send("vibration",analogRead(VIBRATION_PIN),"raw");send("current",analogRead(CURRENT_PIN),"raw");send("rpm",p*60000.0/SAMPLE_MS,"rpm");}
