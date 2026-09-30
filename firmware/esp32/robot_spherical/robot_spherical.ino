#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("base_angle",0),MAI_ANALOG("shoulder_angle",1),MAI_ANALOG("radial_position",2),MAI_ANALOG("wrist_angle",3),MAI_ANALOG("base_current",4),MAI_ANALOG("shoulder_current",5),MAI_ANALOG("radial_current",6),MAI_ANALOG("controller_temperature",7)};
void setup(){maiBegin("robot_spherical",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
