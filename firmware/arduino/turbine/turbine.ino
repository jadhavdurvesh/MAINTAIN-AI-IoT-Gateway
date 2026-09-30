#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Turbine: rpm, vibration, axial position, load, inlet/outlet temp/pressure, oil pressure.
void setup(){Serial.begin(115200);maintainReady("turbine");}
void loop(){/* Encoder, accelerometer, displacement and industrial transducer inputs. */}
