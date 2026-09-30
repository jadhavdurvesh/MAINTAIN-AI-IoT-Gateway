#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Transformer: primary/secondary voltage/current, load, oil/winding/ambient temp, cooling.
void setup(){Serial.begin(115200);maintainReady("transformer");}
void loop(){/* Isolated electrical measurement + RTD/temperature + cooling state. */}
