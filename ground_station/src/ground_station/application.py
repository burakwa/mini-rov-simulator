"""Mini ROV Ground Station Application."""

from __future__ import annotations

import math
import time
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


class ImuData(BaseModel):
    """Inertial Measurement Unit data."""
    roll: float = Field(default=0.0, description="Roll angle in degrees")
    pitch: float = Field(default=0.0, description="Pitch angle in degrees")
    yaw: float = Field(default=0.0, description="Yaw angle in degrees")
    angular_velocity: float = Field(
        default=0.0, description="Angular velocity in deg/s"
    )
    linear_acceleration: float = Field(
        default=0.0, description="Linear acceleration in m/s²"
    )


class DepthData(BaseModel):
    """Depth/temperature sensor data."""
    depth: float = Field(default=0.0, description="Depth in meters")
    temperature: float = Field(
        default=0.0, description="Temperature in °C"
    )
    pressure: float = Field(
        default=0.0, description="Pressure in kPa"
    )


class ThrusterData(BaseModel):
    """Thruster output data."""
    left_thruster: float = Field(
        default=0.0, description="Left thruster [-1, 1]"
    )
    right_thruster: float = Field(
        default=0.0, description="Right thruster [-1, 1]"
    )
    vertical_thruster: float = Field(
        default=0.0, description="Vertical thruster [-1, 1]"
    )


class ROVState(BaseModel):
    """Complete ROV state snapshot."""
    timestamp: float = Field(default_factory=time.time)
    imu: ImuData = Field(default_factory=ImuData)
    depth: DepthData = Field(default_factory=DepthData)
    thrusters: ThrusterData = Field(default_factory=ThrusterData)
    voltage: float = Field(default=12.0, description="System voltage in V")


# ---------------------------------------------------------------------------
# GUI Application
# ---------------------------------------------------------------------------


