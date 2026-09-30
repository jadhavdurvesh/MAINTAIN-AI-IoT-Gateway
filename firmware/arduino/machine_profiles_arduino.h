#pragma once

#include <Arduino.h>
#include <string.h>
#include "../machines/machine_profiles.h"

// Arduino-side profile selection. Set this to the machine physically wired
// to the board. The shared sketch can then be reused without changing its
// transport format.
#ifndef MAINTAIN_MACHINE_PROFILE
#define MAINTAIN_MACHINE_PROFILE "induction_motor"
#endif

inline const MachineProfile* selectedMachineProfile() {
  return machineProfile(MAINTAIN_MACHINE_PROFILE);
}
