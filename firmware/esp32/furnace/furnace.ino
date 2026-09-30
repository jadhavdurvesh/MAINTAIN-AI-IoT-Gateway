#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Furnace: chamber temperature, setpoint, spread, ramp rate, heater load, zone temperatures.
void setup(){Serial.begin(115200);maintainReady("furnace");}
void loop(){/* Thermocouple/RTD and isolated heater/controller inputs. */}
