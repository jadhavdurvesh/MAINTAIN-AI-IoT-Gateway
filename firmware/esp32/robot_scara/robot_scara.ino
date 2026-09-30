#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 SCARA: J1/J2 angles, Z/theta, joint torque, Z force, servo current, controller temp, cycle.
void setup(){Serial.begin(115200);maintainReady("robot_scara");}
void loop(){/* Servo/controller feedback plus force sensor if installed. */}
