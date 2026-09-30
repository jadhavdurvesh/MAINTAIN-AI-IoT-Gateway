#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Lathe: spindle rpm/load/temp/vibration, X/Z, feed rate, tool life, coolant flow.
void setup(){Serial.begin(115200);maintainReady("lathe");}
void loop(){/* Encoder/controller and coolant sensor interfaces. */}
