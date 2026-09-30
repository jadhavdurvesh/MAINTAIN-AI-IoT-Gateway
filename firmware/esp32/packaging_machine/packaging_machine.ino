#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("line_speed",0),MAI_PULSE("throughput",1),MAI_ANALOG("cycle_time",0),MAI_ANALOG("utilization",1),MAI_DIGITAL("feed",2),MAI_DIGITAL("seal",3),MAI_DIGITAL("cut",4),MAI_ANALOG("reject_rate",5)};
void setup(){maiBegin("packaging_machine",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
