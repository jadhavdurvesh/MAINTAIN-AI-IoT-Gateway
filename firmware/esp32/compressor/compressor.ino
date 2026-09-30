#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Compressor: temperature, vibration, current, load, pressure, flow.
void setup(){Serial.begin(115200);maintainReady("compressor");}
void loop(){/* I2C/ADC temperature/vibration/current + pressure/flow transducers. */}
