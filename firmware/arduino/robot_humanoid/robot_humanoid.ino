#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("battery_temperature",0),MAI_ANALOG("battery_soc",1),MAI_ANALOG("torso_temperature",2),MAI_ANALOG("imu_pitch",3),MAI_ANALOG("imu_roll",4),MAI_ANALOG("left_leg_torque",5),MAI_ANALOG("right_leg_torque",6),MAI_ANALOG("left_arm_torque",7),MAI_ANALOG("right_arm_torque",8),MAI_ANALOG("controller_temperature",9)};
void setup(){maiBegin("robot_humanoid",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
