#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("spindle_rpm",0),MAI_ANALOG("spindle_load",0),MAI_ANALOG("spindle_temperature",1),MAI_ANALOG("spindle_vibration",2),MAI_ANALOG("x_position",3),MAI_ANALOG("y_position",4),MAI_ANALOG("z_position",5),MAI_ANALOG("feed_rate",6),MAI_ANALOG("tool_life",7),MAI_PULSE("coolant_flow",1)};
void setup(){maiBegin("milling_machine",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
