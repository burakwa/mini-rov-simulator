#pragma once

namespace rov {

class Motor {
public:
    Motor(double max_rpm = 5000.0, double kv_factor = 0.1);
    double update(double target_rpm, double dt);
    double get_rpm() const;
    double get_voltage_drop(double current_amp) const;

private:
    double max_rpm_;
    double kv_factor_;
    double current_rpm_ = 0.0;
    double max_accel_ = 5000.0;  // RPM/s max acceleration
    double resistance_ = 0.01;   // Ohm
};

} // namespace rov