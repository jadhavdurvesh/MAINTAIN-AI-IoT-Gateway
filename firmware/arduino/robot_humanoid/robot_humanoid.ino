#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Humanoid: battery/torso/controller temperature, SOC, IMU pitch/roll, leg/arm torque.
void setup(){Serial.begin(115200);maintainReady("robot_humanoid");}
void loop(){/* BMS, IMU and actuator/controller telemetry interfaces. */}
