#pragma once

#include "sensor_data.h"
#include "actuator_output.h"
#include <cmath>

namespace rov {

struct PIDCoefficients {
    double kp = 0.0;
    double ki = 0.0;
    double kd = 0.0;
    double integral = 0.0;
    double previous_error = 0.0;
    double output = 0.0;
};

class Controller {
public:
    Controller(double dt);
    void update(const SensorData& sensors, ActuatorOutput& actuators);
    double get_depth_error() const;
    double get_heading_error() const;

private:
    double dt_;
    double timestamp_;
    double roll_ = 0.0, pitch_ = 0.0, yaw_ = 0.0;
    double throttle_ = 0.0;
    PIDCoefficients depth_pid_;
    PIDCoefficients heading_pid_;
};

} // namespace rov