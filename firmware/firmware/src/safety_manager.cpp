#include "safety_manager.h"
#include <cmath>

namespace rov {

SafetyManager::SafetyManager(double max_depth, double max_tilt,
                              double max_voltage, double voltage_threshold)
    : max_depth_(max_depth), max_tilt_(max_tilt),
      max_voltage_(max_voltage), voltage_threshold_(voltage_threshold) {}

bool SafetyManager::check_depth_safety(double depth) const {
    if (std::abs(depth) > max_depth_) {
        return false;  // Out of safe depth range
    }
    return true;
}

bool SafetyManager::check_tilt_safety(double roll, double pitch) const {
    double tilt = std::sqrt(roll * roll + pitch * pitch);
    if (tilt > max_tilt_) {
        return false;  // Excessive tilt angle
    }
    return true;
}

bool SafetyManager::check_voltage_safety(double voltage) const {
    if (std::abs(voltage) > voltage_threshold_) {
        return false;  // Voltage outside safe range
    }
    return true;
}

bool SafetyManager::check_all_sensors(const SensorReadings& readings) const {
    return check_depth_safety(readings.depth) &&
           check_tilt_safety(readings.roll, readings.pitch) &&
           check_voltage_safety(readings.voltage);
}

} // namespace rov