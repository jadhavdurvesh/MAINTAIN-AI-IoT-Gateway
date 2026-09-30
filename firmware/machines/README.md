# Machine telemetry registry

This registry is derived from the machine profiles in Maintain.ai.3 at the firmware integration point. The application currently distinguishes the legacy machine families (induction motor, pump, conveyor, compressor, other), specialized machines, and robot architectures. The registry is shared by Arduino and ESP32 firmware so the physical-device layer does not drift from the application telemetry contract.

## Important implementation rule

A profile lists **expected signals**. It does not mean the microcontroller can measure all of them directly.

Examples:

- temperature/humidity: DHT11/DHT22 or industrial temperature/humidity sensor
- vibration: ADXL345/ADXL355/industrial accelerometer
- current: ACS712/INA219/INA226/current transformer module
- voltage: isolated voltage sensor/transducer
- RPM: Hall/optical encoder
- pressure: pressure transducer with appropriate range
- flow: flow meter/transducer
- position: encoder/linear sensor
- force: load cell + HX711 or industrial load cell amplifier
- torque: torque transducer
- IMU: MPU6050/industrial IMU
- electrical frequency/power: appropriate isolated power measurement hardware

Do not connect mains/high-voltage industrial signals directly to Arduino/ESP32 ADC pins. Use properly rated isolation/transducers and follow the sensor manufacturer's electrical limits.

## Coverage

The current registry includes the machine profiles represented in the Maintain AI specialized UI and robot profiles, including CNC, 3D printer, lathe, milling, drill press, grinding, hydraulic press, injection molding, packaging, generator, transformer, boiler, furnace/oven, HVAC, fan/blower, gearbox, turbine, and articulated/SCARA/Cartesian/delta/cylindrical/spherical/cobot/humanoid robots, plus the legacy equipment families.
