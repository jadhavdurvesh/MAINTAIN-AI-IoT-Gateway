#pragma once
#include <Arduino.h>
#include <string.h>
#include <math.h>
#include "maintain_ai_hardware_config.h"
#include "maintain_ai_sensors.h"
#ifndef IRAM_ATTR
#define IRAM_ATTR
#endif

enum MaiMode : uint8_t { MAI_ANALOG=0, MAI_DIGITAL=1, MAI_PULSE=2 };
struct MaiSignal { const char* name; uint8_t pin; float engMin; float engMax; const char* unit; MaiMode mode; uint8_t pulseIndex; };
static volatile uint32_t maiPulseCount[4]={0,0,0,0};
static uint32_t maiLastPulse[4]={0,0,0,0}, maiLastSample=0, maiSequence=0;
static const uint32_t MAI_SAMPLE_MS=1000;
#if defined(ESP32)
static const uint8_t MAI_ANALOG_PINS[]={36,39,34,35,32,33,25,26,27,14,13,12};
static const uint8_t MAI_PULSE_PINS[]={18,19,23,5};
static const float MAI_ADC_MAX=4095.0f;
#else
static const uint8_t MAI_ANALOG_PINS[]={A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15};
static const uint8_t MAI_PULSE_PINS[]={2,3,18,19};
static const float MAI_ADC_MAX=1023.0f;
#endif
inline bool maiContains(const char*s,const char*q){return strstr(s,q)!=nullptr;}
inline uint8_t maiAnalogPin(uint8_t i){return MAI_ANALOG_PINS[i%(sizeof(MAI_ANALOG_PINS)/sizeof(MAI_ANALOG_PINS[0]))];}
inline uint8_t maiPulsePin(uint8_t i){return MAI_PULSE_PINS[i&3];}
inline void maiDefaults(const char*n,float&lo,float&hi,const char*&u){lo=0;hi=100;u="%";if(maiContains(n,"temperature")){lo=-40;hi=250;u="C";}else if(maiContains(n,"humidity")){lo=0;hi=100;u="%";}else if(maiContains(n,"rpm")){lo=0;hi=12000;u="rpm";}else if(maiContains(n,"frequency")){lo=0;hi=100;u="Hz";}else if(maiContains(n,"voltage")){lo=0;hi=500;u="V";}else if(maiContains(n,"current")){lo=0;hi=200;u="A";}else if(maiContains(n,"pressure")){lo=0;hi=250;u="bar";}else if(maiContains(n,"flow")){lo=0;hi=500;u="L/min";}else if(maiContains(n,"speed")){lo=0;hi=5000;u="mm/s";}else if(maiContains(n,"power")){lo=0;hi=1000;u="kW";}else if(maiContains(n,"position")||maiContains(n,"depth")){lo=0;hi=2000;u="mm";}else if(maiContains(n,"angle")||maiContains(n,"pitch")||maiContains(n,"roll")||maiContains(n,"theta")){lo=-360;hi=360;u="deg";}else if(maiContains(n,"torque")){lo=0;hi=2000;u="Nm";}else if(maiContains(n,"force")){lo=0;hi=50000;u="N";}else if(maiContains(n,"load")){lo=0;hi=100;u="%";}else if(maiContains(n,"cycle_time")||maiContains(n,"injection_time")){lo=0;hi=3600;u="s";}else if(maiContains(n,"life")||maiContains(n,"progress")||maiContains(n,"soc")||maiContains(n,"quality")||maiContains(n,"efficiency")){lo=0;hi=100;u="%";}}
inline MaiSignal maiAnalog(const char*n,uint8_t idx){float lo,hi;const char*u;maiDefaults(n,lo,hi,u);return {n,maiAnalogPin(idx),lo,hi,u,MAI_ANALOG,0};}
inline MaiSignal maiDigital(const char*n,uint8_t idx){return {n,maiAnalogPin(idx),0,1,"state",MAI_DIGITAL,0};}
inline MaiSignal maiPulse(const char*n,uint8_t idx){float lo,hi;const char*u;maiDefaults(n,lo,hi,u);return {n,maiPulsePin(idx),lo,hi,u,MAI_PULSE,idx};}
#define MAI_ANALOG(name,idx) maiAnalog(name,idx)
#define MAI_DIGITAL(name,idx) maiDigital(name,idx)
#define MAI_PULSE(name,idx) maiPulse(name,idx)
inline void IRAM_ATTR maiISR0(){maiPulseCount[0]++;} inline void IRAM_ATTR maiISR1(){maiPulseCount[1]++;} inline void IRAM_ATTR maiISR2(){maiPulseCount[2]++;} inline void IRAM_ATTR maiISR3(){maiPulseCount[3]++;}
inline void maiAttachPulse(uint8_t i){pinMode(maiPulsePin(i),INPUT_PULLUP);int irq=digitalPinToInterrupt(maiPulsePin(i));if(irq==NOT_AN_INTERRUPT)return;if(i==0)attachInterrupt(irq,maiISR0,RISING);if(i==1)attachInterrupt(irq,maiISR1,RISING);if(i==2)attachInterrupt(irq,maiISR2,RISING);if(i==3)attachInterrupt(irq,maiISR3,RISING);}
inline float maiPulseValue(const MaiSignal&s,float dt){uint8_t i=s.pulseIndex;noInterrupts();uint32_t now=maiPulseCount[i],old=maiLastPulse[i];maiLastPulse[i]=now;interrupts();float hz=dt>0?(float)(now-old)/dt:0;return maiContains(s.name,"rpm")?hz/MAI_RPM_PULSES_PER_REV*60.0f:maiContains(s.name,"flow")?hz/MAI_FLOW_PULSES_PER_LITRE*60.0f:hz;}
inline float maiAnalogValue(uint8_t pin,float lo,float hi){uint32_t sum=0;for(uint8_t i=0;i<8;i++){sum+=(uint32_t)analogRead(pin);delayMicroseconds(150);}float raw=(float)sum/8.0f;return lo+(raw/MAI_ADC_MAX)*(hi-lo);}
inline void maiEmit(const MaiSignal&s,float value,const char*quality="ok"){if(!isfinite(value))return;Serial.print("{\"reading_type\":\"");Serial.print(s.name);Serial.print("\",\"value\":");Serial.print(value,3);Serial.print(",\"unit\":\"");Serial.print(s.unit);Serial.print("\",\"quality\":\"");Serial.print(quality);Serial.print("\",\"sequence\":");Serial.print(++maiSequence);Serial.println("}");}
inline void maiBegin(const char*machine,MaiSignal*signals,size_t count){Serial.begin(115200);delay(250);maiHardwareBegin();maiHx.configure(MAI_HX711_SCALE,MAI_HX711_OFFSET);for(size_t i=0;i<count;i++){if(signals[i].mode==MAI_PULSE)maiAttachPulse(signals[i].pulseIndex);else if(signals[i].mode==MAI_DIGITAL)pinMode(signals[i].pin,INPUT_PULLUP);else pinMode(signals[i].pin,INPUT);}Serial.print("MAINTAIN_AI_MACHINE_READY:");Serial.println(machine);}
inline void maiPoll(MaiSignal*signals,size_t count){uint32_t now=millis();if(now-maiLastSample<MAI_SAMPLE_MS)return;float dt=maiLastSample==0?1.0f:(float)(now-maiLastSample)/1000.0f;maiLastSample=now;for(size_t i=0;i<count;i++){float v=0;bool hw=maiHardwareRead(signals[i].name,v);const char*q="ok";if(!hw){v=signals[i].mode==MAI_PULSE?maiPulseValue(signals[i],dt):(signals[i].mode==MAI_DIGITAL?(digitalRead(signals[i].pin)?1.0f:0.0f):maiAnalogValue(signals[i].pin,signals[i].engMin,signals[i].engMax));q="fallback_analog";}maiEmit(signals[i],v,q);}Serial.println("MAINTAIN_AI_HEARTBEAT");}
