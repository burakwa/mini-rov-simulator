#include "firmware.h"
#include "sensor_data.h"
#include "controller.h"
#include "safety_manager.h"
#include <cmath>
#include <iostream>
#include <chrono>
#include <thread>

using namespace std;
using namespace rov;

// ---------------------------------------------------------------------------
// Firmware simulator main
// ---------------------------------------------------------------------------
int main() {
    cout << "Mini ROV Firmware Simulator" << endl;
    cout << "===========================" << endl;

    // Initialize components
    Controller controller(0.01);  // 10ms control loop
    SafetyManager safety(100.0, 30.0, 16.8, 15.0);

    // Simulation parameters
    double simulation_time = 0.0;
    double dt = 0.01;  // 100Hz simulation loop
    double target_depth = 10.0;  // Target depth in meters
    double target_yaw = 0.0;     // Target heading in degrees

    // Sensor simulation state
    double time_constant = 0.0;
    double depth_momentum = 0.0;
    double roll_phase = 0.0;
    double pitch_phase = 0.0;
    double yaw_phase = 0.0;

    cout << "Starting simulation loop..." << endl;
    cout << "Press Ctrl+C to stop." << endl << endl;

    try {
        while (true) {
            // -----------------------------------------------------------------
            // 1. Generate simulated sensor data with realistic dynamics
            // -----------------------------------------------------------------
            simulation_time += dt;

            // Smooth sinusoidal movements for roll/pitch/yaw
            roll_phase += 0.3 * dt;
            pitch_phase += 0.25 * dt;
            yaw_phase += 0.15 * dt;

            IMUData imu;
            imu.roll = 2.0 * sin(roll_phase);                           // Small roll oscillation
            imu.pitch = 1.5 * cos(pitch_phase);                         // Pitch oscillation
            imu.yaw = 5.0 * sin(yaw_phase);                             // Yaw drift
            imu.angular_velocity = 0.1 * sin(simulation_time * 0.5);          // Angular velocity
            imu.linear_acceleration = 0.05 * cos(simulation_time * 0.3);      // Linear accel

            // Depth simulation with first-order dynamics
            double depth_rate = 0.1 * (target_depth - depth_momentum);
            depth_momentum += depth_rate * dt;
            // Add small high-frequency component
            depth_momentum += 0.02 * sin(simulation_time * 1.2);

            DepthData depth;
            depth.current_depth = depth_momentum;
            depth.target_depth = target_depth;
            depth.temperature = 8.0 + 0.5 * sin(simulation_time * 0.1);       // Slight temp variation
            depth.pressure = 101.3 + depth_momentum * 0.997;            // Hydrostatic pressure

            // Thruster state (from last control cycle)
            ThrusterData thrusters;
            thrusters.left = 0.0;
            thrusters.right = 0.0;
            thrusters.vertical = 0.0;

            // -----------------------------------------------------------------
            // 2. Run control algorithm
            // -----------------------------------------------------------------
            SensorData sensors;
            sensors.timestamp = simulation_time;
            sensors.imu = imu;
            sensors.depth = depth;
            sensors.thrusters = thrusters;

            ActuatorOutput actuators;
            controller.update(sensors, actuators);

            // Apply safety checks
            SensorReadings readings;
            readings.depth = depth.current_depth;
            readings.roll = imu.roll;
            readings.pitch = imu.pitch;
            readings.yaw = imu.yaw;
            readings.voltage = 12.0;
            readings.timestamp = simulation_time;

            if (!safety.check_all_sensors(readings)) {
                cout << "WARNING: Safety limit exceeded at t=" << simulation_time << "s" << endl;
                // Zero thrusters on safety breach
                actuators.left_thruster = 0.0;
                actuators.right_thruster = 0.0;
                actuators.vertical_thruster = 0.0;
            }

            thrusters.left = actuators.left_thruster;
            thrusters.right = actuators.right_thruster;
            thrusters.vertical = actuators.vertical_thruster;

// -----------------------------------------------------------------
            // 3. Output data (JSON protocol for ground station)
// -----------------------------------------------------------------
            // JSON format: timestamp, imu, depth, thrusters, voltage
            cout << "{";
            cout << "\"timestamp\":" << simulation_time;
            
            // IMU data
            cout << ",\"imu\":{\"roll\":" << imu.roll
                << ",\"pitch\":" << imu.pitch
                << ",\"yaw\":" << imu.yaw
                << ",\"angular_velocity\":" << imu.angular_velocity
                << ",\"linear_acceleration\":" << imu.linear_acceleration
                << "}";
            
            // Depth data
            cout << ",\"depth\":{\"current_depth\":" << depth.current_depth
                << ",\"target_depth\":" << depth.target_depth
                << ",\"temperature\":" << depth.temperature
                << ",\"pressure\":" << depth.pressure
                << "}";
            
            // Thruster data
            cout << ",\"thrusters\":{\"left\":" << actuators.left_thruster
                << ",\"right\":" << actuators.right_thruster
                << ",\"vertical\":" << actuators.vertical_thruster
                << "}";
            
            // Voltage
            cout << ",\"voltage\":" << 12.0;
            
            cout << "}" << endl;  // Newline for easy line-by-line parsing

            // -----------------------------------------------------------------
            // 4. Sleep for real-time simulation (optional)
            // -----------------------------------------------------------------
            std::this_thread::sleep_for(std::chrono::milliseconds(int(dt * 1000)));
        }
    } catch (const exception& e) {
        cout << "\nSimulation stopped." << endl;
        return 0;
    }

    return 0;
}