#pragma once

#include <string>
#include <iostream>

namespace rov {

// Firmware version
const std::string VERSION = "0.1.0";

// Sensor data structures (forward declarations; defined in sensor_data.h)
struct IMUData;
struct DepthData;
struct ThrusterData;
struct SensorData;
struct ActuatorOutput;

// Function prototypes
void run_simulator();
void process_control_command(const double* command, int size);

} // namespace rov