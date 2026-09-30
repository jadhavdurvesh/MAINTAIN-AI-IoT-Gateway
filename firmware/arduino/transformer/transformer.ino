#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Transformer: primary/secondary voltage, current, load, oil/winding temperature, ambient, cooling.
void setup(){Serial.begin(115200);maintainReady("transformer");}
void loop(){/* Use certified isolated voltage/current measurement and RTD/temperature inputs. */}
