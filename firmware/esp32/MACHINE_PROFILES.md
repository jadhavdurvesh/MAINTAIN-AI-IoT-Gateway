# ESP32 machine profiles

The ESP32 firmware uses the same machine-profile registry as the Arduino firmware. Set `MAINTAIN_MACHINE_PROFILE` in `machine_profiles_esp32.h` to select the physical machine.

Supported Maintain AI profiles:

`induction_motor`, `pump`, `conveyor`, `compressor`, `other`, `cnc`, `3d_printer`, `lathe`, `milling_machine`, `drill_press`, `grinding_machine`, `hydraulic_press`, `injection_molding`, `packaging_machine`, `generator`, `transformer`, `boiler`, `furnace`, `hvac`, `fan_blower`, `gearbox`, `turbine`, `robot_articulated`, `robot_scara`, `robot_cartesian`, `robot_delta`, `robot_cylindrical`, `robot_spherical`, `robot_cobot`, `robot_humanoid`.

The same serial telemetry contract is used for every profile. The profile is a hardware/configuration contract, not a license to emit synthetic values. Only enabled sensors that physically exist on the machine should publish readings.
