"""Tests for the Mini ROV Ground Station application."""

from __future__ import annotations

import pytest

from ground_station.application import ROVApp, ROVState, ImuData, DepthData, ThrusterData


class TestDataModels:
    """Test Pydantic data models."""

    def test_imu_data_default(self):
        """ImuData should have default values."""
        data = ImuData()
        assert data.roll == 0.0
        assert data.pitch == 0.0
        assert data.yaw == 0.0

    def test_imu_data_custom(self):
        """ImuData should accept custom values."""
        data = ImuData(roll=5.0, pitch=-3.2, yaw=45.0)
        assert data.roll == 5.0
        assert data.pitch == -3.2
        assert data.yaw == 45.0

    def test_depth_data_default(self):
        """DepthData should have default values."""
        data = DepthData()
        assert data.depth == 0.0
        assert data.temperature == 0.0
        assert data.pressure == 0.0

    def test_depth_data_custom(self):
        """DepthData should accept custom values."""
        data = DepthData(depth=15.5, temperature=8.2, pressure=100.5)
        assert data.depth == 15.5
        assert data.temperature == 8.2
        assert data.pressure == 100.5

    def test_thruster_data_default(self):
        """ThrusterData should have default values."""
        data = ThrusterData()
        assert data.left_thruster == 0.0
        assert data.right_thruster == 0.0
        assert data.vertical_thruster == 0.0

    def test_rov_state_default(self):
        """ROVState should have default values."""
        state = ROVState()
        assert state.timestamp is not None
        assert state.imu.roll == 0.0
        assert state.depth.depth == 0.0
        assert state.thrusters.left_thruster == 0.0
        assert state.voltage == 12.0


class TestROVAppInitialization:
    """Test ROVApp initialization."""

    def test_app_creation(self):
        """ROVApp should create successfully."""
        app = ROVApp()
        assert app is not None
        assert app.state is not None
        assert app.running is True

    def test_app_state_types(self):
        """ROVApp state should have correct types."""
        app = ROVApp()
        state = app.state
        assert hasattr(state, "imu")
        assert hasattr(state, "depth")
        assert hasattr(state, "thrusters")
        assert hasattr(state, "voltage")