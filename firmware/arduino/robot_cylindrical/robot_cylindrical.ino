#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("base_angle",0),MAI_ANALOG("radial_position",1),MAI_ANALOG("vertical_position",2),MAI_ANALOG("base_current",3),MAI_ANALOG("radial_current",4),MAI_ANALOG("vertical_current",5),MAI_ANALOG("controller_temperature",6)};
void setup(){maiBegin("robot_cylindrical",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
