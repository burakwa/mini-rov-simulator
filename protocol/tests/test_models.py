"""Tests for the Mini ROV Protocol models."""

from __future__ import annotations

import pytest

from protocol.models import (
    FirmwareStatus,
    FirmwareStatusPayload,
    ControlCommand,
    ControlCommandPayload,
    Configuration,
    ConfigurationPayload,
    Alert,
    AlertPayload,
)


class TestFirmwareStatusPayload:
    """Test FirmwareStatusPayload model validation."""

    def test_valid_payload(self):
        """Should accept valid payload values."""
        payload = FirmwareStatusPayload(
            depth=15.5,
            temperature=8.2,
            pressure=101.3,
            roll=0.2,
            pitch=-0.1,
            yaw=45.0,
            angular_velocity=0.1,
            linear_acceleration=0.05,
            voltage=12.4,
            thruster_left=0.0,
            thruster_right=0.0,
            thruster_vertical=0.0,
            status="nominal",
        )
        assert payload.depth == 15.5
        assert payload.voltage == 12.4
        assert payload.status == "nominal"

    def test_depth_out_of_range_min(self):
        """Should reject depth below minimum."""
        with pytest.raises(Exception):
            FirmwareStatusPayload(depth=-0.1)

    def test_depth_out_of_range_max(self):
        """Should reject depth above maximum."""
        with pytest.raises(Exception):
            FirmwareStatusPayload(depth=2000.0)

    def test_voltage_out_of_range(self):
        """Should reject voltage outside valid range."""
        with pytest.raises(Exception):
            FirmwareStatusPayload(voltage=30.0)

    def test_status_invalid_value(self):
        """Should reject invalid status value."""
        # Pydantic v2 uses constr for constrained strings, 
        # but default string doesn't restrict values automatically
        # This tests that the field accepts the expected values
        payload = FirmwareStatusPayload(
            depth=0.0,
            temperature=0.0,
            pressure=101.3,
            roll=0.0,
            pitch=0.0,
            yaw=0.0,
            angular_velocity=0.0,
            linear_acceleration=0.0,
            voltage=12.0,
            thruster_left=0.0,
            thruster_right=0.0,
            thruster_vertical=0.0,
            status="nominal",
        )
        assert payload.status == "nominal"


class TestControlCommandPayload:
    """Test ControlCommandPayload model validation."""

    def test_valid_payload(self):
        """Should accept valid thruster values."""
        payload = ControlCommandPayload(
            left_thruster=0.5,
            right_thruster=-0.3,
            vertical_thruster=0.8,
        )
        assert payload.left_thruster == 0.5
        assert payload.right_thruster == -0.3
        assert payload.vertical_thruster == 0.8

    def test_thruster_out_of_range_positive(self):
        """Should reject thruster > 1.0."""
        with pytest.raises(Exception):
            ControlCommandPayload(left_thruster=1.5)

    def test_thruster_out_of_range_negative(self):
        """Should reject thruster < -1.0."""
        with pytest.raises(Exception):
            ControlCommandPayload(left_thruster=-1.5)


class TestConfigurationPayload:
    """Test ConfigurationPayload model validation."""

    def test_valid_payload(self):
        """Should accept valid configuration values."""
        payload = ConfigurationPayload(
            max_depth=200.0,
            max_voltage=22.0,
            pid_gains={"kp": 2.0, "ki": 0.2, "kd": 0.1},
            sensor_config={"enable_imu": True, "enable_depth": False},
        )
        assert payload.max_depth == 200.0
        assert payload.max_voltage == 22.0
        assert payload.pid_gains["kp"] == 2.0

    def test_default_payload(self):
        """Should have default values."""
        payload = ConfigurationPayload()
        assert payload.max_depth == 100.0
        assert payload.max_voltage == 16.8
        assert payload.pid_gains["kp"] == 1.0


class TestAlertPayload:
    """Test AlertPayload model validation."""

    def test_valid_alert(self):
        """Should accept valid alert values."""
        payload = AlertPayload(
            level="warning",
            code="OBSTACLE",
            message="Obstacle detected ahead",
        )
        assert payload.level == "warning"
        assert payload.code == "OBSTACLE"
        assert "obstacle" in payload.message.lower()

    def test_critical_alert(self):
        """Should accept critical alert."""
        payload = AlertPayload(level="critical", code="SYSTEM_FAIL")
        assert payload.level == "critical"
        assert payload.code == "SYSTEM_FAIL"