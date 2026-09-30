#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Cobot: six joint positions, joint torque, external force, controller temperature, speed.
void setup(){Serial.begin(115200);maintainReady("robot_cobot");}
void loop(){/* Robot controller/servo feedback and force-torque interface. */}
