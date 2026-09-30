#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Milling: spindle rpm/load/temp/vibration, XYZ, feed rate, tool life, coolant flow.
void setup(){Serial.begin(115200);maintainReady("milling_machine");}
void loop(){/* Spindle/axis/controller and coolant interfaces. */}
