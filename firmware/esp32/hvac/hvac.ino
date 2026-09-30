#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 HVAC: supply/return temp, setpoint, capacity, flow, static pressure, compressor load.
void setup(){Serial.begin(115200);maintainReady("hvac");}
void loop(){/* Temperature/pressure/airflow and isolated compressor inputs. */}
