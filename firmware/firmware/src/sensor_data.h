#pragma once

namespace rov {

struct IMUData {
    double roll = 0.0;       // Roll angle in degrees
    double pitch = 0.0;      // Pitch angle in degrees
    double yaw = 0.0;        // Yaw heading in degrees
    double target_yaw = 0.0; // Target heading in degrees
    double angular_velocity = 0.0;  // deg/s
    double linear_acceleration = 0.0;  // m/s^2
};

struct DepthData {
    double current_depth = 0.0;    // meters
    double target_depth = 0.0;     // meters (setpoint)
    double temperature = 0.0;      // °C
    double pressure = 101.3;       // kPa
};

struct ThrusterData {
    double left = 0.0;       // [-1, 1]
    double right = 0.0;      // [-1, 1]
    double vertical = 0.0;   // [-1, 1]
};

struct SensorData {
    double timestamp = 0.0;
    IMUData imu;
    DepthData depth;
    ThrusterData thrusters;
};

struct ActuatorOutput {
    double left_thruster = 0.0;
    double right_thruster = 0.0;
    double vertical_thruster = 0.0;
    double roll_command = 0.0;
    double pitch_command = 0.0;
};

} // namespace rov