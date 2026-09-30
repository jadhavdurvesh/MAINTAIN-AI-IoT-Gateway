#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Humanoid: battery/torso/controller temp, SOC, IMU pitch/roll, leg/arm torque.
void setup(){Serial.begin(115200);maintainReady("robot_humanoid");}
void loop(){/* BMS, IMU and actuator/controller telemetry interfaces. */}
