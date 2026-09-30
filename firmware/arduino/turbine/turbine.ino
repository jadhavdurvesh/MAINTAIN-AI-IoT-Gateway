#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("rpm",0),MAI_ANALOG("vibration",0),MAI_ANALOG("axial_position",1),MAI_ANALOG("load",2),MAI_ANALOG("inlet_temperature",3),MAI_ANALOG("outlet_temperature",4),MAI_ANALOG("pressure",5),MAI_ANALOG("oil_pressure",6)};
void setup(){maiBegin("turbine",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
