# Arduino machine profiles

The Arduino firmware uses one reusable hardware runtime plus a machine profile. This avoids maintaining dozens of copies of the same serial, timing, validation and sensor-driver code.

Set `MAINTAIN_MACHINE_PROFILE` in `machine_profiles_arduino.h` to one of:

`induction_motor`, `pump`, `conveyor`, `compressor`, `other`, `cnc`, `3d_printer`, `lathe`, `milling_machine`, `drill_press`, `grinding_machine`, `hydraulic_press`, `injection_molding`, `packaging_machine`, `generator`, `transformer`, `boiler`, `furnace`, `hvac`, `fan_blower`, `gearbox`, `turbine`, `robot_articulated`, `robot_scara`, `robot_cartesian`, `robot_delta`, `robot_cylindrical`, `robot_spherical`, `robot_cobot`, `robot_humanoid`.

The selected profile documents the expected telemetry signals and keeps the firmware aligned with the Maintain AI machine type. A physical sensor still needs a compatible driver; the firmware must never fabricate readings for sensors that are not installed.

For a real deployment, use the profile as the wiring/build target and enable only the sensor drivers actually connected to the machine.
