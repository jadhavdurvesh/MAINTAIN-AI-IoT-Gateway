#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Generator: power, voltage, current, frequency, rpm, oil pressure/temp, load.
void setup(){Serial.begin(115200);maintainReady("generator");}
void loop(){/* Certified isolated power measurement + rpm/oil/load inputs. */}
