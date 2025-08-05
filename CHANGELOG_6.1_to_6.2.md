# CR6 Community Firmware Changelog: v6.1 → v6.2

## Overview
CR6 Community Firmware v6.2 represents a significant upgrade from v6.1, bringing the codebase from **Marlin 2.0.8.1** to **Marlin 2.0.9.1** while maintaining full compatibility with CR6 SE and CR6 MAX printers.

## 🔧 Core Firmware Upgrade

### Marlin Base Version Upgrade: 2.0.8.1 → 2.0.9.1
This upgrade brings numerous upstream improvements, bug fixes, and new features from the Marlin development team.

## 🎯 CR6-Specific Enhancements

### Build System & Tooling
- **✨ NEW: Linux Build Script** - Added `build-configs.sh` as native Linux equivalent to PowerShell scripts
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
