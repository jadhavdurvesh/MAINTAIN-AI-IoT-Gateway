#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Cylindrical robot: base angle, radial/vertical position, axis currents, controller temperature.
void setup(){Serial.begin(115200);maintainReady("robot_cylindrical");}
void loop(){/* Axis encoders and servo/controller feedback. */}
