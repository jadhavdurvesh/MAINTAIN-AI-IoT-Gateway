#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("rpm",0),MAI_ANALOG("temperature",0),MAI_ANALOG("vibration",1),MAI_ANALOG("load",2),MAI_ANALOG("feed_rate",3),MAI_ANALOG("depth",4),MAI_ANALOG("force",5),MAI_DIGITAL("coolant",6)};
void setup(){maiBegin("drill_press",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
