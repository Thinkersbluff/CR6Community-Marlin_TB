# Build & Test Documentation (Linux)

This document provides comprehensive build and test instructions for Linux users, including Docker setup, build scripts, permission management, and troubleshooting.

## Table of Contents
- Quick Start
- Script Usage Guidelines
- Docker Environment
- Build Methods
- Linux Build Scripts
- Permission Management
- Testing Infrastructure
- Configuration Management
- Makefile Targets
- Continuous Integration
- Build Tools and Scripts
- Focused Development Workflow
- Troubleshooting
- Performance Notes
- Security Guidelines

> **Note:** If you use both Linux and Windows on the same computer, see [DUAL_BOOT_GUIDELINES.md](../DUAL_BOOT_GUIDELINES.md).

---

## Quick Start
- Docker and docker-compose installed

## Script Usage Guidelines

**Golden Rule: Always run scripts from their current location in the repository structure.**

All scripts in this repository are designed to work when you navigate to their directory and run them directly. This provides a consistent, predictable experience for all users.

### Examples:
```bash
# Build scripts - navigate to your platform's build directory
cd tools/linux/build
./build-configs.sh

# VS Code tools - navigate to your platform's vscode directory
cd tools/linux/vscode
```

## Docker Environment

### Install Docker and Docker Compose
```bash
sudo apt update && sudo apt install -y docker.io docker-compose
```

### Add your user to the docker group
```bash
sudo usermod -aG docker $USER
# Logout/login or run:
newgrp docker
```

### Use the configuration files in `tools/linux/build/docker/`.

## Build Methods

### 1. Docker-based Building (Recommended)

#### Build Specific Configuration
```bash
cd tools/linux/build/docker
# Build CR6 SE v4.5.3 configuration
# Example:
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"
```

#### Interactive Docker Session
```bash
cd tools/linux/build/docker
# Get shell inside container
docker-compose run --rm marlin bash
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

## Linux Build Scripts

The Linux build script (`tools/linux/build/build-configs.sh`) can build all or specific configuration examples. The script automatically detects the repository root and can be run from any directory within the repository.

**Basic usage (run from repository root):**
```bash
./tools/linux/build/build-configs.sh
```

**Basic usage (run from tools/linux/build directory):**
```bash
cd tools/linux/build && ./build-configs.sh
```

**Build with custom release name:**
```bash
./tools/linux/build/build-configs.sh v2.1.3.2
```

**Build single configuration:**
```bash
./tools/linux/build/build-configs.sh test-build cr6-se-v4.5.3-mb
```

**Dry run (test without building):**
```bash
./tools/linux/build/build-configs.sh test-build cr6-se-v4.5.3-mb true
```

**Custom touchscreen path:**
```bash
./tools/linux/build/build-configs.sh v2.1.3.2 "" "" ../path/to/CR-6-Touchscreen
```

**All parameters:**
```bash
./tools/linux/build/build-configs.sh release-name cr6-se-v4.5.3-mb false ../CR-6-Touchscreen
```

## Permission Management

Docker containers can create files owned by root, causing permission issues in development workflows. This section covers prevention and resolution strategies.

### Preventing Permission Issues

1. **Use Docker User Mapping** (Recommended):
   ```bash
   docker run --user $(id -u):$(id -g) ...
   ```
2. **Set Proper Umask**:
   ```bash
   umask 0022
   ```
3. **Use Development Containers** with proper user configuration in `.devcontainer/devcontainer.json`.

### Diagnosing Permission Problems

Common symptoms:
- PlatformIO/VS Code initialization failures
- "Permission denied" errors when building
- Cannot modify files in `.pio/build/` directory
- Files owned by root in development directories

Check file ownership:
```bash
ls -la .pio/build/
find . -user root -ls
```

### Fixing Permission Issues

#### Method 1: Fix Ownership (Quick Fix)
```bash
sudo chown -R $USER:$USER .
sudo chown -R $USER:$USER .pio/
```

#### Method 2: Clean and Rebuild
```bash
sudo rm -rf .pio/build/*
sudo chown -R $USER:$USER .pio/
pio system prune --force
```

#### Method 3: Reset PlatformIO Environment
```bash
sudo rm -rf ~/.platformio/
sudo rm -rf .pio/
pip install --user platformio
```

#### Method 4: Docker User Mapping (Permanent Solution)
- `tools/build/docker/.env` file with your UID/GID
- Modified `tools/build/docker/docker-compose.yml` with user mapping
- Updated `tools/build/docker/Dockerfile` that creates a matching user

If you encounter permission issues, first try Method 1 (fix ownership), then rebuild the Docker environment:
```bash
sudo chown -R $USER:$USER .
cd tools/build/docker
docker-compose down
docker-compose build --no-cache
```

## Testing Infrastructure

The repository supports automated testing across 50+ hardware platforms. See the main README for supported platforms and test execution instructions.

## Configuration Management

Configuration directories are in `config/`. Each contains:
- `Configuration.h` - Main Marlin configuration
- `Configuration_adv.h` - Advanced settings
- `platformio-environment.txt` - PlatformIO environment specification

## Makefile Targets

### Setup Targets
```bash
make setup-local-docker          # Build Docker development environment
```

### Testing Targets
```bash
make tests-single-local          # Run single test locally
make tests-single-local-docker   # Run single test in Docker
make tests-all-local            # Run all tests locally  
make tests-all-local-docker     # Run all tests in Docker
make tests-single-ci            # Run single test (CI mode)
```

## Continuous Integration

See `.github/workflows/test-builds.yml` for CI details. Matrix tests run on all supported platforms using Docker and PlatformIO.

## Build Tools and Scripts

Core build tools are in `buildroot/bin/`:
```bash
build_all_examples      # Build all configuration examples
build_example          # Build specific example
run_tests              # Core test runner script
use_example_configs    # Apply example configuration
restore_configs        # Restore original configuration
```

## Focused Development Workflow

For CR6-specific development, use the supported configurations in `config/` and test using the provided Makefile and Docker commands.

## Troubleshooting

### Common Issues
- Permission denied errors: Fix ownership, clean build artifacts, use Docker user mapping
- PlatformIO initialization failures: Remove root-owned files, reset PlatformIO
- Docker permission issues: Add user to docker group
- Linux keyring issues: Check and reset keyring service
- Build environment incompatibility: Ensure environment matches board configuration
- Memory issues: Increase container memory limits

## Performance Notes
- Single platform test: ~2-3 minutes
- All platform tests: ~2-3 hours
- Docker container build: ~5-10 minutes (first time)
- RAM: ~2GB recommended for Docker builds
- Disk: ~5GB for complete environment
- Network: Initial setup downloads ~500MB

## Security Guidelines

For Linux users, GPG key management is essential for secure Docker and package installations. Please review [SECURITY.md](SECURITY.md) for:
- How to verify and manage GPG keys
- Best practices for key safety
- Troubleshooting common GPG-related issues

Proper key management helps prevent build failures and protects your system from untrusted packages.
