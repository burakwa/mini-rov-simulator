# Mini ROV Simulator

A professional Remotely Operated Vehicle (ROV) simulation system with a Python-based ground station UI and C++ firmware simulator.

## Project Structure

```
mini-rov-simulator/
├── ground_station/        # Python Ground Control Station
│   ├── pyproject.toml     # Project configuration
│   ├── src/ground_stain/  # Source code
│   └── README.md          # This file
├── firmware/              # C++ Firmware Simulator
│   ├── CMakeLists.txt
│   └── firmware/          # Source files
├── protocol/              # Communication protocols
└── docs/                  # Documentation
```

## Features

- **Real-time 3D visualization** of ROV state
- **Sensor data display** (depth, temperature, pressure, etc.)
- **Control interface** for thrusters and systems
- **Firmware simulation** compatible with actual ROV firmware
- **Protocol layer** for ground station <-> firmware communication
- **Extensible architecture** for adding new sensors and controllers

## Getting Started

### Prerequisites

- Python 3.12+
- UV package manager
- CMake (for firmware build)

### Installation

```bash
# Install Python dependencies
cd ground_station
uv sync

# Build firmware
cd firmware
mkdir -p build && cd build
cmake ..
make
```

### Running the Ground Station

```bash
cd ground_station
uv run ground-station
```

Or directly with Python:

```bash
uv run python -m ground_station
```

### Building the Firmware

```bash
cd firmware
mkdir -p build && cd build
cmake ..
make
```

The firmware executable will be at `firmware/build/rov_firmware`.
```

Now let me update the todo and create the project structure documentation.</think>
<tool_call>
<function=todowrite>
<parameter=todos>
[{"content": "Create professional README.md for the project", "priority": "high", "status": "completed"}, {"content": "Create project structure documentation (docs/)", "priority": "high", "status": "in_progress"}, {"content": "Design and implement Python ground station UI with matplotlib", "priority": "high", "status": "pending"}, {"content": "Create protocol documentation and message formats", "priority": "medium", "status": "pending"}, {"content": "Set up development workflow and testing", "priority": "medium", "status": "pending"}]