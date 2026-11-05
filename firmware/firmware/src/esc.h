#pragma once

namespace rov {

class ESC {
public:
    ESC(double min_voltage = 10.0, double max_voltage = 16.8, double resolution = 0.01);
    double update(double throttle, double input_voltage);
    double get_pwm_duty() const;
    double get_output_voltage() const;

private:
    double min_voltage_;
    double max_voltage_;
    double resolution_;
    double output_voltage_;
    double pwm_duty_;
};

} // namespace rov