#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Milling: spindle rpm/load/temperature/vibration, X/Y/Z position, feed rate, tool life, coolant flow.
void setup(){Serial.begin(115200);maintainReady("milling_machine");}
void loop(){/* Interface with spindle/axis controller and coolant sensors. */}
