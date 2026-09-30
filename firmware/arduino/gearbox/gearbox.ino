#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Gearbox: input/output rpm, torque, load, oil temperature/level/pressure, particle level.
void setup(){Serial.begin(115200);maintainReady("gearbox");}
void loop(){/* Encoder + torque/load + oil sensors + condition/particle sensor. */}
