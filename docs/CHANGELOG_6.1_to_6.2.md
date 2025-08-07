# CR6 Community Firmware Changelog: v6.1 → v6.2

## Overview
CR6 Community Firmware v6.2 represents a significant upgrade from v6.1, bringing the codebase from **Marlin 2.0.8.1** to **Marlin 2.0.9.1** while maintaining full compatibility with CR6 SE and CR6 MAX printers.

## 🔧 Core Firmware Upgrade

### Marlin Base Version Upgrade: 2.0.8.1 → 2.0.9.1
This upgrade brings numerous upstream improvements, bug fixes, and new features from the Marlin development team.

## 🎯 CR6-Specific Enhancements

### Build System & Tooling
- **✨ NEW: Linux Build Script** - Added `tools/build/build-configs.sh` as native Linux equivalent to PowerShell scripts
- **📚 Enhanced Documentation** - Comprehensive `BUILD_AND_TEST.md` covering Docker environment and build tools
- **🐳 Docker Environment Improvements** - Better permission management and troubleshooting guides
- **🔧 BTT SKR CR6 Support Fixed** - Resolved linking errors, added proper library dependencies

### Configuration Management
- **📦 Release Packaging Enhanced** - Improved ZIP structure with proper Display Firmware handling
- **🚫 No-Autobuild Support** - Added `no-autobuild.txt` flag for excluding configs from batch builds
- **📱 No-Touchscreen Support** - Added `no-touchscreen.txt` handling for BTT TFT configurations
- **🔄 Environment Switching** - Improved platform environment switching during builds

### Hardware Compatibility
- **📊 ERA Board Support** - Clarified that v4.5.3 configurations also support v1.1.0.3 ERA boards
- **🔧 BTT SKR CR6 Fixes** - Resolved TMC stepper, LCD, and EEPROM linking issues
- **📺 Display Firmware** - Enhanced handling of DWIN_SET packaging and download links

## 🔨 Technical Improvements

### Build Infrastructure
- **🐳 Docker Permission Management** - Fixed ownership issues when running Docker commands
- **📦 Automated Release Packaging** - Enhanced ZIP creation with proper directory structure
- **🔍 SHA256 Checksums** - Added integrity verification for release packages
- **🔗 Repository Links** - Automatic inclusion of repository URLs in releases

### Platform Support
- **🎯 STM32F1 Environment** - Comprehensive source filter additions for BTT boards
- **📚 Library Dependencies** - Added U8glib-HAL@~0.5.0 and TMCStepper@0.7.1 support
- **⚡ Controller Fan M710** - Fixed missing source file inclusion

## 📊 Key Upstream Marlin Changes (2.0.8.1 → 2.0.9.1)

