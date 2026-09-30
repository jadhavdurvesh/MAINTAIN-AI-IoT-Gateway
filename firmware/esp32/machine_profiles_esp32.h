#pragma once

#include <Arduino.h>
#include <string.h>
#include "../machines/machine_profiles.h"

#ifndef MAINTAIN_MACHINE_PROFILE
#define MAINTAIN_MACHINE_PROFILE "induction_motor"
#endif

inline const MachineProfile* selectedMachineProfile() {
  return machineProfile(MAINTAIN_MACHINE_PROFILE);
}
