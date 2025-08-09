# Build & Test Documentation (Windows)

This document provides comprehensive build and test instructions for Windows users, including Docker Desktop setup, PowerShell scripts, permission management, and troubleshooting.

## Table of Contents

> **Note:** If you use both Windows and Linux on the same computer, see [DUAL_BOOT_GUIDELINES.md](../DUAL_BOOT_GUIDELINES.md).


## Quick Start
 - Install Docker Desktop and start it before running any Docker commands
 - Use PowerShell or Command Prompt
 - Make sure your repository is in a shared drive (e.g., C:\Users\YourName\CR6Community-Marlin_TB)

## Script Usage Guidelines

**Golden Rule: Always run scripts from their current location in the repository structure.**

All scripts in this repository are designed to work when you navigate to their directory and run them directly. This provides a consistent, predictable experience for all users.

### Examples:
```powershell
# Build scripts - navigate to your platform's build directory
cd tools\windows\build
./Run-ExampleConfigBuilds.ps1 -ReleaseName "test-build"

# VS Code tools - navigate to your platform's vscode directory
cd tools\windows\vscode
```

## Docker Environment

### Install Docker Desktop
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Start Docker Desktop from the Start menu
- Use PowerShell or Command Prompt for Docker commands
- Ensure your project directory is within a shared drive (e.g., C:\Users\YourName\CR6Community-Marlin_TB)
- Use the configuration files in `tools/windows/build/docker/`
- If you encounter permission errors, comment out the `user:` line in `docker-compose.yml`

## Build Methods

### 1. Docker-based Building (Recommended)

#### Build Specific Configuration
```powershell
cd tools\windows\build\docker
# Build CR6 SE v4.5.3 configuration
...Windows-specific build example...
```

#### Interactive Docker Session
```powershell
cd tools\windows\build\docker
# Get shell inside container
...Windows-specific shell example...
```

### 2. Local PlatformIO Building

#### Requirements
- Visual Studio Code with PlatformIO extension
- Python 3.7+
- PlatformIO Core

#### Process
1. Copy configuration files from `config/[your-config]/` to `Marlin/`
2. Update `platformio.ini` `default_envs` to match `platformio-environment.txt`
3. Build using PlatformIO IDE or command line

## Windows Build Scripts
...Windows PowerShell build scripts and usage...

## Permission Management
...Windows-specific permission management and troubleshooting...

## Testing Infrastructure
...Windows-specific testing infrastructure...

## Configuration Management
...Windows configuration management...

## Makefile Targets
...Windows makefile targets and usage...

## Continuous Integration
...Windows CI instructions...

## Build Tools and Scripts
...Windows build tools and scripts...

## Focused Development Workflow
...Windows-focused workflow...

## Troubleshooting
...Windows troubleshooting...

## Performance Notes
...Windows performance notes...

---

*For Linux instructions, see [BUILD_AND_TEST_LINUX.md](BUILD_AND_TEST_LINUX.md).*

---

*For Linux instructions, see [BUILD_AND_TEST_LINUX.md](BUILD_AND_TEST_LINUX.md).*
