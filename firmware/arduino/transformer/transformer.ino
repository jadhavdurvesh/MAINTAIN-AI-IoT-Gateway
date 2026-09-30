#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// High-voltage measurements require certified isolated transducers; never direct-connect HV.
MaiSignal s[]={MAI_ANALOG("primary_voltage",0),MAI_ANALOG("secondary_voltage",1),MAI_ANALOG("current",2),MAI_ANALOG("load",3),MAI_ANALOG("top_oil_temperature",4),MAI_ANALOG("winding_temperature",5),MAI_ANALOG("ambient",6),MAI_DIGITAL("cooling_state",7)};
void setup(){maiBegin("transformer",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
