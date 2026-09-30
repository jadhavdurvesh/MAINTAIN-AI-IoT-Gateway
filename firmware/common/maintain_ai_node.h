#pragma once
#include <Arduino.h>

// Maintain AI physical-node runtime.
// Reference input model: every analog channel must be driven by a SAFE,
// conditioned 0..ADC-range signal (isolated transmitter, divider, shunt,
// instrumentation amplifier, etc.). Never connect mains or industrial
// voltages/currents directly to a MCU pin.

enum MaiMode : uint8_t { MAI_ANALOG=0, MAI_DIGITAL=1, MAI_PULSE=2 };

struct MaiSignal {
  const char* name;
  uint8_t pin;
  float engMin;
  float engMax;
  const char* unit;
  MaiMode mode;
  uint8_t pulseIndex;
};

static volatile uint32_t maiPulseCount[4] = {0,0,0,0};
static uint32_t maiLastPulse[4] = {0,0,0,0};
static uint32_t maiLastSample = 0;
static uint32_t maiSequence = 0;
static const uint32_t MAI_SAMPLE_MS = 1000;

#if defined(ESP32)
  static const uint8_t MAI_ANALOG_PINS[] = {36,39,34,35,32,33,25,26,27,14,13,4,16,17,18,19};
  static const uint8_t MAI_PULSE_PINS[] = {18,19,23,5};
  static const float MAI_ADC_MAX = 4095.0f;
#else
  // Arduino Mega 2560 is the reference high-channel Arduino target.
  // UNO/Nano can be used for profiles with <=6 analog channels.
  static const uint8_t MAI_ANALOG_PINS[] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15};
  static const uint8_t MAI_PULSE_PINS[] = {2,3,18,19};
  static const float MAI_ADC_MAX = 1023.0f;
#endif

inline float maiClamp(float x,float lo,float hi){return x<lo?lo:(x>hi?hi:x);}
inline uint8_t maiAnalogPin(uint8_t i){return MAI_ANALOG_PINS[i % (sizeof(MAI_ANALOG_PINS)/sizeof(MAI_ANALOG_PINS[0]))];}
inline uint8_t maiPulsePin(uint8_t i){return MAI_PULSE_PINS[i & 3];}

inline bool maiContains(const char* s,const char* q){return strstr(s,q)!=nullptr;}

inline void maiDefaults(const char* n,float& lo,float& hi,const char*& unit){
  lo=0; hi=100; unit="%";
  if(maiContains(n,"temperature")){lo=-40;hi=250;unit="C";}
  else if(maiContains(n,"humidity")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"rpm")){lo=0;hi=12000;unit="rpm";}
  else if(maiContains(n,"frequency")){lo=0;hi=100;unit="Hz";}
  else if(maiContains(n,"voltage")){lo=0;hi=500;unit="V";}
  else if(maiContains(n,"current")){lo=0;hi=200;unit="A";}
  else if(maiContains(n,"pressure")){lo=0;hi=250;unit="bar";}
  else if(maiContains(n,"flow")){lo=0;hi=500;unit="L/min";}
  else if(maiContains(n,"speed")){lo=0;hi=5000;unit="mm/s";}
  else if(maiContains(n,"position")||maiContains(n,"depth")){lo=0;hi=2000;unit="mm";}
  else if(maiContains(n,"torque")){lo=0;hi=2000;unit="Nm";}
  else if(maiContains(n,"force")){lo=0;hi=50000;unit="N";}
  else if(maiContains(n,"power")||maiContains(n,"load")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"cycle_time")||maiContains(n,"injection_time")){lo=0;hi=3600;unit="s";}
  else if(maiContains(n,"life")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"progress")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"soc")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"quality")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"efficiency")){lo=0;hi=100;unit="%";}
  else if(maiContains(n,"position")||maiContains(n,"angle")||maiContains(n,"pitch")||maiContains(n,"roll")||maiContains(n,"theta")){lo=-360;hi=360;unit="deg";}
}

inline MaiSignal maiAnalog(const char* n,uint8_t idx){
  float lo,hi; const char* u; maiDefaults(n,lo,hi,u);
  return {n,maiAnalogPin(idx),lo,hi,u,MAI_ANALOG,0};
}
inline MaiSignal maiDigital(const char* n,uint8_t idx){
  return {n,maiAnalogPin(idx),0,1,"state",MAI_DIGITAL,0};
}
inline MaiSignal maiPulse(const char* n,uint8_t idx){
  float lo,hi; const char* u; maiDefaults(n,lo,hi,u);
  return {n,maiPulsePin(idx),lo,hi,u,MAI_PULSE,idx};
}

