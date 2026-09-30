#pragma once
#include <Arduino.h>

inline void maintainSend(const char* type, float value, const char* unit) {
  if (!isfinite(value)) return;
  Serial.print("{\"reading_type\":\""); Serial.print(type);
  Serial.print("\",\"value\":"); Serial.print(value, 3);
  Serial.print(",\"unit\":\""); Serial.print(unit); Serial.println("\"}");
}

inline void maintainReady(const char* machine) {
  Serial.print("MAINTAIN_AI_MACHINE_READY:"); Serial.println(machine);
}

// Physical integration helpers. Replace these channel definitions with the
// actual sensor driver for the installed hardware. Never connect unsafe
// industrial voltages/currents directly to a MCU ADC.
inline float analogRaw(uint8_t pin) { return (float)analogRead(pin); }
