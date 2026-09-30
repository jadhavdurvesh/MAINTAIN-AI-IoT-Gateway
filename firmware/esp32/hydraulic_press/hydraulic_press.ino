#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Hydraulic press: pressure, oil temp, flow, pump load, position, force, speed, cycle.
void setup(){Serial.begin(115200);maintainReady("hydraulic_press");}
void loop(){/* Pressure/temperature/flow transducers, load cell and position interface. */}
