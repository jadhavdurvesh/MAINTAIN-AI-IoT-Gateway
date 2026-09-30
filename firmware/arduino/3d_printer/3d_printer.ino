#include <Arduino.h>
#include "../../common/maintain_ai_node.h"
// Thermistors/controllers must be conditioned to ADC input; motion/flow may come from controller outputs.
MaiSignal s[]={MAI_ANALOG("nozzle_temperature",0),MAI_ANALOG("bed_temperature",1),MAI_ANALOG("chamber_temperature",2),MAI_ANALOG("print_speed",3),MAI_ANALOG("layer_height",4),MAI_ANALOG("z_position",5),MAI_ANALOG("extrusion_rate",6),MAI_PULSE("filament_flow",0),MAI_ANALOG("print_progress",7),MAI_ANALOG("vibration",8),MAI_ANALOG("hotend_current",9),MAI_PULSE("fan_speed",1)};
void setup(){maiBegin("3d_printer",s,sizeof(s)/sizeof(s[0]));}
void loop(){maiPoll(s,sizeof(s)/sizeof(s[0]));}