class ROVApp:
    """Main ground station application."""

    def __init__(self) -> None:
        self.state: Optional[ROVState] = None
        self.running: bool = False

        # Plot data history
        self.history_size: int = 50
        self.time_history: list[float] = []
        self.roll_history: list[float] = []
        self.pitch_history: list[float] = []
        self.yaw_history: list[float] = []
        self.depth_history: list[float] = []
        self.voltage_history: list[float] = []

        # Initialize matplotlib
        self.fig, self.axes = plt.subplots(
            2, 2, figsize=(12, 8)
        )
        self.fig.suptitle("Mini ROV Ground Station", fontsize=16)

        # Top-left: IMU visualization
        self.ax_roll = self.axes[0, 0]
        self.ax_pitch = self.axes[0, 1]
        self.ax_yaw = self.axes[1, 0]
        self.ax_status = self.axes[1, 1]

        self._init_plots()

        # Simulated firmware connection
        self._connect_simulation()

    def _init_plots(self) -> None:
        """Initialize plot styles and limits."""
        # Roll plot
        self.ax_roll.set_title("Roll")
        self.ax_roll.set_ylabel("deg")
        self.ax_roll.set_ylim(-30, 30)
        self.ax_roll.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        self.roll_line, = self.ax_roll.plot(
            [], [], "b-", linewidth=2, label="Roll"
        )
        self.ax_roll.legend(loc="upper right")

        # Pitch plot
        self.ax_pitch.set_title("Pitch")
        self.ax_pitch.set_ylabel("deg")
        self.ax_pitch.set_ylim(-30, 30)
        self.ax_pitch.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        self.pitch_line, = self.ax_pitch.plot(
            [], [], "r-", linewidth=2, label="Pitch"
        )
        self.ax_pitch.legend(loc="upper right")

        # Yaw plot
        self.ax_yaw.set_title("Yaw")
        self.ax_yaw.set_ylabel("deg")
        self.ax_yaw.set_ylim(-180, 180)
        self.ax_yaw.axhline(0, color="gray", linestyle="--", linewidth=0.5)
        self.yaw_line, = self.ax_yaw.plot(
            [], [], "g-", linewidth=2, label="Yaw"
        )
        self.ax_yaw.legend(loc="upper right")

        # Status plot
        self.ax_status.set_title("System Status")
        self.ax_status.set_ylabel("Value")
        self.ax_status.set_ylim(0, 15)
        self.voltage_line, = self.ax_status.plot(
            [], [], "m-", linewidth=2, label="Voltage (V)"
        )
        self.status_text = self.ax_status.text(
            0.02, 0.95, "", transform=self.ax_status.transAxes
        )
        self.ax_status.legend(loc="upper right")

        # Format all axes
        for ax in self.axes.flat:
            ax.set_xlabel("Time (s)")
            ax.grid(True, alpha=0.3)
            ax.set_xlim(0, self.history_size)

    def _connect_simulation(self) -> None:
        """Connect to simulated firmware/ROV state."""
        # In a production system, this would connect to the actual
        # firmware via UDP/TCP or shared memory
        self.running = True
        # Start with static state
        self.state = ROVState()

    def _update_from_firmware(self) -> None:
        """Update state from firmware simulation."""
        # This would receive data from the actual firmware
        # For now, generate subtle simulated movement
        if self.state is None:
            return

        # Sim gentle oscillations
        t = self.state.timestamp
        # Approximately 60 FPS update interval (16ms dt)

        # Small sinusoidal movements
        roll_offset = 2.0 * math.sin(t * 0.5)
        pitch_offset = 1.5 * math.cos(t * 0.7)
        yaw_offset = 1.0 * math.sin(t * 1.1)
        depth_offset = 0.1 * math.sin(t * 0.3)

        self.state = ROVState(
            timestamp=t,
            imu=ImuData(
                roll=self.state.imu.roll + roll_offset,
                pitch=self.state.imu.pitch + pitch_offset,
                yaw=self.state.imu.yaw + yaw_offset,
                angular_velocity=self.state.imu.angular_velocity * 0.98
                + 0.02,
                linear_acceleration=self.state.imu.linear_acceleration * 0.95,
            ),
            depth=DepthData(
                depth=self.state.depth.depth + depth_offset,
                temperature=self.state.depth.temperature
                + 0.01 * __import__("math").sin(t),
                pressure=self.state.depth.pressure + 0.05,
            ),
            thrusters=self.state.thrusters,
            voltage=self.state.voltage,
        )

    def _update_plots(self, frame: int) -> list:
        """Update all plots for animation frame."""
        self._update_from_firmware()

        if self.state is None:
            return []

        t = len(self.time_history)
        self.time_history.append(t)
        self.roll_history.append(self.state.imu.roll)
        self.pitch_history.append(self.state.imu.pitch)
        self.yaw_history.append(self.state.imu.yaw)
        self.depth_history.append(self.state.depth.depth)
        self.voltage_history.append(self.state.voltage)

        # Keep history bounded
        if len(self.time_history) > self.history_size:
            self.time_history.pop(0)
            self.roll_history.pop(0)
            self.pitch_history.pop(0)
            self.yaw_history.pop(0)
            self.depth_history.pop(0)
            self.voltage_history.pop(0)

        # Update roll line
        self.roll_line.set_data(
            list(range(len(self.roll_history))), self.roll_history
        )
        self.ax_roll.set_xlim(0, max(self.history_size, len(self.roll_history)))

        # Update pitch line
        self.pitch_line.set_data(
            list(range(len(self.pitch_history))), self.pitch_history
        )
        self.ax_pitch.set_xlim(0, max(self.history_size, len(self.pitch_history)))

        # Update yaw line
        self.yaw_line.set_data(
            list(range(len(self.yaw_history))), self.yaw_history
        )
        self.ax_yaw.set_xlim(0, max(self.history_size, len(self.yaw_history)))

        # Update voltage/status line
        self.voltage_line.set_data(
            list(range(len(self.voltage_history))), self.voltage_history
        )
        self.ax_status.set_xlim(0, max(self.history_size, len(self.voltage_history)))

        # Status text
        self.status_text.set_text(
            f"Time: {t:.1f}s | "
            f"Depth: {self.state.depth.depth:.1f}m | "
            f"Voltage: {self.state.voltage:.1f}V | "
            f"Roll: {self.state.imu.roll:.1f}° | "
            f"Pitch: {self.state.imu.pitch:.1f}° | "
            f"Yaw: {self.state.imu.yaw:.1f}°"
        )

        return [
            self.roll_line,
            self.pitch_line,
            self.yaw_line,
            self.voltage_line,
            self.status_text,
        ]

    def run(self) -> None:
        """Run the application main loop."""
        try:
            anim = FuncAnimation(
                self.fig,
                self._update_plots,
                interval=50,  # ~20 FPS update
                blit=False,
                cache_frame_data=False,
            )

        except Exception as e:
            print(f"Animation error: {e}")
            raise

        # Add manual control instructions
        self._show_instructions()

        plt.tight_layout()
        plt.show()

    def _show_instructions(self) -> None:
        """Display control instructions."""
        instructions = (
            "Mini ROV Ground Station Controls:\n"
            "  - W/S: Forward/Backward (Vertical Thruster)\n"
            "  - A/D: Left/Right (Lateral Thruster)\n"
            "  - Arrow Keys: Yaw Left/Right\n"
            "  - SPACE: Stop all thrusters\n"
            "  - Q/E: Increase/Decrease Voltage\n"
            "  - R: Reset simulation\n"
            "  - ESC: Close application"
        )
        print(instructions)