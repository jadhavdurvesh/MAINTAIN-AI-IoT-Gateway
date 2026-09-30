#pragma once
#include <Arduino.h>
#include <Wire.h>

// Production hardware abstraction. Drivers are dependency-free and use the
// Arduino core so the same source can run on AVR Arduino and ESP32.
// Configure pins/calibration in maintain_ai_hardware_config.h.

#ifndef MAI_I2C_SDA
  #if defined(ESP32)
    #define MAI_I2C_SDA 21
    #define MAI_I2C_SCL 22
  #else
    #define MAI_I2C_SDA SDA
    #define MAI_I2C_SCL SCL
  #endif
#endif
#ifndef MAI_DS18B20_PIN
#define MAI_DS18B20_PIN 4
#endif
#ifndef MAI_HX711_DOUT
#define MAI_HX711_DOUT 16
#endif
#ifndef MAI_HX711_SCK
#define MAI_HX711_SCK 17
#endif
#ifndef MAI_INA219_ADDR
#define MAI_INA219_ADDR 0x40
#endif
#ifndef MAI_ADXL345_ADDR
#define MAI_ADXL345_ADDR 0x53
#endif

class MaiAdxl345 {
  bool ready_=false;
  int16_t x_=0,y_=0,z_=0;
public:
  bool begin(){
    Wire.begin();
    Wire.beginTransmission(MAI_ADXL345_ADDR);
    if(Wire.endTransmission()!=0) return false;
    Wire.beginTransmission(MAI_ADXL345_ADDR); Wire.write(0x2D); Wire.write(0x08); if(Wire.endTransmission()!=0)return false;
    Wire.beginTransmission(MAI_ADXL345_ADDR); Wire.write(0x31); Wire.write(0x08); if(Wire.endTransmission()!=0)return false;
    ready_=true; return true;
  }
  bool readRms(float &g){
    if(!ready_) return false;
    Wire.beginTransmission(MAI_ADXL345_ADDR); Wire.write(0x32); if(Wire.endTransmission(false)!=0)return false;
    if(Wire.requestFrom(MAI_ADXL345_ADDR,(uint8_t)6)!=6)return false;
    x_=(int16_t)(Wire.read()|Wire.read()<<8); y_=(int16_t)(Wire.read()|Wire.read()<<8); z_=(int16_t)(Wire.read()|Wire.read()<<8);
    const float scale=0.0039f; float gx=x_*scale,gy=y_*scale,gz=z_*scale;
    g=sqrtf(gx*gx+gy*gy+gz*gz); return true;
  }
  bool ready() const { return ready_; }
};

class MaiIna219 {
  bool ready_=false;
  bool write16(uint8_t reg,uint16_t v){Wire.beginTransmission(MAI_INA219_ADDR);Wire.write(reg);Wire.write(v>>8);Wire.write(v&255);return Wire.endTransmission()==0;}
  uint16_t read16(uint8_t reg){Wire.beginTransmission(MAI_INA219_ADDR);Wire.write(reg);if(Wire.endTransmission(false)!=0)return 0xFFFF;Wire.requestFrom(MAI_INA219_ADDR,(uint8_t)2);if(Wire.available()<2)return 0xFFFF;return (uint16_t)Wire.read()<<8|Wire.read();}
public:
  bool begin(){
    Wire.begin(); Wire.beginTransmission(MAI_INA219_ADDR); if(Wire.endTransmission()!=0)return false;
    // 32V bus, 320mV shunt range, 12-bit bus/ADC, continuous shunt+bus.
    ready_=write16(0x00,0x399F); return ready_;
  }
  bool readBusVoltage(float &v){if(!ready_)return false;uint16_t r=read16(0x02);if(r==0xFFFF)return false;v=((r>>3)*0.004f);return true;}
  bool readCurrent(float &a){if(!ready_)return false;int16_t r=(int16_t)read16(0x04);if(r== -1)return false;a=r*0.001f;return true;}
  bool readPower(float &w){float v,a;if(!readBusVoltage(v)||!readCurrent(a))return false;w=v*a;return true;}
  bool ready() const{return ready_;}
};

