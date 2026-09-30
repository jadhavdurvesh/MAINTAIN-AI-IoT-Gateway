#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Cartesian robot: X/Y/Z position/velocity/current and controller temperature.
void setup(){Serial.begin(115200);maintainReady("robot_cartesian");}
void loop(){/* Linear encoders/servo feedback and controller interface. */}
