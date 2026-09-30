#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Articulated robot: joint positions/torques/temps, servo current, controller temp, grip force.
void setup(){Serial.begin(115200);maintainReady("robot_articulated");}
void loop(){/* Prefer robot controller/servo bus integration and force/grip sensors. */}
