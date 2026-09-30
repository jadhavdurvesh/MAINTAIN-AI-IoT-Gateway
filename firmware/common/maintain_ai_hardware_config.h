#pragma once

// Board-specific wiring/calibration. Hazardous industrial measurements must
// enter through certified isolated transducers/signal conditioners.
#define MAI_I2C_SDA 21
#define MAI_I2C_SCL 22
#define MAI_I2C_SDA_PIN MAI_I2C_SDA
#define MAI_I2C_SCL_PIN MAI_I2C_SCL
#define MAI_DS18B20_PIN 4
#define MAI_DS18B20_INPUT MAI_DS18B20_PIN
#define MAI_HX711_DOUT 16
#define MAI_HX711_DOUT_PIN MAI_HX711_DOUT
#define MAI_HX711_SCK 17
#define MAI_HX711_SCK_PIN MAI_HX711_SCK

struct MaiAnalogCalibration { float rawMin; float rawMax; float engMin; float engMax; };
static const MaiAnalogCalibration MAI_DEFAULT_ANALOG = {0.0f, 4095.0f, 0.0f, 100.0f};

#define MAI_HX711_SCALE 1000.0f
#define MAI_HX711_OFFSET 0L
#define MAI_RPM_PULSES_PER_REV 1.0f
#define MAI_FLOW_PULSES_PER_LITRE 450.0f
#define MAI_4_20MA_RAW_MIN 0.0f
#define MAI_4_20MA_RAW_MAX 4095.0f
#define MAI_4_20MA_ENG_MIN 0.0f
#define MAI_4_20MA_ENG_MAX 100.0f
