#!/usr/bin/env python3
"""
Real-time temperature plotter for 3D printer via serial connection.
Visualizes temperature stability to evaluate 12-bit ADC improvements.
"""

import signal
import sys
import time
from collections import deque
from typing import Optional, Deque

try:
    import serial
except ImportError:
    print("Error: pyserial not installed.")
    print("On Ubuntu/Debian, run: sudo apt install python3-serial")
    print("Or in a virtual environment: pip install pyserial")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np
except ImportError:
    print("Error: matplotlib and numpy required.")
    print("On Ubuntu/Debian, run: sudo apt install python3-matplotlib python3-numpy")
    print("Or in a virtual environment: pip install matplotlib numpy")
    sys.exit(1)

# Import shared configuration
try:
    from temp_config import config
except ImportError:
    print("Error: temp_config.py not found.")
    print("Please ensure temp_config.py is in the same directory.")
    sys.exit(1)


class TemperaturePlotter:
    """Real-time temperature plotter for 3D printer ADC evaluation."""

    def __init__(self, port: Optional[str] = None, baud: Optional[int] = None):
        """Initialize the temperature plotter with config file settings."""
        self.serial_port = port or config.serial_port
        self.baud_rate = baud or config.baud_rate
        self.timeout = config.timeout

        # Data storage
        maxlen = config.max_data_points
        self.times: Deque[float] = deque(maxlen=maxlen)
        self.hotend_temps: Deque[float] = deque(maxlen=maxlen)
        self.bed_temps: Deque[float] = deque(maxlen=maxlen)
        self.start_time: Optional[float] = None
        self.serial_connection: Optional[serial.Serial] = None

        # Setup plot
        plot_config = config.get_plotting_config()
        fig_width = plot_config.get('figure_size_width', 12)
        fig_height = plot_config.get('figure_size_height', 8)
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(fig_width, fig_height))

        # Setup signal handler
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, _sig: int, _frame) -> None:
        """Handle Ctrl+C signal gracefully."""
        print('\nStopping temperature plotter...')
        if self.serial_connection:
            self.serial_connection.close()
        plt.close('all')
        sys.exit(0)

    def connect_printer(self) -> bool:
        """Connect to the printer via serial."""
        try:
            self.serial_connection = serial.Serial(
                self.serial_port, self.baud_rate, timeout=self.timeout
            )
            print(f"Connected to printer on {self.serial_port} at {self.baud_rate} baud")
            time.sleep(config.stabilization_delay)  # Wait for connection to stabilize
            return True
        except (serial.SerialException, OSError) as error:
            print(f"Failed to connect to printer: {error}")
            return False

    def send_command(self, command: str) -> None:
        """Send a G-code command to the printer."""
        if not self.serial_connection:
            return

        try:
            cmd = command.strip() + '\n'
            self.serial_connection.write(cmd.encode())
            self.serial_connection.flush()
        except (serial.SerialException, OSError) as error:
            print(f"Error sending command: {error}")

    def read_response(self) -> str:
        """Read response from printer."""
        if not self.serial_connection:
            return ""

        try:
            response = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
            return response
        except (serial.SerialException, UnicodeDecodeError):
            return ""

    def parse_temperature(self, response: str) -> tuple[Optional[float], Optional[float]]:
        """Parse M105 temperature response."""
        hotend_temp = None
        bed_temp = None

        if "T:" in response:
            try:
                # Extract hotend temperature
                t_start = response.find("T:") + 2
                t_end = response.find(" ", t_start)
                if t_end == -1:
                    t_end = response.find("/", t_start)
                hotend_temp = float(response[t_start:t_end])
            except (ValueError, IndexError):
                pass

        if "B:" in response:
            try:
                # Extract bed temperature
                b_start = response.find("B:") + 2
                b_end = response.find(" ", b_start)
                if b_end == -1:
                    b_end = response.find("/", b_start)
                bed_temp = float(response[b_start:b_end])
            except (ValueError, IndexError):
                pass

        return hotend_temp, bed_temp

    def update_plot(self, _frame: int) -> None:
        """Update the temperature plots."""
        if not self.serial_connection:
            return

        # Send temperature request
        self.send_command(config.temperature_command)

        # Read response
        response = self.read_response()

        if response and "T:" in response:
            hotend_temp, bed_temp = self.parse_temperature(response)

            if hotend_temp is not None and bed_temp is not None:
                # Add timestamp
                if self.start_time is None:
                    self.start_time = time.time()

                current_time = time.time() - self.start_time
                self.times.append(current_time)
                self.hotend_temps.append(hotend_temp)
                self.bed_temps.append(bed_temp)

                # Clear and redraw plots
                self.ax1.clear()
                self.ax2.clear()

                if len(self.times) > 1:
                    # Plot hotend temperature
                    self.ax1.plot(list(self.times), list(self.hotend_temps),
                                 'r-', linewidth=1, label='Hotend')
                    self.ax1.set_ylabel('Hotend Temperature (°C)')
                    self.ax1.set_title('Hotend Temperature Stability (ADC Testing)')
                    self.ax1.grid(True, alpha=0.3)
                    self.ax1.legend()

                    # Calculate and display statistics
                    if len(self.hotend_temps) > 10:
                        hotend_array = np.array(list(self.hotend_temps))
                        std_dev = np.std(hotend_array)
                        mean_temp = np.mean(hotend_array)
                        peak_to_peak = np.max(hotend_array) - np.min(hotend_array)

                        stats_text = f'Mean: {mean_temp:.3f}°C\nStd Dev: {std_dev:.3f}°C\nP-P: {peak_to_peak:.3f}°C'
                        self.ax1.text(0.02, 0.98, stats_text,
                                     transform=self.ax1.transAxes, verticalalignment='top',
                                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

                    # Plot bed temperature
                    self.ax2.plot(list(self.times), list(self.bed_temps),
                                 'b-', linewidth=1, label='Bed')
                    self.ax2.set_xlabel('Time (seconds)')
                    self.ax2.set_ylabel('Bed Temperature (°C)')
                    self.ax2.set_title('Bed Temperature Stability (ADC Testing)')
                    self.ax2.grid(True, alpha=0.3)
                    self.ax2.legend()

                    # Calculate and display statistics
                    if len(self.bed_temps) > 10:
                        bed_array = np.array(list(self.bed_temps))
                        std_dev = np.std(bed_array)
                        mean_temp = np.mean(bed_array)
                        peak_to_peak = np.max(bed_array) - np.min(bed_array)

                        stats_text = f'Mean: {mean_temp:.3f}°C\nStd Dev: {std_dev:.3f}°C\nP-P: {peak_to_peak:.3f}°C'
                        self.ax2.text(0.02, 0.98, stats_text,
                                     transform=self.ax2.transAxes, verticalalignment='top',
                                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

                print(f"Time: {current_time:6.1f}s  Hotend: {hotend_temp:6.2f}°C  Bed: {bed_temp:6.2f}°C")

    def run(self) -> None:
        """Main execution method."""
        print("3D Printer Temperature Plotter")
        print("Testing ADC improvements (STM32F103RET6, BTT SKR boards, etc.)")
        print("=" * 56)
        print("Close the plot window to exit")
        
        # Display configuration
        config.print_config_summary()
        print()

        # Connect to printer
        if not self.connect_printer():
            print("Cannot connect to printer. Exiting.")
            return

        try:
            # Initialize plot
            plt.tight_layout()
            plt.ion()  # Interactive mode

            # Start animation with configured update interval
            update_interval = config.get('plotting', 'update_interval_ms', 1000)
            _ani = animation.FuncAnimation(
                self.fig, self.update_plot, interval=update_interval, cache_frame_data=False
            )

            # Show plot
            plt.show(block=True)

        except KeyboardInterrupt:
            pass
        except (serial.SerialException, OSError, UnicodeDecodeError) as error:
            print(f"Error during operation: {error}")
        finally:
            print("\nClosing connection...")
            if self.serial_connection:
                self.serial_connection.close()


def main() -> None:
    """Main entry point."""
    plotter = TemperaturePlotter()
    plotter.run()


if __name__ == "__main__":
    main()

