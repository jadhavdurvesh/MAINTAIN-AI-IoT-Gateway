#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("supply_temperature",0),MAI_ANALOG("return_temperature",1),MAI_ANALOG("setpoint",2),MAI_ANALOG("capacity",3),MAI_PULSE("supply_flow",0),MAI_PULSE("return_flow",1),MAI_ANALOG("static_pressure",4),MAI_ANALOG("compressor_load",5)};
void setup(){maiBegin("hvac",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
