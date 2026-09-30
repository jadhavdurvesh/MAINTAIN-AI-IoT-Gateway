#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("output_power",0),MAI_ANALOG("voltage",1),MAI_ANALOG("current",2),MAI_ANALOG("frequency",3),MAI_PULSE("rpm",0),MAI_ANALOG("oil_pressure",4),MAI_ANALOG("oil_temperature",5),MAI_ANALOG("load",6)};
void setup(){maiBegin("generator",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
