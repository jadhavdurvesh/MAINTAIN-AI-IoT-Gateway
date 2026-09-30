#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Conveyor: temperature, vibration, current, load, speed.
void setup(){Serial.begin(115200);maintainReady("conveyor");}
void loop(){/* Wire temperature sensor, accelerometer, current/load transducer and encoder. */}
