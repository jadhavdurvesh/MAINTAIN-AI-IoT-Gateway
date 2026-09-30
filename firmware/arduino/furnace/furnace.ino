#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Furnace/oven: chamber temperature, setpoint, spread, ramp rate, heater load, zone temperatures.
void setup(){Serial.begin(115200);maintainReady("furnace");}
void loop(){/* Thermocouple/RTD interface and isolated controller/heater measurement. */}