### 🆕 New Features
- **✨ Up to 6 Linear Axes Support** (#19112) - Enhanced multi-axis capability
- **✨ Redundant Part Cooling Fan** (#21888) - Backup cooling fan support
- **✨ Extruder with Dual Stepper Drivers** (#21403) - Advanced extruder configurations
- **✨ M256 LCD Brightness Control** (#22478) - Dynamic display brightness adjustment
- **✨ Laser Support for TFT GLCD** (#22391) - Laser engraving improvements
- **✨ BigTreeTech Octopus V1.1** (#22042) - New board support
- **✨ MKS Monster8 Board** (#22455) - Additional hardware support

### 🐛 Bug Fixes & Improvements
- **🐛 Fixed STM32 Delay Issues** (#22584) - Better timing accuracy
- **🐛 BLTouch Improvements** - Enhanced probe reliability
- **🐛 DGUS Display Fixes** (#22464) - Better touchscreen compatibility
- **🐛 CoreXY Multi-Axis Fixes** - Improved kinematics support
- **🐛 SKR Board Pin Fixes** - Better pin assignments
- **🐛 TMC Driver Enhancements** - Improved stepper motor control

### 🚸 User Experience
- **🚸 Better Error Messages** - More descriptive error reporting
- **🚸 Improved Settings Reports** - Cleaner configuration output
- **🚸 Enhanced Menu Navigation** - Better LCD menu experience
- **🚸 BLTouch Configuration** - Simplified setup process

## 🔧 Configuration Changes

### Updated Configurations
All example configurations have been updated to:
- Support Marlin 2.0.9.1 features
- Include proper platform environment specifications
- Work with enhanced build system
- Support new hardware variants

### New Build Flags
- Enhanced source filters for comprehensive feature support
- Improved library dependency management
- Better platform-specific optimizations

## 🚀 Installation & Upgrade Notes

### For Users Upgrading from v6.1
1. **Display Firmware** - No changes needed; v1.1.x display firmware still compatible
2. **Configuration** - Use appropriate config from `config/` directory
3. **Build Environment** - Use updated platformio-environment.txt values

### For New Users
1. Download appropriate configuration for your hardware
2. Use provided build tools (VSCode + PlatformIO or Docker environment)
3. Flash motherboard firmware first, then display firmware if needed

## 🔗 Resources

- **Repository**: https://github.com/Thinkersbluff/CR6Community-Marlin_TB
- **Build Documentation**: [BUILD_AND_TEST.md](BUILD_AND_TEST.md)
- **Discord Community**: https://discord.gg/RKrxYy3Q9N
- **Original Marlin**: https://github.com/MarlinFirmware/Marlin

## 👥 Credits

### CR6 Community Team
- Sebastiaan Dammann [@Sebazzz] - Netherlands
- Juan Rodriguez [@Nushio] - Mexico  
- Romain [@grobux] - France
- Nick Acker [@nickacker] - USA
- Thinkersbluff [@Thinkersbluff] - v6.2 maintenance and enhancements

### Special Thanks
- Marlin Development Team for upstream improvements
- CR6 Community for testing and feedback
- GitHub Copilot for development assistance

---

*This changelog covers the major changes between CR6 Community Firmware v6.1 (Marlin 2.0.8.1) and v6.2 (Marlin 2.0.9.1). For detailed commit history, see the repository's git log.*


## Official Marlin Release Notes
For a more detailed review, you can also check the official Marlin release notes:
These are the changelogs summarizing what happened to Marlin between release 2.0.8.1 and 2.0.9.1:  

[Marlin 2.0.8.2 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.8.2)  
[Marlin 2.0.8.3 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.8.3)  
[Marlin 2.0.8.4 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.8.4)  
[Marlin 2.0.9 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9)  
[Marlin 2.0.9.1 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.1)  

These release notes may describe bugs that were introduced or discovered during the above evolution and subsequently improved or fixed at a revision later than 2.0.9.1:  

[Marlin 2.0.9.2 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.2)  
[Marlin 2.0.9.3 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.3)  
[Marlin 2.0.9.4 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.4)  
[Marlin 2.0.9.5 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.5)  
[Marlin 2.0.9.6 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.6)  
[Marlin 2.0.9.7 Release Notes](https://github.com/MarlinFirmware/Marlin/releases/tag/2.0.9.7)  

## 🚨 Critical Issues Addressed After v6.2 (Marlin 2.0.9.1)

The following summarizes significant bugs, security issues, and critical fixes that were discovered and resolved in Marlin versions 2.0.9.2 through 2.0.9.7. **While v6.2 is based on Marlin 2.0.9.1, users should be aware of these issues that were subsequently identified and fixed:**

### 🔥 **Critical Safety & Security Issues**

#### Thermal Management & Safety
- **🚑️ Thermal Runaway Fixes** (2.0.9.3) - Fixed `AUTOTEMP` bug that could cause thermal runaway conditions
- **🐛 Heater Control Issues** (2.0.9.3) - Fixed `loud_kill` heater disable functionality
- **🐛 Temperature Sensor Issues** (2.0.9.3, 2.0.9.4) - Multiple MAX31865 PT100/PT1000 sensor fixes for accuracy
- **🩹 Temperature Monitoring** (2.0.9.4) - Fixed temperature variance monitoring and redundant sensor issues

#### Hardware Control & Safety
- **🚑️ Power Management** (2.0.9.3) - Fixed conditional `M81` suicide command issues
- **🐛 Stepper Motor Control** (2.0.9.2) - Fixed multi-endstop stepping and sensorless homing accuracy
- **🐛 Probe Safety** (2.0.9.2, 2.0.9.3) - Fixed probe deployment issues and BLTouch improvements
- **🩹 Emergency Situations** (2.0.9.3) - Fixed AVR watchdog pile-up that could cause system lockups

### ⚠️ **High-Impact Functional Issues**

#### Motion Control & Accuracy
- **🐛 G2/G3 Arc Motion** (2.0.9.2) - Fixed angular motion calculation errors in arc movements
- **🐛 CoreXY Multi-Axis** (2.0.9.2) - Fixed CoreXY plus extra axes motion control
- **🐛 Leveling Systems** (2.0.9.2, 2.0.9.3) - Multiple bed leveling fixes (UBL, ABL, Delta calibration)
- **🐛 IDEX Issues** (2.0.9.3) - Fixed dual extruder positioning and duplication mode

#### Communication & Control
- **🚑️ Serial Communication** (2.0.9.3) - Fixed `M105` regression and serial buffer issues
- **🐛 SD Card Problems** (2.0.9.3, 2.0.9.5) - Fixed SD mount bugs and file handling issues
- **🐛 Host Communication** (2.0.9.3, 2.0.9.4) - Fixed emergency parser and host status notifications

#### Display & User Interface
- **🐛 LCD/TFT Issues** (2.0.9.2, 2.0.9.3) - Multiple display controller fixes and touch interface problems
- **🚑️ Touch Screen Freezes** (2.0.9.5) - Fixed BIQU BX touch freeze issues
- **🐛 E3V2 Display Problems** (2.0.9.3, 2.0.9.4) - Multiple Ender-3 V2 display and UI fixes

### 📊 **Board-Specific Critical Fixes**

#### STM32 Platform Issues
- **🐛 STM32 Timing** (2.0.9.2) - Fixed STM32 delay issues and double reset problems
- **🐛 FSMC TFT Initialization** (2.0.9.2) - Fixed TFT display initialization failures
- **🐛 STM32 PWM Issues** (2.0.9.3) - Fixed PWM control and fast PWM implementation
- **🐛 SDIO Problems** (2.0.9.5) - Fixed SDIO SD card interface for STM32 boards

#### Specific Board Fixes
- **🐛 SKR Mini E3 V2** (2.0.9.3) - Fixed I2C-based EEPROM issues
- **🐛 BTT Boards** (2.0.9.2, 2.0.9.3) - Multiple BigTreeTech board pin and configuration fixes
- **🐛 MKS Boards** (2.0.9.2, 2.0.9.3) - Fixed Robin Nano and other MKS board issues
- **🐛 Chitu F103** (2.0.9.6, 2.0.9.7) - Fixed build issues for Tronxy with Chitu F103

### 🔧 **Build & Compatibility Issues**

#### Compilation Problems
- **🐛 Arduino IDE** (2.0.9.3) - Fixed Arduino IDE compilation errors
- **🐛 PlatformIO Updates** (2.0.9.6) - Support for latest PlatformIO versions
- **🔨 Build Failures** (2.0.9.2-2.0.9.5) - Multiple platform-specific build fixes

#### Feature Interactions
- **🐛 Linear Advance** (2.0.9.3) - Fixed Linear Advance with low E-jerk settings
- **🐛 TMC Driver Issues** (2.0.9.2-2.0.9.4) - Multiple TMC stepper driver fixes and improvements
- **🐛 Mixing Extruder** (2.0.9.2) - Fixed mixing extruder code errors

### 📈 **Impact Assessment for CR6 Community Firmware v6.2 Users**

**Risk Level: MODERATE** - While v6.2 is stable for most users, the above issues represent potential problems that could affect:

1. **Print Quality** - Arc motion and leveling issues could affect print accuracy
2. **Hardware Safety** - Thermal management and power control issues could pose safety risks
3. **Reliability** - Communication and display issues could cause print failures
4. **Board Compatibility** - STM32 and specific board issues could affect certain hardware variants

**Recommendation**: Users experiencing any issues similar to those described above should consider:
- Monitoring for similar symptoms in their setups
- Reviewing the specific fixes in later Marlin versions
- Considering an upgrade path to incorporate critical safety fixes if problems are encountered

*Note: This analysis is based on official Marlin release notes and identifies issues that were present in 2.0.9.1 but subsequently discovered and fixed. The CR6 Community Firmware v6.2 may not be affected by all these issues due to different configuration and code paths.*
