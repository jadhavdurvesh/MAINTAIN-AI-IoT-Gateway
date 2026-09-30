#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("x_position",0),MAI_ANALOG("y_position",1),MAI_ANALOG("z_position",2),MAI_ANALOG("x_velocity",3),MAI_ANALOG("y_velocity",4),MAI_ANALOG("z_velocity",5),MAI_ANALOG("x_current",6),MAI_ANALOG("y_current",7),MAI_ANALOG("z_current",8),MAI_ANALOG("controller_temperature",9)};
void setup(){maiBegin("robot_cartesian",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
