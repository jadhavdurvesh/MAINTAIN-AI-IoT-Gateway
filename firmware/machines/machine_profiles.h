#pragma once

// Machine profiles mirror the telemetry contracts in Maintain.ai.3.
// They are deliberately platform-neutral so the same profile works on
// Arduino and ESP32 firmware. The firmware still needs a real sensor driver
// for each physical signal; this file describes which signals belong to the
// selected machine and prevents accidental cross-machine telemetry.

struct MachineProfile {
  const char* id;
  const char* name;
  const char* signals;
};

// Current Maintain AI machine families and their expected telemetry.
// Legacy families are included first, followed by specialized machines and
// robot architectures present in the application.
static const MachineProfile MACHINE_PROFILES[] = {
  {"induction_motor", "Induction Motor", "temperature,vibration,current,load,rpm"},
  {"pump", "Pump", "temperature,vibration,current,load,pressure,flow"},
  {"conveyor", "Conveyor", "temperature,vibration,current,load,speed"},
  {"compressor", "Compressor", "temperature,vibration,current,load,pressure,flow"},
  {"other", "Other Equipment", "temperature,vibration,current,load"},

  {"cnc", "CNC Machine", "spindle_rpm,spindle_load,spindle_temperature,spindle_vibration,x_position,y_position,z_position,tool_life,coolant_temperature,coolant_flow"},
  {"3d_printer", "3D Printer", "nozzle_temperature,bed_temperature,chamber_temperature,print_speed,layer_height,z_position,extrusion_rate,filament_flow,print_progress,vibration,hotend_current,fan_speed"},
  {"lathe", "Lathe", "spindle_rpm,spindle_load,spindle_temperature,spindle_vibration,x_position,z_position,feed_rate,tool_life,coolant_flow"},
  {"milling_machine", "Milling Machine", "spindle_rpm,spindle_load,spindle_temperature,spindle_vibration,x_position,y_position,z_position,feed_rate,tool_life,coolant_flow"},
  {"drill_press", "Drill Press", "rpm,temperature,vibration,load,feed_rate,depth,force,coolant"},
  {"grinding_machine", "Grinding Machine", "spindle_rpm,grinding_load,vibration,temperature,wheel_speed,wheel_life,dressing,coolant_flow"},
  {"hydraulic_press", "Hydraulic Press", "pressure,oil_temperature,flow,pump_load,position,force,speed,cycle"},
  {"injection_molding", "Injection Molding Machine", "injection_pressure,screw_speed,injection_time,back_pressure,mold_temperature,clamp_force,mold_position,cycle_time"},
  {"packaging_machine", "Packaging Machine", "line_speed,throughput,cycle_time,utilization,feed,seal,cut,reject_rate"},
  {"generator", "Generator", "output_power,voltage,current,frequency,rpm,oil_pressure,oil_temperature,load"},
  {"transformer", "Transformer", "primary_voltage,secondary_voltage,current,load,top_oil_temperature,winding_temperature,ambient,cooling_state"},
  {"boiler", "Boiler", "pressure,temperature,flow,steam_quality,flame_state,fuel_flow,air_flow,burner_load"},
  {"furnace", "Furnace / Oven", "chamber_temperature,setpoint,temperature_spread,ramp_rate,heater_load,zone_1,zone_2,zone_3"},
  {"hvac", "HVAC Unit", "supply_temperature,return_temperature,setpoint,capacity,supply_flow,return_flow,static_pressure,compressor_load"},
  {"fan_blower", "Fan / Blower", "rpm,motor_current,motor_temperature,vibration,flow,pressure,damper_position,efficiency"},
  {"gearbox", "Gearbox", "input_rpm,output_rpm,torque,load,oil_temperature,oil_level,oil_pressure,particle_level"},
  {"turbine", "Turbine", "rpm,vibration,axial_position,load,inlet_temperature,outlet_temperature,pressure,oil_pressure"},

  {"robot_articulated", "Articulated Robot", "j1_position,j1_torque,j1_temperature,j2_position,j2_torque,j2_temperature,j3_position,j3_torque,j4_position,j5_position,j6_position,controller_temperature,servo_current,grip_force"},
  {"robot_scara", "SCARA Robot", "j1_angle,j2_angle,z_position,theta,j1_torque,j2_torque,z_force,servo_current,controller_temperature,cycle_time"},
  {"robot_cartesian", "Cartesian / Gantry Robot", "x_position,y_position,z_position,x_velocity,y_velocity,z_velocity,x_current,y_current,z_current,controller_temperature"},
  {"robot_delta", "Delta / Parallel Robot", "arm_a_position,arm_b_position,arm_c_position,arm_a_current,arm_b_current,arm_c_current,end_effector_position,controller_temperature,cycle_time"},
  {"robot_cylindrical", "Cylindrical Robot", "base_angle,radial_position,vertical_position,base_current,radial_current,vertical_current,controller_temperature"},
  {"robot_spherical", "Spherical / Polar Robot", "base_angle,shoulder_angle,radial_position,wrist_angle,base_current,shoulder_current,radial_current,controller_temperature"},
  {"robot_cobot", "Collaborative Robot", "joint_1_position,joint_2_position,joint_3_position,joint_4_position,joint_5_position,joint_6_position,joint_torque,external_force,controller_temperature,speed"},
  {"robot_humanoid", "Humanoid Robot", "battery_temperature,battery_soc,torso_temperature,imu_pitch,imu_roll,left_leg_torque,right_leg_torque,left_arm_torque,right_arm_torque,controller_temperature"}
};

static const size_t MACHINE_PROFILE_COUNT = sizeof(MACHINE_PROFILES) / sizeof(MACHINE_PROFILES[0]);

inline const MachineProfile* machineProfile(const char* id) {
  for (size_t i = 0; i < MACHINE_PROFILE_COUNT; ++i) {
    if (strcmp(MACHINE_PROFILES[i].id, id) == 0) return &MACHINE_PROFILES[i];
  }
  return nullptr;
}
