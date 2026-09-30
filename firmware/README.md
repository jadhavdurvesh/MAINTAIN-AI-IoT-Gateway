# Maintain AI machine firmware

Each machine has an individual Arduino and ESP32 sketch under `arduino/<machine>/` and `esp32/<machine>/`. The sketches use the shared runtime in `common/` so transport, sequencing and sensor drivers stay consistent.

## Supported physical drivers

- ADXL345 over I2C: vibration/acceleration RMS in g
- INA219 over I2C: bus voltage and current using a 0.1-ohm shunt assumption
- DS18B20 1-Wire: temperature
- HX711: load-cell force/weight after calibration
- Hall/encoder pulse inputs: RPM and flow
- Conditioned analog inputs: industrial transmitter/controller outputs
- Digital inputs: machine state/status

## Defaults

ESP32: I2C SDA=21, SCL=22; DS18B20=GPIO4; HX711 DOUT=16, SCK=17; pulse inputs=18,19,23,5. Arduino uses its board-defined SDA/SCL and the documented pulse/analog mappings. Change the shared hardware configuration for the actual board and wiring before deployment.

## Safety

Never connect mains voltage, motor terminals, hazardous thermocouple wiring, or industrial current loops directly to an MCU pin. Use a correctly rated isolated transducer, signal conditioner, fuse/protection and appropriate grounding. The firmware assumes the signal presented to an analog input is already safe and conditioned.

## Calibration

Do not ship with guessed engineering ranges. Update the calibration constants and machine wiring for the actual installed sensor. For HX711, determine zero offset and scale from a known reference. For RPM/flow, set pulses-per-revolution/litre to the installed sensor specification. The INA219 driver assumes a 0.1-ohm shunt; use the installed shunt's actual value or a suitable industrial current transducer instead.

## Telemetry

Every one-second sample emits JSON with `reading_type`, `value`, `unit`, `quality` and a monotonic `sequence`. Hardware drivers are preferred; when an optional driver is absent, the runtime reports `quality=fallback_analog` rather than silently pretending a hardware driver is present.

## Gateway boundary

The microcontroller emits sensor telemetry only. Authentication, device identity, buffering, retries and HTTPS upload remain in the Gateway application. Never put Supabase, Vercel or Gateway secrets in firmware.
