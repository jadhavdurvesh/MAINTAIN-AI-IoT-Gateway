#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("joint_1_position",0),MAI_ANALOG("joint_2_position",1),MAI_ANALOG("joint_3_position",2),MAI_ANALOG("joint_4_position",3),MAI_ANALOG("joint_5_position",4),MAI_ANALOG("joint_6_position",5),MAI_ANALOG("joint_torque",6),MAI_ANALOG("external_force",7),MAI_ANALOG("controller_temperature",8),MAI_ANALOG("speed",9)};
void setup(){maiBegin("robot_cobot",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
