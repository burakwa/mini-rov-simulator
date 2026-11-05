"""Protocol data models - Pydantic models for message validation."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class FirmwareStatusPayload(BaseModel):
    """Payload for firmware_status messages from firmware to ground station."""
    depth: float = Field(
        default=0.0, ge=0.0, le=1000.0, description="Depth in meters"
    )
    temperature: float = Field(
        default=0.0, ge=-50.0, le=100.0, description="Temperature in °C"
    )
    pressure: float = Field(
        default=101.3, ge=80.0, le=120.0, description="Pressure in kPa"
    )
    roll: float = Field(
        default=0.0, ge=-45.0, le=45.0, description="Roll angle in degrees"
    )
    pitch: float = Field(
        default=0.0, ge=-45.0, le=45.0, description="Pitch angle in degrees"
    )
    yaw: float = Field(
        default=0.0, ge=-180.0, le=180.0, description="Yaw angle in degrees"
    )
    angular_velocity: float = Field(
        default=0.0, ge=-100.0, le=100.0, description="Angular velocity deg/s"
    )
    linear_acceleration: float = Field(
        default=0.0,
        ge=-20.0,
        le=20.0,
        description="Linear acceleration m/s²",
    )
    voltage: float = Field(
        default=12.0, ge=6.0, le=24.0, description="System voltage in V"
    )
    thruster_left: float = Field(
        default=0.0, ge=-1.0, le=1.0, description="Left thruster [-1, 1]"
    )
    thruster_right: float = Field(
        default=0.0, ge=-1.0, le=1.0, description="Right thruster [-1, 1]"
    )
    thruster_vertical: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Vertical thruster [-1, 1]",
    )
    status: str = Field(
        default="nominal",
        description='Status: "nominal" | "warning" | "critical"',
    )


class FirmwareStatus(BaseModel):
    """Full firmware_status message."""
    type: str = Field(default="firmware_status", description="Message type identifier")
    timestamp: float = Field(
        default_factory=lambda: __import__("time").time(),
        description="Unix timestamp in seconds",
    )
    payload: FirmwareStatusPayload = Field(
        default_factory=FirmwareStatusPayload, description="Message payload"
    )


class ControlCommandPayload(BaseModel):
    """Payload for control_command messages from ground station to firmware."""
    left_thruster: float = Field(
        default=0.0, ge=-1.0, le=1.0, description="Left thruster [-1, 1]"
    )
    right_thruster: float = Field(
        default=0.0, ge=-1.0, le=1.0, description="Right thruster [-1, 1]"
    )
    vertical_thruster: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Vertical thruster [-1, 1]",
    )


class ControlCommand(BaseModel):
    """Full control_command message."""
    type: str = Field(
        default="control_command", description="Message type identifier"
    )
    timestamp: float = Field(
        default_factory=lambda: __import__("time").time(),
        description="Unix timestamp in seconds",
    )
    payload: ControlCommandPayload = Field(
        default_factory=ControlCommandPayload, description="Message payload"
    )


class ConfigurationPayload(BaseModel):
    """Payload for configuration messages."""
    max_depth: float = Field(
        default=100.0, ge=0.0, description="Maximum depth in meters"
    )
    max_voltage: float = Field(
        default=16.8, ge=0.0, description="Maximum system voltage in V"
    )
    pid_gains: dict = Field(
        default={
            "kp": 1.0,
            "ki": 0.1,
            "kd": 0.05,
        },
        description="PID controller gains {kp, ki, kd}",
    )
    sensor_config: dict = Field(
        default={
            "enable_imu": True,
            "enable_depth": True,
        },
        description="Sensor configuration flags",
    )


class Configuration(BaseModel):
    """Full configuration message."""
    type: str = Field(
        default="configuration", description="Message type identifier"
    )
    timestamp: float = Field(
        default_factory=lambda: __import__("time").time(),
        description="Unix timestamp in seconds",
    )
    payload: ConfigurationPayload = Field(
        default_factory=ConfigurationPayload, description="Message payload"
    )


class AlertPayload(BaseModel):
    """Payload for alert messages from firmware."""
    level: str = Field(
        default="warning",
        description='Alert level: "warning" | "critical"',
    )
    code: str = Field(
        default="GENERIC",
        description="Alert code identifier",
    )
    message: str = Field(
        default="",
        description="Human-readable description",
    )


class Alert(BaseModel):
    """Full alert message."""
    type: str = Field(
        default="alert", description="Message type identifier"
    )
    timestamp: float = Field(
        default_factory=lambda: __import__("time").time(),
        description="Unix timestamp in seconds",
    )
    payload: AlertPayload = Field(
        default_factory=AlertPayload, description="Message payload"
    )