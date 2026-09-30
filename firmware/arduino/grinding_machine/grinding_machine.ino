#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("spindle_rpm",0),MAI_ANALOG("grinding_load",0),MAI_ANALOG("vibration",1),MAI_ANALOG("temperature",2),MAI_PULSE("wheel_speed",1),MAI_ANALOG("wheel_life",3),MAI_DIGITAL("dressing",4),MAI_PULSE("coolant_flow",2)};
void setup(){maiBegin("grinding_machine",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
