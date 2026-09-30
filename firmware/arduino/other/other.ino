#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Other equipment: temperature, vibration, current, load.
void setup(){Serial.begin(115200);maintainReady("other");}
void loop(){/* Configure only the physical sensors installed on this equipment. */}
