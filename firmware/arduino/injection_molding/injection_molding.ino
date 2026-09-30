#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("injection_pressure",0),MAI_PULSE("screw_speed",0),MAI_ANALOG("injection_time",1),MAI_ANALOG("back_pressure",2),MAI_ANALOG("mold_temperature",3),MAI_ANALOG("clamp_force",4),MAI_ANALOG("mold_position",5),MAI_ANALOG("cycle_time",6)};
void setup(){maiBegin("injection_molding",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
