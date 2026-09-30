#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
MaiSignal s[]={MAI_ANALOG("chamber_temperature",0),MAI_ANALOG("setpoint",1),MAI_ANALOG("temperature_spread",2),MAI_ANALOG("ramp_rate",3),MAI_ANALOG("heater_load",4),MAI_ANALOG("zone_1",5),MAI_ANALOG("zone_2",6),MAI_ANALOG("zone_3",7)};
void setup(){maiBegin("furnace",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
