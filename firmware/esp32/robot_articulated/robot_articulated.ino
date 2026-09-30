#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("j1_position",0),MAI_ANALOG("j1_torque",1),MAI_ANALOG("j1_temperature",2),MAI_ANALOG("j2_position",3),MAI_ANALOG("j2_torque",4),MAI_ANALOG("j2_temperature",5),MAI_ANALOG("j3_position",6),MAI_ANALOG("j3_torque",7),MAI_ANALOG("j3_temperature",8),MAI_ANALOG("j4_position",9),MAI_ANALOG("j5_position",10),MAI_ANALOG("j6_position",11),MAI_ANALOG("controller_temperature",12),MAI_ANALOG("servo_current",13),MAI_ANALOG("grip_force",14)};
void setup(){maiBegin("robot_articulated",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
