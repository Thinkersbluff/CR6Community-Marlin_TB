# Build & Test Documentation

This document describes the comprehensive build and test infrastructure available in this repository, including Docker environment setup, automated testing, and various build tools.

## Table of Contents

- [Quick Start](#quick-start)
- [Script Usage Guidelines](#script-usage-guidelines)
- [Docker Environment](#docker-environment)
- [Build Methods](#build-methods)
- [Linux Build Scripts](#linux-build-scripts)
- [Permission Management](#permission-management)
- [Testing Infrastructure](#testing-infrastructure)
- [Configuration Management](#configuration-management)
- [Makefile Targets](#makefile-targets)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Docker and docker-compose installed

## Script Usage Guidelines

**🎯 Golden Rule: Always run scripts from their current location in the repository structure.**

All scripts in this repository are designed to work when you navigate to their directory and run them directly. This provides a consistent, predictable experience for all users.

### Examples:
```bash
# Build scripts - navigate to your platform's build directory
# Linux/macOS users:
cd tools/linux/build
./build-configs.sh

# Windows users:
cd tools/windows/build
./Run-ExampleConfigBuilds.ps1 -ReleaseName "test-build"

# VS Code tools - navigate to your platform's vscode directory  
# Linux/macOS users:
cd tools/linux/vscode
# Windows users:
cd tools/windows/vscode
```

### Why This Approach?
- **🆕 Beginner-friendly**: Only one rule to remember
- **🔍 Discoverable**: Find a script, navigate to it, run it
- **📁 Self-documenting**: Location tells you how to use it
- **🔄 Consistent**: Every script works the same way

### Technical Details:
Our scripts use automatic repository root detection, so they work correctly regardless of where you run them from. However, following the "run from script location" pattern creates consistency and helps build good habits for repository navigation.

### Docker Usage (Linux & Windows):

#### Linux
```bash
# Docker files are located in tools/linux/build/docker/
cd tools/linux/build/docker

# Build the container
docker-compose build

# Run a build
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"

# Get an interactive shell
docker-compose run --rm marlin bash
```

#### Windows
```powershell
# Docker files are located in tools/windows/build/docker/
cd tools\windows\build\docker

# Build the container
docker-compose build

# Run a build
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"

# Get an interactive shell
docker-compose run --rm marlin bash
```

> **Windows Notes:**
> - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it before running these commands.
> - Use PowerShell or Command Prompt.
> - Make sure your repository is in a shared drive (e.g., C:\Users\YourName\CR6Community-Marlin_TB).
> - Use the configuration files in `tools/windows/build/docker/`.
> - If you see permission errors, comment out the `user:` line in `docker-compose.yml`.

#### Basic Docker Build (Both Platforms)
```bash
# Setup Docker environment (one-time)
make setup-local-docker

# Test a specific platform
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality

# Run all tests
make tests-all-local-docker
```

## Docker Environment
[note]
## Docker Usage: Linux and Windows

### Linux
- Install Docker and Docker Compose using your package manager:
    ```bash
    sudo apt update && sudo apt install -y docker.io docker-compose
    ```
- Add your user to the docker group:
    ```bash
    sudo usermod -aG docker $USER
    # Logout/login or run:
    newgrp docker
    ```
- Use the configuration files in `tools/linux/build/docker/`.

### Windows
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Why Docker Desktop? Windows does not natively support the Linux container runtime. Docker Desktop provides a VM-based backend and integrates with Windows networking and filesystems.
- After installation:
    - Start Docker Desktop from the Start menu.
    - Use PowerShell or Command Prompt for Docker commands.
    - Ensure your project directory is within a shared drive (e.g., C:\Users\YourName\CR6Community-Marlin_TB).
- Use the configuration files in `tools/windows/build/docker/`.
- If you encounter permission errors, comment out the `user:` line in `docker-compose.yml`.

### Platform-Specific Configuration Files
- If Windows users need to comment out or modify lines (e.g., `user: "${UID:-1000}:${GID:-1000}"` in `docker-compose.yml`), a Windows-friendly version is provided in `tools/windows/build/docker/`.
- The Linux version is in `tools/linux/build/docker/`.
- Documented here and in the README:
    - "Windows users should use the configuration files in `tools/windows/build/docker/`."
    - "Linux users should use the configuration files in `tools/linux/build/docker/`."

### Example Docker Compose Usage
```bash
# Linux
cd tools/linux/build/docker
docker-compose build
docker-compose run --rm marlin bash

# Windows
cd tools/windows/build/docker
docker-compose build
docker-compose run --rm marlin bash
```

### Why Different Files?
- Linux supports user mapping for file permissions; Windows does not.
- Docker Desktop is required on Windows for container support.
- Providing platform-specific configuration files ensures a smooth experience for all users.

### Overview

The repository includes a complete Docker-based development environment for both Linux and Windows:
- Consistent build environment across different systems
- All required dependencies (PlatformIO, Python, build tools)
- Isolated testing environment
- Automated CI/CD capabilities

### Docker Setup

#### Initial Setup

**Linux:**
```bash
# Install Docker (Ubuntu/Debian)
sudo apt update && sudo apt install -y docker.io docker-compose

# Add user to docker group (requires logout/login to take effect)
sudo usermod -aG docker $USER
# Logout/login or run:
newgrp docker

# Start Docker service
sudo systemctl start docker && sudo systemctl enable docker
```

**Windows:**
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it before running any Docker commands.
- Use PowerShell or Command Prompt.
- Ensure your repository is in a shared drive (e.g., `C:\Users\YourName\CR6Community-Marlin_TB`).

#### GPG Key Management

The development environment requires GPG keys for package verification (Linux only):
- **Docker keys**: Automatically installed with Docker packages
- **Microsoft keys**: Required for VS Code repository (if using VS Code)

```bash
# Check installed keys
ls -la /etc/apt/trusted.gpg.d/

# If Microsoft key is missing (VS Code repository issues):
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
rm packages.microsoft.gpg
```

#### Build Docker Container

```bash
# Build the development container (from repository root, both platforms)
make setup-local-docker

# Or manually from your platform's Docker directory:
# Linux:
cd tools/linux/build/docker
docker-compose build
# Windows:
cd tools\windows\build\docker
docker-compose build
```

### Docker Files Structure

#### Docker Files Structure
- **Linux:**
    - `tools/linux/build/docker/docker-compose.yml`: Main Docker Compose configuration
    - `tools/linux/build/docker/Dockerfile`: Container definition with PlatformIO and dependencies
    - `tools/linux/build/docker/get-docker.sh`: Docker installation helper script
- **Windows:**
    - `tools/windows/build/docker/docker-compose.yml`: Windows-friendly Docker Compose configuration
    - `tools/windows/build/docker/Dockerfile`: Container definition for Windows Docker Desktop
    - `tools/windows/build/docker/get-docker.sh`: Docker Desktop helper script
- `platformio-cache` volume: Persists PlatformIO libraries between runs


**Note:**
- Makefile commands (`make setup-local-docker`, `make tests-*`) work from the repository root for both platforms.
- Direct `docker-compose` commands must be run from your platform's Docker directory (`tools/linux/build/docker/` for Linux, `tools/windows/build/docker/` for Windows).
- **Windows users:** If you see permission errors, comment out the `user:` line in `docker-compose.yml`.

### Dual-Boot System Guidelines

If you use both Linux and Windows on the same computer (dual-boot):

- **Keep separate clones:**
    - Clone the repository to a Windows-accessible drive for Windows development.
    - Clone the repository to a Linux partition for Linux development.
    - Do not use the same physical folder or partition for both OSes.

- **Avoid shared working directories:**
    - Do not point both OSes to the same folder, even if it is on a shared or network drive.
    - This prevents file permission conflicts and Docker-related issues.

- **Sync changes via Git:**
    - Make changes on one OS, push to GitHub, and pull those changes into your other OS.
    - This keeps your work in sync and avoids cross-platform permission problems.

- **Docker builds:**
    - Run Docker builds only in the environment matching your clone (Linux or Windows).
    - Each OS will handle file permissions and user mapping correctly in its own clone.

**Summary:**
Always use separate clones for Linux and Windows, and sync via Git. Never share the same working directory between OSes for Docker-based builds.

## Build Methods

### 1. Docker-based Building (Recommended)

#### Build Specific Configuration
```bash
# Navigate to Docker directory
cd tools/linux/build/docker

# Build CR6 SE v4.5.3 configuration
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"

# Build BTT SKR CR6 configuration
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/btt-skr-cr6-with-btt-tft && platformio run -e STM32F103RE_btt_USB"
```

#### Interactive Docker Session
```bash
# Navigate to Docker directory
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

For users running on Linux systems, we provide native shell scripts that offer equivalent functionality to the PowerShell scripts used in the Windows development environment.

### tools/linux/build/build-configs.sh

The Linux build script (`tools/linux/build/build-configs.sh`) is equivalent to the PowerShell `Run-ExampleConfigBuilds.ps1` script and can build all or specific configuration examples. The script automatically detects the repository root and can be run from any directory within the repository.

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

#### Parameters and Options

The script accepts up to four positional parameters:

1. **Release Name** (optional, default: "test-build")
   - Sets the prefix for output ZIP files and directories
   - Used for version tagging in release builds
   - Example: `v2.1.3.2`, `nightly-build`, `feature-test`

2. **Single Build** (optional)
   - Specify a single configuration to build instead of all configurations
   - Must match a directory name in the `config/` folder
   - Example: `cr6-se-v4.5.3-mb`, `btt-skr-cr6-with-btt-tft`

3. **Dry Run** (optional, default: false)
   - Set to `true` to test the script without actually building firmware
   - Useful for validating configurations and checking script logic
   - Shows what would be built without consuming time/resources

4. **Touchscreen Repository Path** (optional, default: "../CR-6-Touchscreen")
   - Path to the CR-6 touchscreen firmware repository
   - Only needed if your touchscreen repo is in a different location than the default
   - The script looks for `DWIN_SET` folder at `[this-path]/src/DWIN/DWIN_SET`
   - Set to non-existent path to deliberately skip touchscreen firmware

#### Advanced Usage Examples

```bash
# Release build for all configurations
./tools/linux/build/build-configs.sh v2.1.3.2

# Test specific configuration without building
./tools/linux/build/build-configs.sh test-build cr6-max-stock-mb true

# Build with custom touchscreen repository path (only if not at default location)
./tools/linux/build/build-configs.sh v2.1.3.2 "" "" /home/stephen/CR-6-Touchscreen

# Build only BTT configurations (using pattern matching)
for config in $(ls config/ | grep btt); do
    ./tools/linux/build/build-configs.sh release-candidate "$config"
done

# Quick test build of modified configuration
./tools/linux/build/build-configs.sh debug-test cr6-se-v4.5.3-mb

# Skip touchscreen firmware entirely (disable touchscreen)
./tools/linux/build/build-configs.sh v2.1.3.2 "" "" /nonexistent/path
```

#### Touchscreen Firmware Integration

The script automatically includes CR-6 touchscreen firmware when:

1. **DWIN_SET folder exists** at `[touchscreen-repo]/src/DWIN/DWIN_SET`
2. **Configuration supports touchscreen** (no `no-touchscreen.txt` file present)

**Touchscreen Repository Setup:**
```bash
# Clone the touchscreen repository to the default location
git clone https://github.com/CR6Community/CR-6-touchscreen ../CR-6-Touchscreen

# Verify DWIN_SET folder exists at expected location
ls ../CR-6-Touchscreen/src/DWIN/DWIN_SET/

# Build will automatically find and package touchscreen firmware
./tools/linux/build/build-configs.sh v2.1.3.2

# If your touchscreen repo is elsewhere, specify the path:
./tools/linux/build/build-configs.sh v2.1.3.2 "" "" /home/stephen/CR-6-Touchscreen
```

**How It Works:**
- **DWIN_SET found**: Creates `DWIN_SET.zip` containing all touchscreen firmware files
- **DWIN_SET missing**: Creates `CR-6-Touchscreen-Download.url` shortcut to GitHub repository
- **No touchscreen configs**: Skips touchscreen processing for BTT TFT configurations

**Configurations without Touchscreen:**
Some configurations exclude touchscreen firmware by including a `no-touchscreen.txt` file:
- BTT SKR CR6 configurations (use BTT TFT instead of CR-6 touchscreen)
- Custom configurations with different display solutions

When a configuration contains `no-touchscreen.txt`, the build script will:
- Skip touchscreen firmware packaging entirely
- Copy the `no-touchscreen.txt` file to the `Display Firmware/` folder in the release ZIP
- This informs end users why no touchscreen firmware is included with their build

#### Script Features

The script includes:
- **Docker-based building** using the project's docker-compose configuration
- **Automatic ZIP packaging** of firmware files with organized directory structure
- **SHA256 checksum generation** for release verification and integrity checking
- **Display firmware packaging** automatically packages DWIN_SET folder or creates download link
- **Repository URL inclusion** adds link to source repository in each build package
- **Configuration validation** ensuring required files exist before building (skips incomplete configurations)
- **Platform environment detection** from `platformio-environment.txt` files
- **No-autobuild support** respects `no-autobuild.txt` flags in configurations
- **No-touchscreen support** respects `no-touchscreen.txt` flags for BTT TFT configurations
- **Proper error handling** with detailed progress reporting and failure detection
- **Git state restoration** automatically restores original configuration files
- **Timestamped outputs** for build tracking and organization

#### Output Structure

Built packages are organized as follows:
```
.pio/build-output/
├── [release-name]-[config-name]-[timestamp].zip
│   ├── [release-name]-[config-name]-[timestamp]/
│   │   ├── Firmware/
│   │   │   ├── Motherboard firmware/
│   │   │   │   └── firmware.bin
│   │   │   └── Display Firmware/
│   │   │       ├── DWIN_SET.zip  (if DWIN_SET folder found and touchscreen supported)
│   │   │       ├── CR-6-Touchscreen-Download.url  (if DWIN_SET not found and touchscreen supported)
│   │   │       └── no-touchscreen.txt  (if configuration excludes touchscreen)
│   │   ├── configs/
│   │   │   ├── Configuration.h
│   │   │   └── Configuration_adv.h
│   │   └── description.txt
│   └── CR6Community-Marlin-Repository.url
└── checksums.txt
```

#### Configuration Requirements

Each configuration directory must contain:
- `Configuration.h` - Main Marlin configuration
- `Configuration_adv.h` - Advanced settings  
- `platformio-environment.txt` - Target platform specification

Optional files:
- `description.txt` - Custom description (auto-generated if missing)
- `no-autobuild.txt` - Skip in batch builds (still builds if specifically requested)
- `no-touchscreen.txt` - Exclude touchscreen firmware from this configuration

#### No-Autobuild Flag

To prevent a configuration from being built during batch builds (when running `./tools/build/build-configs.sh` without specifying a single configuration), create a `no-autobuild.txt` file in the configuration directory:

```bash
# Create the file with explanation text
echo "Community Firmware releases are not automaticallly building this folder" > config/my-config/no-autobuild.txt
```

The file should contain a brief explanation of why the configuration is excluded from automatic builds. Common reasons include:
- Experimental or untested configurations
- Specialized hardware variants with limited user base  
- Development/debugging configurations
- Configurations requiring manual verification before release

**Important**: The `no-autobuild.txt` flag only affects batch builds. You can still build the configuration explicitly:
```bash
# This will build even with no-autobuild.txt present
./tools/build/build-configs.sh release-name my-excluded-config
```

### run-powershell.sh

For cases where PowerShell scripts must be executed on Linux systems:

```bash
# Execute PowerShell script through Docker
./tools/linux/build/run-powershell.sh tools/windows/build/Run-ExampleConfigBuilds.ps1 -ReleaseName cr6-se-v4.5.3-mb

# Run with additional parameters
./tools/linux/build/run-powershell.sh tools/windows/build/Generate-ConfigExample.ps1 -ConfigName cr6-se-v4.5.3-mb
```

This wrapper provides:
- PowerShell Core execution via Docker container
- Proper volume mounting for script access
- Execution policy bypass for script execution
- Parameter forwarding to PowerShell scripts

## Permission Management

Docker containers can create files owned by root, causing permission issues in development workflows. This section covers prevention and resolution strategies.

### Preventing Permission Issues

1. **Use Docker User Mapping** (Recommended):
   ```bash
   # Add to docker-compose.yml or run with user mapping
   docker run --user $(id -u):$(id -g) ...
   ```

2. **Set Proper Umask**:
   ```bash
   # Add to ~/.bashrc or session
   umask 0022
   ```

3. **Use Development Containers** with proper user configuration in `.devcontainer/devcontainer.json`:
   ```json
   {
     "remoteUser": "vscode",
     "containerUser": "vscode"
   }
   ```

### Diagnosing Permission Problems

Common symptoms:
- PlatformIO/VS Code initialization failures
- "Permission denied" errors when building
- Cannot modify files in `.pio/build/` directory
- Files owned by root in development directories

Check file ownership:
```bash
# Check ownership of build directories
ls -la .pio/build/

# Check for root-owned files in workspace
find . -user root -ls
```

### Fixing Permission Issues

#### Method 1: Fix Ownership (Quick Fix)
```bash
# Fix ownership of entire repository (recommended first step)
sudo chown -R $USER:$USER .

# Specific fix for PlatformIO directories only
sudo chown -R $USER:$USER .pio/
```

#### Method 2: Clean and Rebuild
```bash
# Remove all build artifacts
sudo rm -rf .pio/build/*

# Fix ownership of remaining directories
sudo chown -R $USER:$USER .pio/

# Clean PlatformIO cache
pio system prune --force
```

#### Method 3: Reset PlatformIO Environment
```bash
# Complete PlatformIO reset
sudo rm -rf ~/.platformio/
sudo rm -rf .pio/

# Reinstall PlatformIO
pip install --user platformio
```

#### Method 4: Docker User Mapping (Permanent Solution)
The repository is configured to prevent permission issues by running Docker containers with your user ID instead of root. This is handled automatically via:

- `tools/build/docker/.env` file with your UID/GID
- Modified `tools/build/docker/docker-compose.yml` with user mapping
- Updated `tools/build/docker/Dockerfile` that creates a matching user

If you encounter permission issues, first try Method 1 (fix ownership), then rebuild the Docker environment:

```bash
# Fix ownership and rebuild Docker environment
sudo chown -R $USER:$USER .
cd tools/build/docker
docker-compose down
docker-compose build --no-cache
```

### Docker-Specific Solutions

The repository is configured to prevent permission issues by running Docker containers with your user ID. This is handled automatically via:

- **User mapping**: `tools/build/docker/docker-compose.yml` includes `user: "${UID:-1000}:${GID:-1000}"`
- **Environment variables**: `tools/build/docker/.env` file contains your user/group IDs  
- **Container user**: `tools/build/docker/Dockerfile` creates a `user` account that matches your host user

For manual Docker builds, ensure proper user mapping:

```bash
# Build with user mapping (if not using docker-compose)
docker run --user $(id -u):$(id -g) marlin-dev

# The tools/build/docker/docker-compose.yml already handles this automatically:
services:
  marlin:
    user: "${UID:-1000}:${GID:-1000}"
```

If you need to rebuild the Docker environment after permission issues:

```bash
# Complete Docker environment reset
cd tools/linux/build/docker
docker-compose down
docker volume rm cr6community-marlin_tb_platformio-cache
docker-compose build --no-cache
```

### Best Practices

1. **Always check permissions** before starting development
2. **Use consistent user mapping** in Docker configurations
3. **Regularly clean build artifacts** to prevent accumulation
4. **Set up proper umask** in development environment
5. **Document permission requirements** for team members

### Automated Permission Checks

Add to your development workflow:

```bash
#!/bin/bash
# check-permissions.sh - Verify development environment permissions

echo "Checking PlatformIO permissions..."
if [ -d ".pio" ]; then
    ROOT_FILES=$(find .pio -user root 2>/dev/null | wc -l)
    if [ $ROOT_FILES -gt 0 ]; then
        echo "WARNING: Found $ROOT_FILES root-owned files in .pio/"
        echo "Run: sudo chown -R \$USER:\$USER .pio/"
    else
        echo "✓ PlatformIO permissions OK"
    fi
else
    echo "✓ No .pio directory found"
fi
```

## Testing Infrastructure

### Test Platforms
The repository supports automated testing across 50+ hardware platforms:

**Arduino Platforms:**
- `mega2560`, `mega1280`, `rambo`
- `sanguino1284p`, `sanguino644p`

**STM32 Platforms:**
- `STM32F103RET6_creality` (Creality v4.5.2/v4.5.3 boards)
- `STM32F103RE_btt_USB` (BTT SKR CR6 board)
- `STM32F103RC_btt`, `STM32F103RE_btt`
- Many other STM32 variants

**Other Platforms:**
- `esp32`, `teensy31`, `teensy35`, `teensy41`
- `DUE`, `DUE_archim`
- `linux_native` (for simulation)

### Available Test Configurations
Located in `buildroot/tests/[platform]`, each containing:
- Platform-specific test scripts
- Configuration modifications
- Build validation steps

### Test Execution

#### Single Platform Test
```bash
# Test specific platform
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality

# With verbose output
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality VERBOSE_PLATFORMIO=1

# Test subset matching pattern
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality ONLY_TEST="CrealityUI"
```

#### All Platforms Test
```bash
# Run all available tests (takes significant time)
make tests-all-local-docker

# Run all tests locally (without Docker)
make tests-all-local
```

#### Get Available Test Targets
```bash
# List all available test platforms
python3 get_test_targets.py
```

## Configuration Management

### Configuration Structure
```
config/
├── cr6-se-v4.5.2-mb/           # CR6 SE with v4.5.2 motherboard
├── cr6-se-v4.5.3-mb/           # CR6 SE with v4.5.3 motherboard
├── cr6-max-stock-mb/           # CR6 Max with stock motherboard
├── btt-skr-cr6-with-btt-tft/   # BTT SKR CR6 + BTT TFT
├── btt-skr-cr6-with-stock-creality-tft/  # BTT SKR CR6 + Stock TFT
└── [other configurations...]
```

Each configuration directory contains:
- `Configuration.h` - Main Marlin configuration
- `Configuration_adv.h` - Advanced settings
- `platformio-environment.txt` - PlatformIO environment specification

### Hardware-Specific Environments

#### Creality Motherboards (v4.5.2, v4.5.3 and v1.1.0.3 ERA)
- **Environment**: `STM32F103RET6_creality`
- **Boards**: `BOARD_CREALITY_V452`, `BOARD_CREALITY_V453`
- **Compatible with**: CR6 SE, CR6 Max

#### BTT SKR CR6 Board
- **Environment**: `STM32F103RE_btt_USB`
- **Board**: `BOARD_BTT_SKR_CR6`
- **Compatible with**: CR6 SE, CR6 Max (with BTT upgrade)

### Using Configurations

#### Apply Configuration
```bash
# Copy configuration files
cp config/cr6-se-v4.5.3-mb/* Marlin/

# Update platformio.ini default_envs
# Set to content of platformio-environment.txt
```

#### Generate New Configuration (Maintainers)
```bash
# Requires PowerShell Core
pwsh scripts/Generate-ConfigExample.ps1 -Name MyNewConfig
```

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

### Environment Variables
```bash
TEST_TARGET=platform            # Specify test platform
ONLY_TEST="pattern"            # Filter tests by pattern or index
VERBOSE_PLATFORMIO=1           # Enable verbose PlatformIO output
GIT_RESET_HARD=true           # Reset git state after test (CI)
```

### Examples
```bash
# Test Creality board
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality

# Test BTT board with verbose output
make tests-single-local-docker TEST_TARGET=STM32F103RE_btt_USB VERBOSE_PLATFORMIO=1

# Test all platforms (long running)
make tests-all-local-docker
```

## Continuous Integration

### GitHub Actions Workflow
Located in `.github/workflows/test-builds.yml`:

- **Triggers**: Pull requests and pushes to `extui` branch
- **Matrix Strategy**: Tests across 50+ hardware platforms
- **Caching**: PlatformIO dependencies cached for speed
- **Python 3.7**: Consistent with production environment

### CI Test Process
1. **Checkout code**
2. **Setup Python 3.7**
3. **Install PlatformIO**
4. **Cache dependencies**
5. **Run platform-specific tests**
6. **Report results**

### Local CI Simulation
```bash
# Run same test as CI
make tests-single-ci TEST_TARGET=STM32F103RET6_creality
```

## Build Tools and Scripts

### Core Build Tools
Located in `buildroot/bin/`:

```bash
build_all_examples      # Build all configuration examples
build_example          # Build specific example
run_tests              # Core test runner script
use_example_configs    # Apply example configuration
restore_configs        # Restore original configuration
opt_enable/opt_disable # Enable/disable configuration options
opt_set               # Set configuration values
```

### Helper Scripts
```bash
# Build specific example
./buildroot/bin/build_example config/cr6-se-v4.5.3-mb

# Apply configuration
./buildroot/bin/use_example_configs config/btt-skr-cr6-with-btt-tft

# Restore original config
./buildroot/bin/restore_configs
```

### PowerShell Scripts (Maintainers on Windows system)
Located in `tools/windows/build/`:
- `Generate-ConfigExample.ps1` - Create new configuration
- `Update-ConfigExamples.ps1` - Update all configurations
- `Run-ExampleConfigBuilds.ps1` - Build all examples

## Focused Development Workflow

For CR6-specific development (your use case):

### Supported Configurations
1. **CR6 SE v4.5.2**: `config/cr6-se-v4.5.2-mb/`
2. **CR6 SE v4.5.3**: `config/cr6-se-v4.5.3-mb/`
3. **CR6 Max**: `config/cr6-max-stock-mb/`
4. **BTT SKR CR6 + BTT TFT**: `config/btt-skr-cr6-with-btt-tft/`
5. **BTT SKR CR6 + Stock TFT**: `config/btt-skr-cr6-with-stock-creality-tft/`

### Test Your Configurations
```bash
# Test Creality boards
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality

# Test BTT board  
make tests-single-local-docker TEST_TARGET=STM32F103RE_btt_USB

# Build specific configurations
cd tools/linux/build/docker
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"
```

## Troubleshooting

### Common Issues

#### Permission Denied Errors
If you encounter permission issues, particularly with PlatformIO or Docker:

1. **Check file ownership**: `ls -la .pio/build/`
2. **Fix ownership**: `sudo chown -R $USER:$USER .pio/`
3. **Clean build artifacts**: `sudo rm -rf .pio/build/*`
4. **Use Docker user mapping**: See [Permission Management](#permission-management) section

#### PlatformIO Initialization Failures
- Usually caused by root-owned files in `.pio/` directory
- Follow the permission fixing steps above
- If persistent, reset PlatformIO: `sudo rm -rf ~/.platformio/ .pio/`

#### Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Then logout/login or run:
newgrp docker
```

#### Linux Keyring Issues
If you see keyring errors when opening VS Code:
```bash
# Check keyring service status
systemctl --user status gnome-keyring-daemon

# Reset keyring if needed
rm -rf ~/.local/share/keyrings/
```

#### PowerShell Script Execution on Linux
Use the provided wrapper instead of direct execution:
```bash
# Use this instead of direct PowerShell
./run-powershell.sh scripts/Run-ExampleConfigBuilds.ps1 [arguments]
```

#### Build Environment Incompatibility
- **Error**: "Build environment 'X' is incompatible with BOARD_Y"
- **Solution**: Ensure environment matches board configuration
- **Example**: `BOARD_CREALITY_V453` requires `STM32F103RET6_creality`

#### Python Path Issues in Docker
- Some builds may fail with path-related errors
- This is typically due to configuration mismatches
- Ensure you're using the correct config/environment combination

#### Memory Issues
```bash
# If builds fail due to memory constraints
cd tools/build/docker
docker-compose run --rm marlin bash -c "ulimit -m 2097152 && platformio run -e STM32F103RET6_creality"
```

### Permission Management Quick Fixes

#### Automated Permission Check
```bash
#!/bin/bash
# check-permissions.sh - Verify development environment permissions
echo "Checking PlatformIO permissions..."
if [ -d ".pio" ]; then
    ROOT_FILES=$(find .pio -user root 2>/dev/null | wc -l)
    if [ $ROOT_FILES -gt 0 ]; then
        echo "WARNING: Found $ROOT_FILES root-owned files in .pio/"
        echo "Run: sudo chown -R \$USER:\$USER .pio/"
    else
        echo "✓ PlatformIO permissions OK"
    fi
else
    echo "✓ No .pio directory found"
fi
```

#### Complete Environment Reset
```bash
# Nuclear option - reset everything
sudo rm -rf .pio/
sudo rm -rf ~/.platformio/
pip install --user platformio
```

### Debug Information

#### Check Available Platforms
```bash
cd tools/build/docker
docker-compose run --rm marlin platformio platform list
```

#### Verbose Build Output
```bash
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality VERBOSE_PLATFORMIO=1
```

#### Container Shell Access
```bash
cd tools/linux/build/docker
docker-compose run --rm marlin bash
```

#### Environment Verification
```bash
#!/bin/bash
# verify-environment.sh
echo "=== Environment Check ==="
echo "OS: $(uname -s -r)"
echo "Docker: $(docker --version 2>/dev/null || echo 'Not installed')"
echo "Docker Compose: $(docker-compose --version 2>/dev/null || echo 'Not installed')"
echo "PlatformIO: $(pio --version 2>/dev/null || echo 'Not installed')"
echo "Python: $(python3 --version 2>/dev/null || echo 'Not installed')"
echo ""
echo "=== Permission Check ==="
if [ -d ".pio" ]; then
    ROOT_FILES=$(find .pio -user root 2>/dev/null | wc -l)
    echo "Root-owned files in .pio/: $ROOT_FILES"
fi
echo "Current user: $(whoami)"
echo "Docker group membership: $(groups | grep -o docker || echo 'Not in docker group')"
```

### Getting Help

- **Community Discord**: [CR6 Community Discord](https://discord.gg/RKrxYy3Q9N)
- **GitHub Issues**: Report bugs and permission issues with full error output
- **Include System Info**: OS, Docker version, PlatformIO version when reporting issues
- **GitHub Issues**: Use for bugs and feature requests
- **Marlin Documentation**: [marlinfw.org](http://marlinfw.org)

## Performance Notes

### Build Times
- **Single platform test**: ~2-3 minutes
- **All platform tests**: ~2-3 hours
- **Docker container build**: ~5-10 minutes (first time)

### Resource Usage
- **RAM**: ~2GB recommended for Docker builds
- **Disk**: ~5GB for complete environment
- **Network**: Initial setup downloads ~500MB

### Optimization Tips
- Use `platformio-cache` volume for faster subsequent builds
- Run specific platform tests rather than full suite during development
- Use `ONLY_TEST` parameter to filter test subsets

---

*This documentation covers the sophisticated build and test infrastructure already present in the repository. The tools provide professional-grade automated testing and build capabilities for reliable firmware development.*
