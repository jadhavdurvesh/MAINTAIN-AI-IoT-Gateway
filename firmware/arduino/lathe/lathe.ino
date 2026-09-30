#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Lathe: spindle rpm/load/temperature/vibration, X/Z position, feed rate, tool life, coolant flow.
void setup(){Serial.begin(115200);maintainReady("lathe");}
void loop(){/* Interface with spindle encoder, axes, tool controller and coolant sensors. */}
