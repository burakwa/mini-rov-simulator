#include "controller.h"
#include <cmath>

namespace rov {

Controller::Controller(double dt) : dt_(dt), timestamp_(0.0) {
    // Initialize PID gains for depth control
    depth_pid_.kp = 1.0;
    depth_pid_.ki = 0.1;
    depth_pid_.kd = 0.05;
    depth_pid_.integral = 0.0;
    depth_pid_.previous_error = 0.0;

    // Initialize PID gains for heading control
    heading_pid_.kp = 2.0;
    heading_pid_.ki = 0.2;
    heading_pid_.kd = 0.1;
    heading_pid_.integral = 0.0;
    heading_pid_.previous_error = 0.0;
}

void Controller::update(const SensorData& sensors, ActuatorOutput& actuators) {
    timestamp_ = sensors.timestamp;

    // Update IMU-derived variables
    roll_ = sensors.imu.roll;
    pitch_ = sensors.imu.pitch;
    yaw_ = sensors.imu.yaw;

    // Depth control using PID
    double depth_error = sensors.depth.target_depth - sensors.depth.current_depth;
    depth_pid_.integral += depth_error * dt_;
    double depth_derivative = (depth_error - depth_pid_.previous_error) / dt_;
    depth_pid_.output = depth_pid_.kp * depth_error +
                        depth_pid_.ki * depth_pid_.integral +
                        depth_pid_.kd * depth_derivative;
    depth_pid_.previous_error = depth_error;

    // Heading/yaw control
    double heading_error = normalize_angle(sensors.imu.target_yaw - sensors.imu.yaw);
    heading_pid_.integral += heading_error * dt_;
    double heading_derivative = (heading_error - heading_pid_.previous_error) / dt_;
    heading_pid_.output = heading_pid_.kp * heading_error +
                          heading_pid_.ki * heading_pid_.integral +
                          heading_pid_.kd * heading_derivative;
    heading_pid_.previous_error = heading_error;

    // Calculate thruster outputs
    // Differential drive for turning, vertical thrust for depth
    double left_thruster = clamp(throttle_ + heading_pid_.output / 2.0);
    double right_thruster = clamp(throttle_ - heading_pid_.output / 2.0);
    double vertical_thruster = clamp(depth_pid_.output);

    // Saturation limits
    left_thruster = std::max(-1.0, std::min(1.0, left_thruster));
    right_thruster = std::max(-1.0, std::min(1.0, right_thruster));
    vertical_thruster = std::max(-1.0, std::min(1.0, vertical_thruster));

    actuators.left_thruster = left_thruster;
    actuators.right_thruster = right_thruster;
    actuators.vertical_thruster = vertical_thruster;
    actuators.roll_command = roll_;
    actuators.pitch_command = pitch_;
}

double Controller::clamp(double val, double min_val, double max_val) {
    return std::max(min_val, std::min(max_val, val));
}

double Controller::normalize_angle(double angle) {
    while (angle > M_PI) angle -= 2.0 * M_PI;
    while (angle < -M_PI) angle += 2.0 * M_PI;
    return angle;
}

} // namespace rov