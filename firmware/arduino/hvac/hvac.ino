#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// HVAC: supply/return temperature, setpoint, capacity, flows, static pressure, compressor load.
void setup(){Serial.begin(115200);maintainReady("hvac");}
void loop(){/* Temperature, pressure and airflow sensors plus isolated compressor/load input. */}
