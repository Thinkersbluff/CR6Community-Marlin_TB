# Temperature Monitoring Tools for ADC Testing

This directory contains Python tools for monitoring and analyzing 3D printer temperature stability to evaluate ADC (Analog-to-Digital Converter) improvements, specifically comparing 10-bit vs 12-bit ADC performance on various Marlin-compatible boards including STM32F103RET6, BTT SKR series, and others.

## Tools Overview

### 1. `temp_monitor_clean.py` - Basic Temperature Logger
**Purpose**: Simple temperature data collection with statistics
- Connects to printer via serial
- Logs hotend and bed temperatures
- Calculates basic statistics (mean, min, max, range)
- Suitable for automated testing scripts

### 2. `temp_analyzer_clean.py` - Real-time Analysis Monitor
**Purpose**: Live temperature monitoring with visual feedback
- Real-time display with ASCII graphs
- Rolling statistics (last 30 readings)
- Live stability assessment
- Screen clearing for continuous updates
- Best for interactive monitoring sessions

### 3. `temp_plotter_clean.py` - Graphical Real-time Plotter
**Purpose**: Visual temperature plotting with matplotlib
- Real-time temperature graphs
- Statistical overlays (mean, std dev, peak-to-peak)
- 5-minute rolling window
- Professional graphical output
- Requires matplotlib and numpy

## Board Compatibility

These tools work with **any Marlin-compatible 3D printer** that supports standard G-code temperature commands (`M105`). This includes:

- **STM32-based boards**: STM32F103RET6 (stock CR-6), STM32F407 (BTT SKR Pro), STM32F446 (BTT SKR V2)
- **BTT SKR series**: SKR V1.4, SKR V2.0, SKR CR6, SKR E3, etc.
- **LPC-based boards**: SKR V1.3 (LPC1768)
- **Arduino/AVR boards**: RAMPS, MKS, etc.
- **ESP32 boards**: Various WiFi-enabled controllers

The tools are **board-agnostic** because they communicate via standard serial G-code rather than direct hardware access.

## Installation Requirements

### System Dependencies (Ubuntu/Debian)
```bash
sudo apt install python3-serial python3-matplotlib python3-numpy
```

### Virtual Environment (Alternative)
```bash
python3 -m venv venv
source venv/bin/activate
pip install pyserial matplotlib numpy
```

## Usage Instructions

### Basic Usage

1. **Connect your 3D printer** via USB to `/dev/ttyUSB0` (Linux) or appropriate COM port (Windows)

2. **Ensure printer is powered on** and responsive to G-code commands

3. **Run your chosen tool**:
   ```bash
   # Basic logging (5 minutes)
   python3 temp_monitor_clean.py
   
   # Real-time analysis (press Ctrl+C to stop)
   python3 temp_analyzer_clean.py
   
   # Graphical plotting (close window to stop)
   python3 temp_plotter_clean.py
   ```

### Advanced Configuration

All tools can be customized by modifying the class initialization:

```python
# Custom serial port and baud rate
monitor = TemperatureMonitor(port='/dev/ttyUSB1', baud=115200)

# Custom monitoring duration
monitor.run(duration_minutes=10)
```

### Testing Workflow for ADC Comparison

1. **Flash 10-bit ADC firmware** to printer
2. **Run PID autotune**: `M303 E0 S200 C8`
3. **Save settings**: `M500`
4. **Set target temperature**: `M104 S200`
5. **Wait for stability**, then run monitoring tool
6. **Record results** and firmware configuration
7. **Repeat with 12-bit ADC firmware**
8. **Compare results** for temperature stability metrics

### Key Metrics to Monitor

- **Standard Deviation**: Lower = more stable (target: <0.2°C)
- **Temperature Range**: Peak-to-peak variation (target: <1.0°C)
- **Stability Rating**: EXCELLENT/GOOD/FAIR/POOR classification
- **Raw ADC noise**: Visible in temperature fluctuations

## Output Interpretation

### Good ADC Performance Indicators
- Standard deviation < 0.15°C
- Temperature range < 0.5°C over time
- Smooth, consistent readings
- Minimal high-frequency noise

### Poor ADC Performance Indicators
- Standard deviation > 0.3°C
- Large temperature swings (>1°C range)
- Erratic, jumpy readings
- Visible quantization steps

## Troubleshooting

### Connection Issues
- Check serial port permissions: `sudo usermod -a -G dialout $USER`
- Verify correct port: `ls /dev/ttyUSB*` or `dmesg | grep tty`
- Ensure printer is not connected to other software (Pronterface, etc.)

### Import Errors
- Install missing packages with apt or pip
- Check Python version compatibility (Python 3.6+)
- For virtual environments, ensure activation

### Data Quality Issues
- Verify printer is at stable temperature before testing
- Ensure adequate PID tuning for your system
- Check for electrical interference (USB isolation, proper grounding)
- Verify thermistor connections and quality

## File Structure Integration

These tools integrate into the existing Marlin testing infrastructure and can be used alongside PlatformIO build processes for comprehensive ADC validation.
