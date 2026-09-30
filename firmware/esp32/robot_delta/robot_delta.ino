#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Delta: arm positions/currents, end-effector position, controller temperature, cycle time.
void setup(){Serial.begin(115200);maintainReady("robot_delta");}
void loop(){/* Servo/controller feedback and end-effector position. */}
