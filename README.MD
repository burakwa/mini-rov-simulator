# Mini ROV Simulator

## Project Overview

**Mini ROV Simulator** is a complete simulation system for testing and developing Remotely Operated Vehicle (ROV) control systems. The project is split into three main components:

- **Firmware Simulator** (`firmware/`) — C++ program that mimics actual ROV firmware behavior, including motor control, ESC emulation, sensor fusion, and safety systems.
- **Ground Station** (`ground_station/`) — Python-based UI application that provides real-time visualization, telemetry monitoring, and control input interface.
- **Protocol Layer** (`protocol/`) — Defines the JSON‑encoded messages exchanged between ground station and firmware, using Pydantic models for validation.

The system uses **C++20** for the firmware, **Python 3.12+** with **matplotlib** and **pydantic** for the ground station, and **CMake** as the build system.

---

## Directory Structure

```
mini-rov-simulator/
├─ .git/                    # Git version control
├─ .gitignore               # Git ignore rules
├─ README.md                # You are here
├─ firmware/                # C++ firmware simulator
│  ├─ CMakeLists.txt       # CMake build configuration
│  ├─ CMakePresets.json    # CMake preset configurations
│  ├─ firmware/            # Inner CMake project (executable)
│  │  ├─ CMakeLists.txt    # Sources list, compiler flags
│  │  ├─ firmware.cpp      # Entry point, simulation loop
│  │  ├─ firmware.h        # API prototypes
│  │  ├─ include/          # Additional headers
│  │  ├─ main.cpp          # Main source (currently empty)
│  │  ├─ out/              # Build outputs (x64‑Debug, etc.)
│  │  ├─ src/              # Implementation files
│  │  │  ├─ controller.cpp / .h
│  │  │  ├─ esc.cpp / .h
│  │  │  ├─ main.cpp
│  │  │  ├─ motor.cpp / .h
│  │  │  ├─ safety_manager.cpp / .h
│  │  │  └─ sensor_data.h  # Sensor & actuator structs
│  │  └─ tests/
│  │     └─ test_motor.cpp
│  └─ tests/
│     └─ test_motor.cpp
├─ ground_station/          # Python ground station application
│  ├─ .python-version      # Python version (3.12)
│  ├─ .venv/               # Virtual environment
│  ├─ pyproject.toml       # Project metadata, dependencies, entry point
│  ├─ README.md            # Ground station specific README
│  ├─ src/
│  │  └─ ground_station/
│  │     ├─ __init__.py
│  │     ├─ _version.py
│  │     ├─ application.py # Main application, firmware integration, plots
│  │     ├─ communication/   # (empty, intended for protocol handlers)
│  │     ├─ models/          # (empty, intended for Pydantic models)
│  │     ├─ services/        # (empty, intended for services)
│  │     └─ ui/              # (empty, intended for UI components)
│  ├─ src/ground_stain      # Actual Python package (note: directory named ground_station inside src)
│  ├─ tests/
│  │  └─ test_application.py
│  └─ uv.lock              # Lock file for dependencies
├─ protocol/                # Message definitions and Pydantic models
│  ├─ __pycache__/
│  ├─ models.py            # Pydantic models for firmware_status, control_command, etc.
│  ├─ protocol_spec.md     # Human‑readable protocol specification
│  ├─ tests/
│  │  └─ test_models.py
│  └─ __pycache__/
├─ docs/                    # Documentation
│  └─ project_overview.md  # High‑level architecture and development workflow
└─ protocol/                # (duplicate entry, same as above)
```

---

## File‑by‑File Explanation

### Firmware (`firmware/`)

| File / Folder | Purpose |
|---|---|
| `CMakeLists.txt` | Top‑level CMake file that includes the `firmware` sub‑project. |
| `firmware/CMakeLists.txt` | Defines the `firmware` executable, lists source files (`main.cpp`, `motor.cpp`, `esc.cpp`, `controller.cpp`, `safety_manager.cpp`, `sensor_data.h`), sets C++20, and enables testing. |
| `firmware/firmware/firmware.cpp` | **Simulation loop**: generates sensor data (IMU, depth), runs the PID controller (`Controller`), applies safety checks (`SafetyManager`), and prints a formatted status line. |
| `firmware/firmware/firmware.h` | Declares `run_simulator()` and `process_control_command()` for external command processing. |
| `firmware/firmware/firmware.h` | Forward‑declares sensor/actuator structs used across modules. |
| `firmware/firmware/src/motor.cpp / .h` | `Motor` class: models RPM update with acceleration limiting, voltage drop calculation. |
| `firmware/firmware/src/esc.cpp / .h` | `ESC` class: converts throttle (0‑1) to output voltage, clamps to valid voltage range. |
| `firmware/firmware/src/controller.cpp / .h` | `Controller` class: PID controllers for depth and heading/yaw, produces thruster output commands (`left_thruster`, `right_thruster`, `vertical_thruster`). |
| `firmware/firmware/src/safety_manager.cpp / .h` | `SafetyManager` class: validates depth, tilt, and voltage limits; zeros thrusters if any limit is exceeded. **Missing header `sensor_readings.h` must be created (see fixes).** |
| `firmware/firmware/src/sensor_data.h` | Core data structures: `IMUData`, `DepthData`, `ThrusterData`, `SensorData`, `ActuatorOutput`. |
| `firmware/tests/test_motor.cpp` | Placeholder test file for the Motor class. |

### Ground Station (`ground_station/`)

