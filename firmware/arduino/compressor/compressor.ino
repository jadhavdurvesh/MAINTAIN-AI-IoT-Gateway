#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Compressor: temperature, vibration, current, load, pressure, flow.
void setup(){Serial.begin(115200);maintainReady("compressor");}
void loop(){/* Wire temperature, accelerometer, current/load, pressure and flow sensors. */}
