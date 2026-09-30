#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Hydraulic press: pressure, oil temperature, flow, pump load, position, force, speed, cycle.
void setup(){Serial.begin(115200);maintainReady("hydraulic_press");}
void loop(){/* Pressure/temperature/flow transducers + load cell + position/controller inputs. */}
