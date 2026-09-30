#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Conveyor: temperature, vibration, current, load, speed.
void setup(){Serial.begin(115200);maintainReady("conveyor");}
void loop(){/* ADC/I2C sensors plus encoder. */}