class MaiDs18b20 {
  bool ready_=false; uint8_t rom_[8]={0};
  bool reset(){pinMode(MAI_DS18B20_PIN,INPUT_PULLUP);delayMicroseconds(480);pinMode(MAI_DS18B20_PIN,OUTPUT);digitalWrite(MAI_DS18B20_PIN,LOW);delayMicroseconds(480);pinMode(MAI_DS18B20_PIN,INPUT_PULLUP);delayMicroseconds(70);bool p=!digitalRead(MAI_DS18B20_PIN);delayMicroseconds(410);return p;}
  void writeBit(bool b){pinMode(MAI_DS18B20_PIN,OUTPUT);digitalWrite(MAI_DS18B20_PIN,LOW);delayMicroseconds(b?6:60);pinMode(MAI_DS18B20_PIN,INPUT_PULLUP);if(b)delayMicroseconds(54);}
  bool readBit(){pinMode(MAI_DS18B20_PIN,OUTPUT);digitalWrite(MAI_DS18B20_PIN,LOW);delayMicroseconds(3);pinMode(MAI_DS18B20_PIN,INPUT_PULLUP);delayMicroseconds(10);bool b=digitalRead(MAI_DS18B20_PIN);delayMicroseconds(50);return b;}
  void writeByte(uint8_t v){for(uint8_t i=0;i<8;i++,v>>=1)writeBit(v&1);}
  uint8_t readByte(){uint8_t v=0;for(uint8_t i=0;i<8;i++)if(readBit())v|=1<<i;return v;}
public:
  bool begin(){ready_=reset();if(!ready_)return false;writeByte(0xCC);writeByte(0x4E);writeByte(0x4B);writeByte(0x46);writeByte(0x7F);return true;}
  bool readC(float &c){if(!ready_&&!begin())return false;if(!reset())return false;writeByte(0xCC);writeByte(0x44);delay(750);if(!reset())return false;writeByte(0xCC);writeByte(0xBE);uint8_t l=readByte(),h=readByte();int16_t raw=(int16_t)((uint16_t)h<<8|l);c=raw/16.0f;return c>-55&&c<125;}
  bool ready()const{return ready_;}
};

class MaiHx711 {
  bool ready_=false; long offset_=0; float scale_=1.0f;
public:
  void configure(float scale,float offset){scale_=scale;offset_=offset;}
  bool begin(){pinMode(MAI_HX711_DOUT,INPUT);pinMode(MAI_HX711_SCK,OUTPUT);digitalWrite(MAI_HX711_SCK,LOW);ready_=digitalRead(MAI_HX711_DOUT)==LOW;return ready_;}
  bool read(float &value){if(!ready_&&!begin())return false;uint32_t start=millis();while(digitalRead(MAI_HX711_DOUT)){if(millis()-start>100)return false;}int32_t v=0;for(uint8_t i=0;i<24;i++){digitalWrite(MAI_HX711_SCK,HIGH);v=(v<<1)|digitalRead(MAI_HX711_DOUT);digitalWrite(MAI_HX711_SCK,LOW);}digitalWrite(MAI_HX711_SCK,HIGH);digitalWrite(MAI_HX711_SCK,LOW);if(v&0x800000)v|=0xFF000000;value=((float)v-(float)offset_)/scale_;return true;}
};

struct MaiHardwareStatus { bool adxl=false,ina=false,ds18=false,hx711=false; };
static MaiAdxl345 maiAdxl; static MaiIna219 maiIna; static MaiDs18b20 maiDs18; static MaiHx711 maiHx;
static MaiHardwareStatus maiHw;

inline void maiHardwareBegin(){
  Wire.begin();
#if defined(ESP32)
  Wire.setPins(MAI_I2C_SDA,MAI_I2C_SCL); Wire.begin();
#endif
  maiHw.adxl=maiAdxl.begin();
  maiHw.ina=maiIna.begin();
  maiHw.ds18=maiDs18.begin();
  maiHw.hx711=maiHx.begin();
}

inline bool maiHardwareRead(const char* name,float &v){
  if(strstr(name,"vibration")||strstr(name,"acceleration")){float g;if(maiHw.adxl&&maiAdxl.readRms(g)){v=g;return true;}}
  if(strstr(name,"current")){if(maiHw.ina&&maiIna.readCurrent(v))return true;}
  if(strstr(name,"voltage")){if(maiHw.ina&&maiIna.readBusVoltage(v))return true;}
  if(strstr(name,"power")){if(maiHw.ina&&maiIna.readPower(v))return true;}
  if(strstr(name,"force")){if(maiHw.hx711&&maiHx.read(v))return true;}
  if(strstr(name,"temperature")){if(maiHw.ds18&&maiDs18.readC(v))return true;}
  return false;
}
