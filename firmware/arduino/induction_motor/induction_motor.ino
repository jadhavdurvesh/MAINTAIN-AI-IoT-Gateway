#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Reference wiring: conditioned temperature/vibration/current/load analog outputs + Hall/encoder RPM.
MaiSignal s[]={MAI_ANALOG("temperature",0),MAI_ANALOG("vibration",1),MAI_ANALOG("current",2),MAI_ANALOG("load",3),MAI_PULSE("rpm",0)};
void setup(){maiBegin("induction_motor",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
