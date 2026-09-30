#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Spherical: base/shoulder/wrist angles, radial position, axis currents, controller temp.
void setup(){Serial.begin(115200);maintainReady("robot_spherical");}
void loop(){/* Joint encoders and servo/controller feedback. */}
