#pragma once

namespace rov {

struct SensorReadings {
    double depth = 0.0;    // meters
    double roll = 0.0;     // degrees
    double pitch = 0.0;    // degrees
    double yaw = 0.0;      // degrees
    double voltage = 0.0;  // volts
    double timestamp = 0.0;
};

} // namespace rov