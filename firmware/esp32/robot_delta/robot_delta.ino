#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("arm_a_position",0),MAI_ANALOG("arm_b_position",1),MAI_ANALOG("arm_c_position",2),MAI_ANALOG("arm_a_current",3),MAI_ANALOG("arm_b_current",4),MAI_ANALOG("arm_c_current",5),MAI_ANALOG("end_effector_position",6),MAI_ANALOG("controller_temperature",7),MAI_ANALOG("cycle_time",8)};
void setup(){maiBegin("robot_delta",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
