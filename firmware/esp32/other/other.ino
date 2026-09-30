#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Other equipment: configurable temperature, vibration, current, load.
void setup(){Serial.begin(115200);maintainReady("other");}
void loop(){/* Configure only installed sensors. */}
