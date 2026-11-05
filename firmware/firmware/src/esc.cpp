#include "esc.h"
#include <cmath>
#include <algorithm>

namespace rov {

ESC::ESC(double min_voltage, double max_voltage, double resolution)
    : min_voltage_(min_voltage), max_voltage_(max_voltage), resolution_(resolution),
      output_voltage_(0.0), pwm_duty_(0.0) {}

double ESC::update(double throttle, double input_voltage) {
    // Clamp throttle to [0, 1] range
    throttle = std::max(0.0, std::min(1.0, throttle));

    // Convert throttle to PWM duty cycle (0-100%)
    pwm_duty_ = throttle * 100.0;

    // Calculate output voltage considering back EMF
    output_voltage_ = input_voltage * (pwm_duty_ / 100.0);

    // Clamp to valid range
    if (output_voltage_ < min_voltage_) output_voltage_ = min_voltage_;
    if (output_voltage_ > max_voltage_) output_voltage_ = max_voltage_;

    return output_voltage_;
}

double ESC::get_pwm_duty() const { return pwm_duty_; }
double ESC::get_output_voltage() const { return output_voltage_; }

} // namespace rov