#define MAI_ANALOG(name,idx) maiAnalog(name,idx)
#define MAI_DIGITAL(name,idx) maiDigital(name,idx)
#define MAI_PULSE(name,idx) maiPulse(name,idx)

inline void IRAM_ATTR maiISR0(){maiPulseCount[0]++;}
inline void IRAM_ATTR maiISR1(){maiPulseCount[1]++;}
inline void IRAM_ATTR maiISR2(){maiPulseCount[2]++;}
inline void IRAM_ATTR maiISR3(){maiPulseCount[3]++;}

inline void maiAttachPulse(uint8_t i){
  pinMode(maiPulsePin(i),INPUT_PULLUP);
  if(i==0) attachInterrupt(digitalPinToInterrupt(maiPulsePin(i)),maiISR0,RISING);
  if(i==1) attachInterrupt(digitalPinToInterrupt(maiPulsePin(i)),maiISR1,RISING);
  if(i==2) attachInterrupt(digitalPinToInterrupt(maiPulsePin(i)),maiISR2,RISING);
  if(i==3) attachInterrupt(digitalPinToInterrupt(maiPulsePin(i)),maiISR3,RISING);
}

inline float maiPulseValue(const MaiSignal& s,float dtSec){
  uint8_t i=s.pulseIndex; noInterrupts(); uint32_t now=maiPulseCount[i]; uint32_t old=maiLastPulse[i]; maiLastPulse[i]=now; interrupts();
  float hz=(dtSec>0)?((float)(now-old)/dtSec):0;
  if(maiContains(s.name,"rpm")) return hz*60.0f;
  if(maiContains(s.name,"flow")) return hz; // Configure pulses-per-litre in the machine file if required.
  return hz;
}

inline float maiAnalogValue(uint8_t pin,float lo,float hi){
  uint32_t sum=0; const uint8_t samples=8;
  for(uint8_t i=0;i<samples;i++){sum+=(uint32_t)analogRead(pin); delayMicroseconds(150);}
  float raw=(float)sum/(float)samples;
  return lo+(raw/MAI_ADC_MAX)*(hi-lo);
}

inline void maiEmit(const MaiSignal& s,float value,const char* quality="ok"){
  if(!isfinite(value)) return;
  Serial.print("{\"reading_type\":\"");Serial.print(s.name);
  Serial.print("\",\"value\":");Serial.print(value,3);
  Serial.print(",\"unit\":\"");Serial.print(s.unit);
  Serial.print("\",\"quality\":\"");Serial.print(quality);
  Serial.print("\",\"sequence\":");Serial.print(++maiSequence);
  Serial.println("}");
}

inline void maiBegin(const char* machine,MaiSignal* signals,size_t count){
  Serial.begin(115200);
  delay(250);
  for(size_t i=0;i<count;i++){
    if(signals[i].mode==MAI_PULSE) maiAttachPulse(signals[i].pulseIndex);
    else if(signals[i].mode==MAI_DIGITAL) pinMode(signals[i].pin,INPUT_PULLUP);
    else pinMode(signals[i].pin,INPUT);
  }
  Serial.print("MAINTAIN_AI_MACHINE_READY:");Serial.println(machine);
}

inline void maiPoll(MaiSignal* signals,size_t count){
  uint32_t now=millis(); if(now-maiLastSample<MAI_SAMPLE_MS) return;
  float dt=(maiLastSample==0)?1.0f:(float)(now-maiLastSample)/1000.0f; maiLastSample=now;
  for(size_t i=0;i<count;i++){
    float value=0;
    if(signals[i].mode==MAI_PULSE) value=maiPulseValue(signals[i],dt);
    else if(signals[i].mode==MAI_DIGITAL) value=digitalRead(signals[i].pin)?1.0f:0.0f;
    else value=maiAnalogValue(signals[i].pin,signals[i].engMin,signals[i].engMax);
    maiEmit(signals[i],value);
  }
  Serial.println("MAINTAIN_AI_HEARTBEAT");
}
