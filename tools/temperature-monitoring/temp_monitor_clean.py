#!/usr/bin/env python3
"""
Simple temperature monitor for 3D printer via serial connection.
Monitors hotend and bed temperatures to evaluate 12-bit ADC improvements.
"""

import signal
import sys
import time
from datetime import datetime
from typing import List, Optional, Tuple

try:
    import serial
except ImportError:
    print("Error: pyserial not installed.")
    print("On Ubuntu/Debian, run: sudo apt install python3-serial")
    print("Or in a virtual environment: pip install pyserial")
    sys.exit(1)


class SimpleTemperatureMonitor:
    """Simple temperature monitoring for 3D printer ADC evaluation."""

    def __init__(self, port: str = '/dev/ttyUSB0', baud: int = 115200, timeout: int = 2):
        """Initialize the temperature monitor."""
        self.serial_port = port
        self.baud_rate = baud
        self.timeout = timeout
        self.serial_connection: Optional[serial.Serial] = None

        # Setup signal handler
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, _sig: int, _frame) -> None:
        """Handle Ctrl+C signal gracefully."""
        print('\nStopping temperature monitor...')
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
            time.sleep(2)  # Wait for connection to stabilize
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
            print(f"Sent: {command}")
        except (serial.SerialException, OSError) as error:
            print(f"Error sending command: {error}")

    def read_response(self) -> str:
        """Read response from printer."""
        if not self.serial_connection:
            return ""

        try:
            response = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
            return response
        except (serial.SerialException, UnicodeDecodeError) as error:
            print(f"Error reading response: {error}")
            return ""

    def parse_temperatures(self, response: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse temperature response and return as strings."""
        hotend_temp = None
        bed_temp = None

        # Extract hotend temperature
        if "T:" in response:
            try:
                t_start = response.find("T:") + 2
                t_end = response.find(" ", t_start)
                if t_end == -1:
                    t_end = response.find("/", t_start)
                hotend_temp = response[t_start:t_end]
            except (ValueError, IndexError):
                hotend_temp = "N/A"

        # Extract bed temperature
        if "B:" in response:
            try:
                b_start = response.find("B:") + 2
                b_end = response.find(" ", b_start)
                if b_end == -1:
                    b_end = response.find("/", b_start)
                bed_temp = response[b_start:b_end]
            except (ValueError, IndexError):
                bed_temp = "N/A"

        return hotend_temp, bed_temp

    def calculate_statistics(self, temperatures: List[float], name: str) -> None:
        """Calculate and print temperature statistics."""
        if not temperatures:
            return

        print(f"\n{name} Temperature Statistics:")
        print(f"  Samples: {len(temperatures)}")
        print(f"  Average: {sum(temperatures)/len(temperatures):.2f}°C")
        print(f"  Min: {min(temperatures):.2f}°C")
        print(f"  Max: {max(temperatures):.2f}°C")
        print(f"  Range: {max(temperatures) - min(temperatures):.2f}°C")

    def monitor_temperatures(self, duration_minutes: int = 10) -> None:
        """Monitor temperatures for specified duration."""
        print(f"\nStarting temperature monitoring for {duration_minutes} minutes...")
        print("Time\t\tHotend\tBed\tAmbient")
        print("-" * 50)

        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)

        hotend_temps: List[float] = []
        bed_temps: List[float] = []

        while time.time() < end_time:
            try:
                # Request temperature report
                self.send_command("M105")

                # Read response
                response = self.read_response()

                if response and "T:" in response:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    hotend_temp, bed_temp = self.parse_temperatures(response)

                    # Store temperatures for analysis
                    if hotend_temp and hotend_temp != "N/A":
                        try:
                            hotend_temps.append(float(hotend_temp))
                        except ValueError:
                            pass

                    if bed_temp and bed_temp != "N/A":
                        try:
                            bed_temps.append(float(bed_temp))
                        except ValueError:
                            pass

                    print(f"{current_time}\t{hotend_temp or 'N/A'}°C\t{bed_temp or 'N/A'}°C\t-")

                    # Also print raw response for debugging
                    print(f"Raw: {response}")

                time.sleep(2)  # Read every 2 seconds

            except KeyboardInterrupt:
                break
            except (serial.SerialException, OSError, UnicodeDecodeError) as error:
                print(f"Error during monitoring: {error}")
                time.sleep(1)

        # Print statistics
        self.calculate_statistics(hotend_temps, "Hotend")
        self.calculate_statistics(bed_temps, "Bed")

    def run(self, duration_minutes: int = 5) -> None:
        """Main execution method."""
        print("3D Printer Temperature Monitor")
        print("Testing 12-bit ADC improvements (STM32F103RET6, BTT SKR boards, etc.)")
        print("=" * 72)

        # Connect to printer
        if not self.connect_printer():
            print("Cannot connect to printer. Exiting.")
            return

        try:
            # Send initial commands
            print("\nInitializing printer communication...")
            self.send_command("M115")  # Get firmware version
            time.sleep(1)

            # Read any initial responses
            for _ in range(5):
                response = self.read_response()
                if response:
                    print(f"Response: {response}")

            # Start temperature monitoring
            self.monitor_temperatures(duration_minutes)

        except KeyboardInterrupt:
            pass
        except (serial.SerialException, OSError, UnicodeDecodeError) as error:
            print(f"Error during operation: {error}")
        finally:
            if self.serial_connection:
                print("\nClosing connection...")
                self.serial_connection.close()


def main() -> None:
    """Main entry point."""
    monitor = SimpleTemperatureMonitor()
    monitor.run(duration_minutes=5)


if __name__ == "__main__":
    main()
