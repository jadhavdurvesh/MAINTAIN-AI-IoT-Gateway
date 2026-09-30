#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("temperature",0),MAI_ANALOG("vibration",1),MAI_ANALOG("current",2),MAI_ANALOG("load",3),MAI_PULSE("speed",0)};
void setup(){maiBegin("conveyor",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
