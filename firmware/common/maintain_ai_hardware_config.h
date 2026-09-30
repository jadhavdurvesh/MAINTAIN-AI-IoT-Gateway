#pragma once

// Board-specific wiring/calibration lives here. Keep hazardous industrial
// measurements isolated and conditioned before they reach an MCU pin.
#define MAI_I2C_SDA_PIN 21
#define MAI_I2C_SCL_PIN 22
#define MAI_DS18B20_INPUT 4
#define MAI_HX711_DOUT_PIN 16
#define MAI_HX711_SCK_PIN 17

// Analog transducer calibration: engineering = raw-normalized * span + offset.
struct MaiAnalogCalibration { float rawMin; float rawMax; float engMin; float engMax; };
static const MaiAnalogCalibration MAI_DEFAULT_ANALOG = {0.0f, 4095.0f, 0.0f, 100.0f};

// HX711: set these after calibrating the installed load cell.
#define MAI_HX711_SCALE 1000.0f
#define MAI_HX711_OFFSET 0L

// Pulse sensors: pulses per revolution and pulses per litre can be configured
// per machine. These are deliberately explicit rather than guessed.
#define MAI_RPM_PULSES_PER_REV 1.0f
#define MAI_FLOW_PULSES_PER_LITRE 450.0f
