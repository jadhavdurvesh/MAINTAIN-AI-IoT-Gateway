#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Cartesian: XYZ position/velocity/current and controller temperature.
void setup(){Serial.begin(115200);maintainReady("robot_cartesian");}
void loop(){/* Linear encoders and servo/controller feedback. */}
