#!/usr/bin/env python3
"""
Shared configuration module for temperature monitoring tools.
Loads settings from config.json file.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any


class TemperatureMonitorConfig:
    """Configuration manager for temperature monitoring tools."""

    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration from JSON file."""
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        # Get the directory where this script is located
        script_dir = Path(__file__).parent
        config_path = script_dir / self.config_file

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            print(f"Error: Configuration file '{config_path}' not found.")
            print("Please ensure config.json exists in the tools directory.")
            sys.exit(1)
        except json.JSONDecodeError as error:
            print(f"Error: Invalid JSON in configuration file: {error}")
            sys.exit(1)
        except (OSError, PermissionError) as error:
            print(f"Error: Cannot read configuration file: {error}")
            sys.exit(1)

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get a configuration value from a specific section."""
        return self.config.get(section, {}).get(key, default)

    def get_serial_config(self) -> Dict[str, Any]:
        """Get all serial communication settings."""
        return self.config.get('serial', {})

    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get all monitoring settings."""
        return self.config.get('monitoring', {})

    def get_display_config(self) -> Dict[str, Any]:
        """Get all display settings."""
        return self.config.get('display', {})

    def get_plotting_config(self) -> Dict[str, Any]:
        """Get all plotting settings."""
        return self.config.get('plotting', {})

    def get_analysis_config(self) -> Dict[str, Any]:
        """Get all analysis settings."""
        return self.config.get('analysis', {})

    @property
    def serial_port(self) -> str:
        """Get serial port setting."""
        return self.get('serial', 'port', '/dev/ttyUSB0')

    @property
    def baud_rate(self) -> int:
        """Get baud rate setting."""
        return self.get('serial', 'baud_rate', 115200)

    @property
    def timeout(self) -> int:
        """Get serial timeout setting."""
        return self.get('serial', 'timeout', 2)

    @property
    def stabilization_delay(self) -> float:
        """Get connection stabilization delay."""
        return self.get('serial', 'stabilization_delay', 2.0)

    @property
    def default_duration_minutes(self) -> int:
        """Get default monitoring duration."""
        return self.get('monitoring', 'default_duration_minutes', 5)

    @property
    def sample_interval(self) -> float:
        """Get sampling interval in seconds."""
        return self.get('monitoring', 'sample_interval_seconds', 1.0)

    @property
    def max_data_points(self) -> int:
        """Get maximum number of data points to store."""
        return self.get('monitoring', 'max_data_points', 300)

    @property
    def temperature_command(self) -> str:
        """Get temperature request command."""
        return self.get('monitoring', 'temperature_request_command', 'M105')

    def print_config_summary(self) -> None:
        """Print a summary of current configuration."""
        print("Temperature Monitor Configuration:")
        print("=" * 40)
        print(f"Serial Port: {self.serial_port}")
        print(f"Baud Rate: {self.baud_rate}")
        print(f"Timeout: {self.timeout}s")
        print(f"Default Duration: {self.default_duration_minutes} minutes")
        print(f"Sample Interval: {self.sample_interval}s")
        print("=" * 40)


# Global configuration instance
config = TemperatureMonitorConfig()
