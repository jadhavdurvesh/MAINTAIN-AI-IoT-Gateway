#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_PULSE("input_rpm",0),MAI_PULSE("output_rpm",1),MAI_ANALOG("torque",0),MAI_ANALOG("load",1),MAI_ANALOG("oil_temperature",2),MAI_ANALOG("oil_level",3),MAI_ANALOG("oil_pressure",4),MAI_ANALOG("particle_level",5)};
void setup(){maiBegin("gearbox",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
