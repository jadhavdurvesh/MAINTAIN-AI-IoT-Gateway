#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Fan/blower: rpm, motor current/temp, vibration, flow, pressure, damper position, efficiency.
void setup(){Serial.begin(115200);maintainReady("fan_blower");}
void loop(){/* Hall/encoder, current/temp, accelerometer, pressure/flow and damper inputs. */}
