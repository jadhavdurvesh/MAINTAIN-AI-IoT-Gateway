#pragma once
#include <Arduino.h>
#include <SPI.h>

#ifndef MAI_MAX31855_CS
  #if defined(ESP32)
    #define MAI_MAX31855_SCK 14
    #define MAI_MAX31855_MISO 12
    #define MAI_MAX31855_CS 15
  #else
    #define MAI_MAX31855_SCK 13
    #define MAI_MAX31855_MISO 12
    #define MAI_MAX31855_CS 10
  #endif
#endif

class MaiMax31855 {
  uint8_t cs_; bool ready_=false;
  uint32_t read32(){digitalWrite(cs_,LOW);uint32_t v=0;for(uint8_t i=0;i<4;i++)v=(v<<8)|SPI.transfer(0);digitalWrite(cs_,HIGH);return v;}
public:
  explicit MaiMax31855(uint8_t cs=MAI_MAX31855_CS):cs_(cs){}
  void begin(){pinMode(cs_,OUTPUT);digitalWrite(cs_,HIGH);#if defined(ESP32)
    SPI.begin(MAI_MAX31855_SCK,MAI_MAX31855_MISO,MOSI,cs_);
#else
    SPI.begin();
#endif
    ready_=true;}
  bool readC(float &c){if(!ready_)begin();uint32_t r=read32();if(r&0x00010000UL)return false;int32_t raw=(int32_t)(r>>18);if(raw&0x2000)raw|=~0x3FFF;c=raw*0.25f;return isfinite(c)&&c>-270&&c<1372;}
};

// Minimal Modbus RTU master for isolated RS-485 transceivers. The transceiver
// DE/RE pin must be wired to a GPIO and the bus must be electrically isolated.
class MaiModbusRtu {
  Stream &port_; int8_t dePin_;
  static uint16_t crc(const uint8_t*b,size_t n){uint16_t c=0xFFFF;for(size_t i=0;i<n;i++){c^=b[i];for(uint8_t j=0;j<8;j++)c=(c&1)?(c>>1)^0xA001:c>>1;}return c;}
  void tx(bool on){if(dePin_>=0){digitalWrite(dePin_,on?HIGH:LOW);if(on)delayMicroseconds(100);}}
public:
  MaiModbusRtu(Stream &p,int8_t dePin=-1):port_(p),dePin_(dePin){}
  void begin(){if(dePin_>=0){pinMode(dePin_,OUTPUT);digitalWrite(dePin_,LOW);}}
  bool readHolding(uint8_t id,uint16_t reg,uint16_t count,uint16_t*out,uint16_t timeoutMs=250){if(count==0||count>32)return false;while(port_.available())port_.read();uint8_t q[8]={id,3,(uint8_t)(reg>>8),(uint8_t)reg,(uint8_t)(count>>8),(uint8_t)count,0,0};uint16_t c=crc(q,6);q[6]=c&255;q[7]=c>>8;tx(true);port_.write(q,8);port_.flush();tx(false);uint8_t r[69];size_t n=0;uint32_t start=millis();while(millis()-start<timeoutMs&&n<sizeof(r)){while(port_.available()&&n<sizeof(r))r[n++]=(uint8_t)port_.read();}size_t expected=5+2*count;if(n<expected||r[0]!=id||r[1]!=3||r[2]!=2*count)return false;uint16_t got=(uint16_t)r[expected-2]|((uint16_t)r[expected-1]<<8);if(crc(r,expected-2)!=got)return false;for(uint16_t i=0;i<count;i++)out[i]=((uint16_t)r[3+i*2]<<8)|r[4+i*2];return true;}
};
