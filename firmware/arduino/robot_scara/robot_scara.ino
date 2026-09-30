#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// SCARA: J1/J2 angles, Z/theta position, joint torque, Z force, servo current, controller temp, cycle.
void setup(){Serial.begin(115200);maintainReady("robot_scara");}
void loop(){/* Interface controller/servo feedback plus force sensor if installed. */}
