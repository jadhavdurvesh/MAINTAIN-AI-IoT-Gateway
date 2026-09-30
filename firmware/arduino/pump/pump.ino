#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Pump: temperature, vibration, current, load, pressure, flow.
// Wire real sensors to the documented hooks; this sketch never fabricates values.
#define PRESSURE_PIN A0
#define FLOW_PIN A1
#define CURRENT_PIN A2
#define TEMP_PIN A3
void setup(){Serial.begin(115200);maintainReady("pump");}
void loop(){static unsigned long t=0;if(millis()-t<5000)return;t=millis();
  // Replace analogRaw() with calibrated sensor drivers for your modules.
  // maintainSend("temperature", ... , "C");
  // maintainSend("vibration", ... , "g");
  // maintainSend("current", ... , "A");
  // maintainSend("load", ... , "%");
  maintainSend("pressure",analogRaw(PRESSURE_PIN),"raw");
  maintainSend("flow",analogRaw(FLOW_PIN),"raw");
  maintainSend("current",analogRaw(CURRENT_PIN),"raw");
  maintainSend("temperature",analogRaw(TEMP_PIN),"raw");
}
