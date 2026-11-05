# Mini ROV Simulator

## Project Overview

A complete mini Remotely Operated Vehicle (ROV) simulation system with a Python-based ground station UI and C++ firmware simulator. Designed for research, education, and ROV control system development.

## Project Structure

```
mini-rov-simulator/
├── ground_station/          # Python Ground Control Station
│   ├── pyproject.toml       # Project configuration (UV, matplotlib, pydantic)
│   ├── src/ground_station/  # Source code
│   │   ├── __init__.py
│   │   ├── main.py          # Entry point
│   │   ├── application.py   # Main application with UI
│   │   └── _version.py
│   └── README.md            # This file
├── firmware/                # C++ Firmware Simulator
│   ├── CMakeLists.txt
│   ├── firmware/
│   │   ├── firmware.cpp
│   │   ├── firmware.h
│   │   ├── include/rov/
│   │   │   ├── esc.hpp
│   │   │   ├── controller.hpp
│   │   │   ├── motor.hpp
│   │   │   ├── safety_manager.hpp
│   │   │   └── command.hpp
│   │   └── src/
│   │       ├── main.cpp
│   │       ├── motor.cpp
│   │       ├── esc.cpp
│   │       ├── controller.cpp
│   │       ├── safety_manager.cpp
│   │       └── sensor_data.h
│   └── tests/
├── protocol/                # Communication protocols
│   ├── protocol_spec.md     # Message specification
│   ├── models.py            # Pydantic v2 models with validation
│   └── tests/               # 12 protocol tests
└── docs/                    # Documentation
    └── project_overview.md  # Architecture and workflow
```

## Features

### Ground Station (Python)
- **Real-time 4-panel visualization**: Roll, Pitch, Yaw gauges + System Status
- **Sensor data display**: Depth, temperature, pressure, voltage
- **Thruster control interface**: Left/Right/Vertical thruster outputs
- **Firmware simulation**: Integrated ROV firmware simulator
- **Protocol validation**: Pydantic-based message validation
- **Bilingual instructions**: Turkish & English control panel

### Firmware (C++)
- **Sensor simulation**: IMU (roll/pitch/yaw), depth, temperature, pressure
- **Control system**: PID-based depth and heading control
- **Safety checks**: Depth limits, tilt detection, voltage protection
- **Real-time control loop**: 100Hz simulation frequency
- **CMake build system**: MSVC and GCC compatible

### Protocol Layer
- **JSON messages** over UDP
- **Message types**: firmware_status, control_command, configuration, alert
- **Schema validation**: Pydantic models with range checking
- **20Hz minimum** status message rate

## Getting Started

### Prerequisites

- Python 3.12+
- UV package manager
- CMake 3.20+ (for firmware)
- C++ compiler (MSVC or GCC)

### Installation

```bash
# 1. Install Python dependencies
cd ground_station
uv sync

# 2. Build firmware simulator
cd firmware
mkdir -p build && cd build
cmake ..
make

# 3. Run the ground station
uv run ground-station
# Or: python -m ground_station.application
```

### Running the Ground Station

```bash
cd ground_station
uv run ground-station
```

The application will:
1. Start the firmware simulator automatically
2. Display real-time ROV state visualization
3. Show sensor data (depth, attitude, voltage)
4. Display control instructions (bilingual)

### Building the Firmware

```bash
cd firmware
mkdir -p build && cd build
cmake ..
make
```

The firmware executable will be at `firmware/build/firmware`.

## Usage

### Controls

| Key | Function | Description |
|-----|----------|-------------|
| **W** | Vertical ↑ | Move ROV forward/upward |
| **S** | Vertical ↓ | Move ROV backward/downward |
| **A** | Lateral ← | Strafe left |
| **D** | Lateral → | Strafe right |
| **↑** | Yaw ↑ | Yaw left |
| **↓** | Yaw ↓ | Yaw right |
| **SPACE** | Stop | Halt all thrusters |
| **Q** | Voltage ↑ | Increase system voltage |
| **E** | Voltage ↓ | Decrease system voltage |
| **R** | Reset | Reset simulation state |
| **ESC** | Quit | Close application |

### Visualization panels:
- **Roll**: Pitch angle in degrees (-30° to +30°)
- **Pitch**: Roll angle in degrees (-30° to +30°)
- **Yaw**: Heading in degrees (-180° to +180°)
- **Status**: Depth (m), Voltage (V), thruster outputs

### Protocol Messages

The ground station communicates with firmware using JSON messages over UDP port 5678:

- `firmware_status`: Sent from firmware to ground station (20Hz)
- `control_command`: Sent from ground station to firmware
- `configuration`: System configuration messages
- `alert`: Warning/critical alerts from firmware

Message format:
```json
{
  "type": "firmware_status",
  "timestamp": 1793874420.123,
  "payload": {
    "depth": 15.5,
    "temperature": 8.2,
    "pressure": 101.3,
    "roll": 0.2,
    "pitch": -0.1,
    "yaw": 45.0,
    "angular_velocity": 0.1,
    "linear_acceleration": 0.05,
    "voltage": 12.4,
    "thruster_left": 0.0,
    "thruster_right": 0.0,
    "thruster_vertical": 0.0,
    "status": "nominal"
  }
}
```

## Development

### Adding New Features

1. **Protocol**: Define message format in `protocol/protocol_spec.md`
2. **Firmware**: Add simulation logic in `firmware/firmware/src/`
3. **Ground Station**: Add UI components in `ground_station/src/ground_station/`
4. **Tests**: Write tests in respective `tests/` directories

### Running Tests

```bash
# Ground station tests
cd ground_station
uv run pytest

# Protocol tests
uv run pytest --dir protocol

# Firmware tests (if applicable)
cd firmware/build
make test
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Type checking
python -m mypy ground_station/
```

## Roadmap

- [x] Project structure and basic setup
- [x] Ground station UI with matplotlib visualization
- [x] Firmware sensor simulation (IMU, depth, temperature)
- [x] Protocol implementation and message validation
- [ ] Mission editor and waypoint navigation
- [ ] Data logging and replay functionality
- [ ] Multi-rover simulation support
- [ ] Web-based UI alternative
- [ ] Real firmware integration (ROS2, MAVLink)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

- **Author**: Burak K.
- **Email**: burakkilnnc@gmail.com
- **GitHub**: [Your GitHub Repository]