#pragma once

#include "sensor_readings.h"
#include <cmath>

namespace rov {

class SafetyManager {
public:
    SafetyManager(double max_depth = 100.0, double max_tilt = 30.0,
                  double max_voltage = 16.8, double voltage_threshold = 15.0);
    
    bool check_depth_safety(double depth) const;
    bool check_tilt_safety(double roll, double pitch) const;
    bool check_voltage_safety(double voltage) const;
    bool check_all_sensors(const SensorReadings& readings) const;

private:
    double max_depth_;
    double max_tilt_;
    double max_voltage_;
    double voltage_threshold_;
};

} // namespace rov