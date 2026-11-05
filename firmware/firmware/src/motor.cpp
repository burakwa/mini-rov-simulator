#include "motor.h"
#include <cmath>

namespace rov {

Motor::Motor(double max_rpm, double kv_factor)
    : max_rpm_(max_rpm), kv_factor_(kv_factor), current_rpm_(0.0) {}

double Motor::update(double target_rpm, double dt) {
    // Smooth RPM transition
    double diff = target_rpm - current_rpm_;
    double change = std::min(std::abs(diff), max_accel_ * dt) * (diff > 0 ? 1.0 : -1.0);
    current_rpm_ += change;
    return current_rpm_;
}

double Motor::get_rpm() const { return current_rpm_; }
double Motor::get_voltage_drop(double current_amp) const {
    return resistance_ * current_amp;
}

} // namespace rov