#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("rpm",0),MAI_ANALOG("motor_current",0),MAI_ANALOG("motor_temperature",1),MAI_ANALOG("vibration",2),MAI_PULSE("flow",1),MAI_ANALOG("pressure",3),MAI_ANALOG("damper_position",4),MAI_ANALOG("efficiency",5)};
void setup(){maiBegin("fan_blower",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
