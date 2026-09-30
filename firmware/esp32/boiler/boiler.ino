#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// ESP32 Boiler: pressure, temperature, flow, steam quality, flame state, fuel/air flow, burner load.
void setup(){Serial.begin(115200);maintainReady("boiler");}
void loop(){/* Industrial transducer and flame/controller interfaces. */}
