# Project Overview: Mini ROV Simulator

## Purpose

This project implements a complete mini ROV (Remotely Operated Vehicle) simulation system designed for research, education, and development of ROV control systems. The system consists of a Python-based ground station UI and a C++ firmware simulator.

## Architecture

### 1. Ground Station (`ground_station/`)

The ground station provides:
- Real-time visualization of ROV state
- Telemetry monitoring and logging
- Thrust and control input interface
- Sensor data display
- Mission planning tools

**Tech Stack:**
- Python 3.12+
- matplotlib (3.11.2+) for visualization
- pydantic (2.14.3+) for data validation
- UV as package manager

### 2. Firmware Simulator (`firmware/`)

A C++ simulator that mimics actual ROV firmware behavior:
- Motor control simulation
- ESC (Electronic Speed Controller) emulation
- Sensor fusion simulation
- Safety systems
- Real-time control loops

**Build System:** CMake with C++20

### 3. Protocol Layer (`protocol/`)

Defines the communication messages between ground station and firmware:
- Status messages (position, velocity, sensor data)
- Control commands (thrust, heading, depth)
- Configuration messages
- Alert and error signals

### 4. Documentation (`docs/`)

Comprehensive documentation including:
- API references
- Usage guides
- Development guidelines
- Architecture decisions

## Key Design Principles

1. **Modularity** - Each component can be developed independently
2. **Extensibility** - New sensors, thrusters, and controllers can be added without modifying core code
3. **Testability** - Comprehensive test coverage for all components
4. **Professional Code Quality** - Type safety, linting, formatting
5. **Real-time Performance** - Suitable for control system development

## Development Workflow

### Adding New Features

1. **Protocol**: Define message format in `protocol/`
2. **Firmware**: Implement simulation in `firmware/firmware/src/`
3. **Ground Station**: Add UI components and handling in `ground_station/src/`
4. **Tests**: Write tests in respective `tests/` directories

### Running Tests

```bash
# Ground station tests
cd ground_station
uv run pytest

# Firmware tests (if applicable)
cd firmware
make test
```

### Code Quality

```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .
```

## Roadmap

- [x] Project structure and basic setup
- [ ] Ground station UI with 3D ROV visualization
- [ ] Firmware sensor simulation (IMU, depth, temperature)
- [ ] Protocol implementation and message validation
- [ ] Mission editor and waypoint navigation
- [ ] Data logging and replay functionality
- [ ] Multi-rover simulation support
- [ ] Web-based UI alternative