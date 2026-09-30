#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Gearbox: input/output rpm, torque, load, oil temp/level/pressure, particle level.
void setup(){Serial.begin(115200);maintainReady("gearbox");}
void loop(){/* Encoders, torque/load, oil and particle sensor interfaces. */}