| File / Folder | Purpose |
|---|---|
| `pyproject.toml` | Project metadata (`ground-station`), dependencies (`matplotlib`, `pydantic`), entry point `ground-station = "ground_station:main"`. |
| `ground_station/application.py` | **Main application logic**: defines data models (`ImuData`, `DepthData`, `ThrusterData`, `ROVState`), manages the firmware subprocess (`FirmwareProcess`), creates matplotlib plots, and runs the animation loop. |
| `ground_station/main.py` | Minimal entry point that instantiates `ROVApp` and calls `run()`. |
| `ground_station/application.py `_`FirmwareProcess` | Starts/stops the firmware simulator and reads its stdout. Currently falls back to simulated data if the firmware cannot be launched. |
| `ground_station/application.py `_`ROVApp` | Holds the state, plot data histories, initializes four sub‑plots (Roll, Pitch, Yaw, Status), and provides `_update_from_firmware()` / `_update_plots()` for the `FuncAnimation` loop. |
| `ground_station/tests/test_application.py` | Pytest tests for data models (`ImuData`, `DepthData`, `ThrusterData`, `ROVState`) and for `ROVApp` initialization. |
| `ground_station/src/ground_station/__init__.py` | Small package init that prints "Hello from ground-station!". |
| `ground_station/.venv/` | Virtual environment with installed dependencies. |

### Protocol (`protocol/`)

| File / Folder | Purpose |
|---|---|
| `models.py` | **Pydantic models** for all message types: `FirmwareStatusPayload`, `FirmwareStatus`, `ControlCommandPayload`, `ControlCommand`, `ConfigurationPayload`, `Configuration`, `AlertPayload`, `Alert`. Used for validation and JSON serialization. |
| `protocol_spec.md` | Human‑readable specification of the communication protocol (message format, fields, transmission details). |
| `tests/test_models.py` | Pytest tests that validate model constraints (range checks, default values, invalid input rejection). |

### Documentation (`docs/`)

| File / Folder | Purpose |
|---|---|
| `project_overview.md` | High‑level architecture, design principles, roadmap, and development workflow. |

---

## Building and Running

### 1. Firmware (C++)

The firmware is built with **CMake** and **C++20**. On Windows (MinGW or MSVC):

```powershell
# From the project root
cd firmware
mkdir -p out\build\x64-debug
cd out\build\x64-debug
cmake .. -G "MinGW Makefiles"  # or "Visual Studio 17 2022"
cmake --build .               # or use IDE's Build button
```

The built executable will be placed in `firmware/out/build/x64-debug/firmware.exe` (or `firmware` on Linux).

**Notes:**
- The `SafetyManager` references `SensorReadings` defined in `sensor_readings.h`. This header **must exist** for compilation; see the "Fixes Applied" section below.
- The `Controller::normalize_angle` originally used `M_PI`. The fix replaces it with `std::numbers::pi` from `<numbers>` (C++20).

### 2. Ground Station (Python)

The ground station requires Python **3.12+** and uses **UV** as the package manager.

```powershell
# From the project root
cd ground_station
# Install/refresh dependencies
uv sync
# Run the application
uv run ground-station
# or directly run the main script
uv run python -m ground_station
```

The first run will start the application in simulated mode (firmware subprocess fails gracefully, fallback to generated sine‑wave data). To connect the actual firmware, ensure the compiled `firmware.exe` is on the PATH or modify `FirmwareProcess.start()` in `application.py` to point to the executable.

### 3. Protocol & Models

No building required; the Python models are pure‑Pydantic and can be imported directly:

```python
from protocol.models import FirmwareStatus, ControlCommand
```

Run the protocol tests:

```powershell
cd ground_station
uv run pytest  # runs both ground_station and protocol tests
# or from root
uv run pytest --dir protocol
```

### 4. Linting and Formatting

```powershell
# Lint
uv run ruff check .

# Format
uv run ruff format .
```

---

## Fixes Applied

| Issue | Fix |
|---|---|
| **Missing `sensor_readings.h`** referenced by `safety_manager.h` | Created `firmware/firmware/src/sensor_readings.h` with a `SensorReadings` struct containing `depth`, `roll`, `pitch`, `yaw`, `voltage`, `timestamp`. |
| **`M_PI` not guaranteed in C++20** used in `controller.cpp::normalize_angle` | Replaced `M_PI` with `std::numbers::pi` from `<numbers>`. Updated `#include <numbers>` and qualified as `std::numbers::pi`. |
| **`FirmwareProcess.start()` may fail to launch firmware** | The method now prints a clear warning and falls back to simulated data; a guide for building and linking the firmware executable is provided above. |
| **Ground‑station package discovery** | `pyproject.toml` uses default `src`‑layout; the package lives in `src/ground_station/`. `uv sync` handles this correctly. |

---

## Development Workflow

1. **Add a new protocol message** – Define the Pydantic model in `protocol/models.py`, add the message type to `protocol_spec.md`, and generate corresponding firmware/ground‑station handling.
2. **Extend firmware** – Edit source files in `firmware/firmware/src/` and rebuild with CMake.
3. **Add ground‑station UI** – Add components under `ground_station/src/ground_station/ui/` and wire them in `application.py`.
4. **Run tests** – `uv run pytest` from the root or from individual sub‑directories.
5. **Check code quality** – `uv run ruff check .` and `uv run ruff format .`.

---

## Contact

- **Author**: Burak K.
- **Email**: burakkilnnc@gmail.com