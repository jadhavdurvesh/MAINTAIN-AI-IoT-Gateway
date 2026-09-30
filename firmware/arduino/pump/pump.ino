#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Reference wiring: temperature/vibration/current/load/pressure analog transmitters + pulse flow meter.
MaiSignal s[]={MAI_ANALOG("temperature",0),MAI_ANALOG("vibration",1),MAI_ANALOG("current",2),MAI_ANALOG("load",3),MAI_ANALOG("pressure",4),MAI_PULSE("flow",1)};
void setup(){maiBegin("pump",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
