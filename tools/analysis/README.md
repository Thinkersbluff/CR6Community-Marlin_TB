# Analysis Tools

Cross-platform analysis and monitoring tools for firmware performance evaluation and data gathering.

## Directory Structure

```
analysis/
└── temperature-monitoring/     # Temperature monitoring and performance analysis
    ├── (Future Python tools from test-stm32-adc-fixes branch)
    ├── Real-time data collection scripts
    ├── Performance comparison utilities
    └── Bug report data gathering tools
```

## Purpose

This directory contains **platform-agnostic analysis tools** that support:

- **Performance Evaluation**: Before/after comparisons when implementing firmware changes
- **Real-time Monitoring**: Live temperature and performance data collection
- **Bug Reporting**: Data gathering to support issue reports and feature requests
- **Upgrade Assessment**: Quantitative analysis to help users decide if upgrades are beneficial

## Tool Categories

### Temperature Monitoring
- **Location**: `temperature-monitoring/`
- **Purpose**: Monitor printer temperature behavior and performance
- **Integration**: Tools will be merged from `test-stm32-adc-fixes` branch
- **Language**: Python (cross-platform)

### Future Analysis Tools
Additional analysis utilities can be added as peer directories:
- `performance/` - General performance analysis
- `calibration/` - Calibration and tuning tools  
- `diagnostics/` - Hardware diagnostic utilities

## Usage Philosophy

These tools are designed to be:
- **User-accessible**: Any user can run analysis on any platform
- **Developer-friendly**: Support comparative evaluation during development
- **Data-driven**: Provide quantitative evidence for firmware improvements
- **Bug-support**: Generate data for issue reports and debugging

## Integration Plan

Tools from the `test-stm32-adc-fixes` branch will be integrated into `temperature-monitoring/` as Python scripts that can be run directly by users and developers on any platform.
