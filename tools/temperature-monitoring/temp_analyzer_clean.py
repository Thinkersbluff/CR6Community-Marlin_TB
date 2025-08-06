#!/usr/bin/env python3
"""
Real-time temperature monitor for 3D printer via serial connection.
Shows temperature stability in text format to evaluate 12-bit ADC improvements.
"""

import signal
import statistics
import sys
import time
from collections import deque
from datetime import datetime
from typing import Optional, List, Tuple, Deque

try:
    import serial
except ImportError:
    print("Error: pyserial not installed.")
    print("On Ubuntu/Debian, run: sudo apt install python3-serial")
    print("Or in a virtual environment: pip install pyserial")
    sys.exit(1)


class TemperatureMonitor:
    """Monitor and analyze 3D printer temperature stability."""

    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 250000):
        """Initialize temperature monitor."""
        self.serial_port = port
        self.baud_rate = baud
        self.timeout = 1

        self.temps_hotend: Deque[float] = deque(maxlen=60)
        self.temps_bed: Deque[float] = deque(maxlen=60)
        self.start_time: Optional[float] = None
        self.serial_connection: Optional[serial.Serial] = None

        # Setup signal handler
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, _sig: int, _frame) -> None:
        """Handle Ctrl+C signal gracefully."""
        print('\nStopping temperature monitor...')
        self.print_final_stats()
        if self.serial_connection:
            self.serial_connection.close()
        sys.exit(0)

    def connect_printer(self) -> bool:
        """Connect to the printer via serial."""
        try:
            self.serial_connection = serial.Serial(
                self.serial_port, self.baud_rate, timeout=self.timeout
            )
            print(f"Connected to printer on {self.serial_port} at {self.baud_rate} baud")
            time.sleep(1)
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

    def parse_temperature(self, response: str) -> Tuple[Optional[float],
                                                       Optional[float]]:
        """Parse M105 temperature response."""
        hotend_temp = None
        bed_temp = None

        if "T:" in response:
            try:
                t_start = response.find("T:") + 2
                t_end = response.find(" ", t_start)
                if t_end == -1:
                    t_end = response.find("/", t_start)
                hotend_temp = float(response[t_start:t_end])
            except (ValueError, IndexError):
                pass

        if "B:" in response:
            try:
                b_start = response.find("B:") + 2
                b_end = response.find(" ", b_start)
                if b_end == -1:
                    b_end = response.find("/", b_start)
                bed_temp = float(response[b_start:b_end])
            except (ValueError, IndexError):
                pass

        return hotend_temp, bed_temp

    def create_text_graph(self, values: List[float], width: int = 50,
                          label: str = "") -> str:
        """Create a simple ASCII graph."""
        if not values or len(values) < 2:
            return ""

        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val

        if range_val == 0:
            return f"{label}: All values equal to {min_val:.3f}"

        range_info = f"({min_val:.3f} to {max_val:.3f}, range: {range_val:.3f}°C)"
        graph = f"{label} {range_info}:\n"

        # Create graph lines
        for i in range(5, -1, -1):  # 6 levels
            level = min_val + (range_val * i / 5)
            line = f"{level:6.2f} |"

            for val in values[-width:]:  # Last 'width' values
                normalized = (val - min_val) / range_val
                if normalized >= i / 5 - 0.1:
                    line += "*"
                else:
                    line += " "

            graph += line + "\n"

        # Add time axis
        graph += "       +" + "-" * min(len(values), width) + "\n"

        return graph

    def print_stats(self, temps: List[float], label: str) -> None:
        """Print temperature statistics."""
        if len(temps) < 5:
            return

        mean_temp = statistics.mean(temps)
        stdev = statistics.stdev(temps) if len(temps) > 1 else 0
        min_temp = min(temps)
        max_temp = max(temps)
        range_temp = max_temp - min_temp

        print(f"\n{label} Statistics (last {len(temps)} readings):")
        print(f"  Mean: {mean_temp:.4f}°C")
        print(f"  Std Dev: {stdev:.4f}°C")
        range_info = f"(min: {min_temp:.3f}, max: {max_temp:.3f})"
        print(f"  Range: {range_temp:.4f}°C {range_info}")

        stability = "EXCELLENT" if stdev < 0.1 else \
                   "GOOD" if stdev < 0.3 else \
                   "FAIR" if stdev < 0.5 else "POOR"
        print(f"  Stability: {stability}")

    def print_final_stats(self) -> None:
        """Print final statistics summary."""
        print("\n" + "="*60)
        print("FINAL ADC PERFORMANCE ANALYSIS")
        print("="*60)

        if self.temps_hotend:
            self.print_stats(list(self.temps_hotend), "HOTEND")
            print(self.create_text_graph(list(self.temps_hotend), width=40, label="Hotend Graph"))

        if self.temps_bed:
            self.print_stats(list(self.temps_bed), "BED")
            print(self.create_text_graph(list(self.temps_bed), width=40, label="Bed Graph"))

        print("\nWith 12-bit ADC, you should expect:")
        print("  - Standard deviation < 0.2°C for good stability")
        print("  - Range < 1.0°C over time")
        print("  - Smooth, consistent readings")

    def run(self) -> None:
        """Main monitoring loop."""
        print("3D Printer Temperature Monitor - ADC Testing")
        print("Testing temperature stability and noise reduction")
        print("="*60)
        print("Press Ctrl+C to stop and see final statistics\n")

        # Connect to printer
        if not self.connect_printer():
            print("Cannot connect to printer. Exiting.")
            return

        self.start_time = time.time()
        reading_count = 0

        try:
            while True:
                # Send temperature request
                self.send_command("M105")

                # Read response
                response = self.read_response()

                if response and "T:" in response:
                    hotend_temp, bed_temp = self.parse_temperature(response)

                    if hotend_temp is not None and bed_temp is not None:
                        self.temps_hotend.append(hotend_temp)
                        self.temps_bed.append(bed_temp)
                        reading_count += 1

                        elapsed = time.time() - self.start_time
                        current_time = datetime.now().strftime("%H:%M:%S")

                        # Clear screen and show current data
                        print("\033[2J\033[H")  # Clear screen, move cursor to top
                        print("3D Printer Temperature Monitor - ADC Testing")
                        time_info = f"Time: {current_time} | Elapsed: {elapsed:.0f}s"
                        print(f"{time_info} | Readings: {reading_count}")
                        print("="*60)

                        print(f"Current: Hotend {hotend_temp:.3f}°C | Bed {bed_temp:.3f}°C")

                        # Show recent statistics
                        if len(self.temps_hotend) >= 10:
                            hotend_data = list(self.temps_hotend)[-30:]
                            self.print_stats(hotend_data, "Hotend (last 30 readings)")

                        if len(self.temps_bed) >= 10:
                            bed_data = list(self.temps_bed)[-30:]
                            self.print_stats(bed_data, "Bed (last 30 readings)")

                        # Show mini graphs
                        if len(self.temps_hotend) >= 10:
                            print("\nRecent Hotend Trend:")
                            recent_data = list(self.temps_hotend)[-20:]
                            print(self.create_text_graph(recent_data, width=30))

                        print(f"\nRaw response: {response}")
                        print("\nPress Ctrl+C to stop and see final analysis...")

                time.sleep(2)  # Read every 2 seconds

        except KeyboardInterrupt:
            pass
        except (serial.SerialException, OSError, UnicodeDecodeError) as error:
            print(f"Error during monitoring: {error}")
        finally:
            if self.serial_connection:
                print("\nClosing connection...")
                self.serial_connection.close()
            self.print_final_stats()


def main() -> None:
    """Main entry point."""
    monitor = TemperatureMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
