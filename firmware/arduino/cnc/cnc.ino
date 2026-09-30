#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// CNC: spindle_rpm, spindle_load, spindle_temperature, spindle_vibration,
// X/Y/Z position, tool_life, coolant_temperature, coolant_flow.
void setup(){Serial.begin(115200);maintainReady("cnc");}
void loop(){/* Use encoder/PLC/CNC controller interfaces and suitable sensors. */}
