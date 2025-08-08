# ADC Comparison Test Report: 10-bit vs 12-bit Performance Analysis

**Date:** August 7, 2025  
**Repository:** CR6Community-Marlin_TB  
**Branch:** test-stm32-adc-fixes  
**Testing Platform:** Creality CR-6 SE with STM32F103RET6 motherboard  

## Executive Summary

Comparative performance analysis of 10-bit versus 12-bit ADC configurations on STM32F103RET6-based 3D printer firmware shows **no measurable advantage** for 12-bit ADC implementation in temperature stability or control precision. Based on rigorous testing using identical hardware, environmental conditions, and standardized test protocols, the upgrade from 10-bit to 12-bit ADC resolution does not provide sufficient benefit to justify implementation.

## Test Methodology

### Hardware Configuration
- **Printer:** Creality CR-6 SE
- **Motherboard:** STM32F103RET6 (stock v1.1.0.3 ERA)
- **Hotend Thermistor:** PT1000 (sensor_0 = 1047)
- **Bed Thermistor:** Stock NTC thermistor
- **Hotend:** All-metal configuration (HEATER_0_MAXTEMP 375°C)

### Test Protocol
1. **Firmware Preparation**
   - Flash 10-bit ADC firmware configuration
   - Perform PID autotune: `M303 E0 S200 C8`
   - Save settings: `M500`
   - Allow thermal stabilization (30+ seconds)

2. **Data Collection**
   - Set target temperatures: Hotend 200°C, Bed 60°C
   - Monitor for 5-minute duration using `temp_plotter_clean.py`
   - Sample interval: 1.0 seconds (300 data points)
   - Record temperature stability metrics

3. **Firmware Switch and Repeat**
   - Flash 12-bit ADC firmware configuration
   - Repeat identical test protocol
   - Maintain consistent environmental conditions

### Measurement Tools
- **Primary Tool:** `temp_plotter_clean.py` with matplotlib visualization
- **Configuration:** Standard settings from `config.json`
- **Metrics Collected:**
  - Temperature standard deviation
  - Peak-to-peak temperature range
  - Real-time graphical visualization
  - Statistical stability assessment

## Test Results

### Visual Analysis
The following comparison graphs demonstrate temperature stability over identical 5-minute monitoring periods:

- [**`ADC-10bits_200C_60C.png`**](./Sample Plots/ADC-10bits_200C_60C.png) - 10-bit ADC performance baseline
- [**`ADC-12bits_200C_60C.png`**](./Sample Plots/ADC-12bits_200C_60C.png) - 12-bit ADC performance comparison

### Performance Metrics

| Configuration | Hotend Stability | Bed Stability | Overall Assessment |
|---------------|------------------|---------------|-------------------|
| 10-bit ADC    | Comparable       | Comparable    | Baseline performance |
| 12-bit ADC    | No improvement   | No improvement| Equivalent performance |

### Key Findings

1. **Temperature Stability:** Both configurations exhibit equivalent temperature stability profiles with similar standard deviation and peak-to-peak ranges.

2. **Noise Performance:** No observable reduction in temperature reading noise or quantization artifacts with 12-bit ADC.

3. **Control Response:** PID control effectiveness appears identical between configurations, suggesting thermal mass and heater characteristics dominate system response rather than ADC resolution.

## Analysis and Interpretation

### ADC Resolution Context
- **10-bit ADC:** 1024 discrete levels across measurement range
- **12-bit ADC:** 4096 discrete levels across measurement range  
- **Theoretical Improvement:** 4x resolution increase

### Practical Limitations
Despite the theoretical 4x resolution improvement, several factors explain the absence of measurable benefits:

1. **Thermistor Characteristics:** PT1000 and NTC thermistor inherent noise and response characteristics may exceed ADC quantization noise

2. **Electrical Noise:** System electrical noise (power supply ripple, switching noise, EMI) may mask ADC resolution benefits

3. **PID Controller Saturation:** PID control algorithms may be optimized for 10-bit resolution and not take advantage of higher precision

### Stability Classification
Using the analysis thresholds from `config.json`:
- **Excellent:** Standard deviation < 0.15°C, Range < 0.5°C
- **Good:** Standard deviation < 0.25°C, Range < 1.0°C  
- **Fair:** Standard deviation < 0.5°C, Range < 2.0°C

Both configurations achieved similar stability classifications, indicating ADC resolution is not the performance bottleneck.

## Conclusion and Recommendations

### Primary Conclusion
**The upgrade from 10-bit to 12-bit ADC resolution provides no measurable improvement in temperature control performance** for the tested STM32F103RET6-based 3D printer configuration.

### Technical Rationale
1. **System-Limited Performance:** Temperature control performance appears limited by thermal system characteristics rather than ADC resolution
2. **Noise Floor Dominance:** Other noise sources mask potential ADC resolution benefits
3. **PID Control Adequacy:** Current PID control algorithms achieve stable performance with 10-bit resolution

### Recommendations

#### For Development Priority:
1. **Maintain 10-bit ADC configuration** as the standard implementation
2. **Focus optimization efforts** on PID tuning algorithms and thermal system improvements
3. **Investigate alternative improvements** such as thermistor upgrade paths, noise reduction techniques, improvements to PID control or alternatives to PID control

#### For Future Investigation:
1. **Test with higher-precision thermistors** (e.g., PT100, high-grade NTC) to determine if measurement precision becomes ADC-limited
2. **Evaluate electrical noise reduction** techniques to lower system noise floor
3. **Consider ADC oversampling** techniques as an alternative to higher bit-depth ADCs

#### For Documentation:
1. **Update firmware documentation** to reflect ADC configuration decisions based on empirical testing
2. **Document test methodology** for future hardware evaluation projects
3. **Establish baseline performance metrics** for regression testing

## Test Environment Details

### Software Configuration
- **Monitoring Tools:** Python-based temperature analysis suite
- **Data Visualization:** matplotlib with real-time plotting
- **Statistical Analysis:** numpy-based stability metrics
- **Configuration Management:** JSON-based centralized settings

### Test Repeatability
- All tests conducted on identical hardware
- Consistent environmental conditions maintained
- Standardized firmware flashing and calibration procedures
- Reproducible test protocols documented in repository

### Data Integrity
- Raw temperature data collected at 1Hz sampling rate
- No post-processing filtering applied to maintain measurement fidelity
- Statistical calculations performed using standard numpy functions
- Graphical outputs saved for visual verification and future reference

---

**Report Generated:** August 7, 2025  
**Testing Tools:** CR6Community-Marlin_TB/tools/temperature-monitoring/  
**Graphs Referenced:** Sample Plots/ADC-10bits_200C_60C.png, ADC-12bits_200C60C.png, ADC-12bits_200C_60C_fanAt140secs.png
