#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Generator: output power, voltage, current, frequency, rpm, oil pressure/temp, load.
void setup(){Serial.begin(115200);maintainReady("generator");}
void loop(){/* Use isolated power meter, frequency input, rpm, oil and load sensors. */}
