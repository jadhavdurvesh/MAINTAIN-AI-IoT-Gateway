#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Grinding: spindle rpm/load, vibration, temperature, wheel speed/life, dressing, coolant flow.
void setup(){Serial.begin(115200);maintainReady("grinding_machine");}
void loop(){/* Use spindle encoder, accelerometer, temperature, wheel/controller and flow sensors. */}
