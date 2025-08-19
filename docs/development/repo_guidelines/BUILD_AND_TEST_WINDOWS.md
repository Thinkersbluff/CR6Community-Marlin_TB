
# Build & Test Documentation (Windows 10/11)

This document provides users with basic instructions and workflows for configuring this repository and building CR6Community Firmware on a Windows 10 or 11 platform.

> **Note:** If you use both Windows and Linux/macOS on the same computer to maintain this repository, see also the [DUAL_BOOT_GUIDELINES.md](../DUAL_BOOT_GUIDELINES.md).

## Table of Contents
- [Script Usage Guidelines](#script-usage-guidelines)
- [Containerized (Docker Desktop) Environment](#containerized-docker-desktop-environment)
- [Why Docker Desktop on Windows?](#why-docker-desktop-on-windows)
- [Build Methods](#build-methods)
- [Windows Build Scripts](#windows-build-scripts)
- [Permission Management](#permission-management)
- [Testing Infrastructure](#testing-infrastructure)
- [Configuration Management](#configuration-management)
- [Makefile Targets](#makefile-targets)
- [Continuous Integration](#continuous-integration)
- [Build Tools and Scripts](#build-tools-and-scripts)
- [Focused Development Workflow](#focused-development-workflow)
- [Troubleshooting](#troubleshooting)
- [Performance Notes](#performance-notes)
- [Security Guidelines](#security-guidelines)

---

## Script Usage Guidelines
← [ToC](#table-of-contents)

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

## Containerized (Docker Desktop) Environment
← [ToC](#table-of-contents)

### Install Docker Desktop
- Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Start Docker Desktop from the Start menu
- Use PowerShell or Command Prompt for Docker commands
- Ensure your project directory is within a shared drive (e.g., `C:\Users\YourName\CR6Community-Marlin_TB`)
- Use the configuration files in `tools/windows/build/docker/`

## Why Docker Desktop on Windows?
← [ToC](#table-of-contents)

While Podman is used for containerization on Linux and macOS, Docker Desktop is currently recommended for Windows because it is more mature and stable on this platform. Podman Desktop for Windows is still evolving and may not provide the same level of integration or reliability as Docker Desktop, especially for complex development workflows. If Podman Desktop becomes equally robust on Windows in the future, this recommendation may change.

## Build Methods
← [ToC](#table-of-contents)

### 1. Docker-based Building (Recommended)

#### Build Specific Configuration
```powershell
cd tools\windows\build\docker
# Build CR6 SE v4.5.3 configuration
docker compose run --rm marlin powershell -Command "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb; platformio run -e STM32F103RET6_creality"
```

#### Interactive Docker Session
```powershell
cd tools\windows\build\docker
# Get shell inside container
docker compose run --rm marlin powershell
# Inside container, you can run any build commands:
platformio run -e STM32F103RET6_creality
./buildroot/bin/build_example config/cr6-se-v4.5.2-mb
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
← [ToC](#table-of-contents)

PowerShell build scripts are provided in `tools/windows/build/`. Example usage:
```powershell
cd tools\windows\build
./Run-ExampleConfigBuilds.ps1 -ReleaseName "test-build"
```

## Permission Management
← [ToC](#table-of-contents)

- Ensure your repository is on a Docker Desktop shared drive (e.g., `C:\Users\YourName\CR6Community-Marlin_TB`).
- If you see "permission denied" errors, check Docker Desktop's "Resources > File Sharing" settings.
- Windows file permissions are less strict, but Docker Desktop may not be able to access files outside shared drives.
- If you see "file path too long" errors, enable long path support in Windows 10/11:
	- Open Group Policy Editor (`gpedit.msc`)
	- Navigate to Local Computer Policy > Computer Configuration > Administrative Templates > System > Filesystem
	- Enable "Enable Win32 long paths"

## Testing Infrastructure
← [ToC](#table-of-contents)

The repository supports automated testing across 50+ hardware platforms. See the main README for supported platforms and test execution instructions.

## Configuration Management
← [ToC](#table-of-contents)

Configuration directories are in `config/`. Each contains:
- `Configuration.h` - Main Marlin configuration
- `Configuration_adv.h` - Advanced settings
- `platformio-environment.txt` - PlatformIO environment specification

## Makefile Targets
← [ToC](#table-of-contents)

### Setup Targets
```powershell
# (If using Make for Windows, or adapt to PowerShell scripts as needed)
make setup-local-docker          # Build Docker development environment
```

### Testing Targets
```powershell
make tests-single-local          # Run single test locally
make tests-single-local-docker   # Run single test in Docker
make tests-all-local            # Run all tests locally  
make tests-all-local-docker     # Run all tests in Docker
make tests-single-ci            # Run single test (CI mode)
```

## Continuous Integration
← [ToC](#table-of-contents)

See `.github/workflows/test-builds.yml` for CI details. Matrix tests run on all supported platforms using Docker Desktop and PlatformIO.

## Build Tools and Scripts
← [ToC](#table-of-contents)

Core build tools are in `buildroot/bin/`:
```powershell
build_all_examples      # Build all configuration examples
build_example          # Build specific example
run_tests              # Core test runner script
use_example_configs    # Apply example configuration
restore_configs        # Restore original configuration
```

## Focused Development Workflow
← [ToC](#table-of-contents)

For CR6-specific development, use the supported configurations in `config/` and test using the provided PowerShell scripts and Docker commands.

## Troubleshooting
← [ToC](#table-of-contents)

- **Permission denied errors:** Ensure your repo is on a Docker Desktop shared drive and Docker Desktop has access.
- **File path too long:** Enable long path support in Windows.
- **PlatformIO not found:** Ensure Python and PlatformIO are installed and in your PATH.
- **Line ending issues:** Use a `.gitattributes` file to enforce consistent line endings.

## Performance Notes
← [ToC](#table-of-contents)
- Single platform test: ~2-3 minutes
- All platform tests: ~2-3 hours
- Docker container build: ~5-10 minutes (first time)
- RAM: ~2GB recommended for Docker builds
- Disk: ~5GB for complete environment
- Network: Initial setup downloads ~500MB

## Security Guidelines
← [ToC](#table-of-contents)

For Windows users, GPG key management is essential for secure Docker and package installations. Please review [SECURITY.md](SECURITY.md) for:
- How to verify and manage GPG keys
- Best practices for key safety
- Troubleshooting common GPG-related issues

Proper key management helps prevent build failures and protects your system from untrusted packages.
