#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Pressure/fuel/air signals must be isolated industrial transmitters; flame is a certified status output.
MaiSignal s[]={MAI_ANALOG("pressure",0),MAI_ANALOG("temperature",1),MAI_PULSE("flow",0),MAI_ANALOG("steam_quality",2),MAI_DIGITAL("flame_state",3),MAI_PULSE("fuel_flow",1),MAI_PULSE("air_flow",2),MAI_ANALOG("burner_load",4)};
void setup(){maiBegin("boiler",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
