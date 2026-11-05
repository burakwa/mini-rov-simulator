# Mini ROV Protocol Specification

## Overview

This module defines the communication protocol between the Ground Station and the ROV Firmware. All messages are JSON-encoded and transmitted over UDP.

## Message Format

All messages follow this structure:
```json
{
  "type": "<message_type>",
  "timestamp": "<iso8601_timestamp>",
  "payload": { ... }
}
```

## Message Types

### 1. Firmware Status (`firmware_status`)

Sent from firmware to ground station at 20Hz minimum.

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | float | Seconds since epoch |
| `depth` | float | Depth in meters |
| `temperature` | float | Temperature in °C |
| `pressure` | float | Pressure in kPa |
| `roll` | float | Roll angle in degrees |
| `pitch` | float | Pitch angle in degrees |
| `yaw` | float | Yaw angle in degrees |
| `angular_velocity` | float | deg/s |
| `linear_acceleration` | float | m/s² |
| `voltage` | float | System voltage in V |
| `thruster_left` | float | [-1, 1] |
| `thruster_right` | float | [-1, 1] |
| `thruster_vertical` | float | [-1, 1] |
| `status` | string | "nominal" | "warning" | "critical" |

**Example:**
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

### 2. Control Command (`control_command`)

Sent from ground station to firmware.

| Field | Type | Description |
|-------|------|-------------|
| `left_thruster` | float | [-1, 1] |
| `right_thruster` | float | [-1, 1] |
| `vertical_thruster` | float | [-1, 1] |
| `timestamp` | float | Seconds since epoch |

**Example:**
```json
{
  "type": "control_command",
  "timestamp": 1793874420.123,
  "payload": {
    "left_thruster": 0.5,
    "right_thruster": 0.5,
    "vertical_thruster": 0.0
  }
}
```

### 3. Configuration (`configuration`)

Sent from ground station to configure firmware parameters.

| Field | Type | Description |
|-------|------|-------------|
| `max_depth` | float | Maximum depth in meters |
| `max_voltage` | float | Maximum system voltage in V |
| `pid_gains` | object | PID controller gains |
| `sensor_config` | object | Sensor configuration |

**Example:**
```json
{
  "type": "configuration",
  "timestamp": 1793874420.123,
  "payload": {
    "max_depth": 100.0,
    "max_voltage": 16.8,
    "pid_gains": {
      "kp": 1.0,
      "ki": 0.1,
      "kd": 0.05
    },
    "sensor_config": {
      "enable_imu": true,
      "enable_depth": true
    }
  }
}
```

### 4. Alert (`alert`)

Sent from firmware to ground station for abnormal conditions.

| Field | Type | Description |
|-------|------|-------------|
| `level` | string | "warning" | "critical" |
| `code` | string | Alert code identifier |
| `message` | string | Human-readable description |
| `timestamp` | float | Seconds since epoch |

**Example:**
```json
{
  "type": "alert",
  "timestamp": 1793874420.123,
  "payload": {
    "level": "warning",
    "code": "OVER_VOLTAGE",
    "message": "Voltage exceeded 15V threshold"
  }
}
```

## Message Transmission

- **Transport**: UDP over IPv4
- **Port**: 5678 (configurable)
- **Encoding**: UTF-8 JSON
- **Direction**: 
  - Firmware → Ground Station: `firmware_status` and `alert`
  - Ground Station → Firmware: `control_command` and `configuration`
- **Rate**: 20Hz minimum for status messages

## Validation

All messages are validated using Pydantic models defined in `protocol/models.py`. Invalid messages are logged and discarded.

## Versioning

- **Protocol Version**: 1.0.0
- **Compatible Firmware**: >= 0.1.0
- **Breaking Changes**: Require protocol version bump