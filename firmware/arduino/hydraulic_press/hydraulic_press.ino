#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("pressure",0),MAI_ANALOG("oil_temperature",1),MAI_PULSE("flow",0),MAI_ANALOG("pump_load",2),MAI_ANALOG("position",3),MAI_ANALOG("force",4),MAI_ANALOG("speed",5),MAI_DIGITAL("cycle",6)};
void setup(){maiBegin("hydraulic_press",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
