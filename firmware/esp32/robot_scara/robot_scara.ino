#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("j1_angle",0),MAI_ANALOG("j2_angle",1),MAI_ANALOG("z_position",2),MAI_ANALOG("theta",3),MAI_ANALOG("j1_torque",4),MAI_ANALOG("j2_torque",5),MAI_ANALOG("z_force",6),MAI_ANALOG("servo_current",7),MAI_ANALOG("controller_temperature",8),MAI_ANALOG("cycle_time",9)};
void setup(){maiBegin("robot_scara",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
