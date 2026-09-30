#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Drill press: rpm, temperature, vibration, load, feed rate, depth, force, coolant.
void setup(){Serial.begin(115200);maintainReady("drill_press");}
void loop(){/* Hall/encoder + temperature + accelerometer + load cell + depth/coolant inputs. */}
