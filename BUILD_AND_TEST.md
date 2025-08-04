# Build & Test Documentation

This document describes the comprehensive build and test infrastructure available in this repository, including Docker environment setup, automated testing, and various build tools.

## Table of Contents

- [Quick Start](#quick-start)
- [Docker Environment](#docker-environment)
- [Build Methods](#build-methods)
- [Testing Infrastructure](#testing-infrastructure)
- [Configuration Management](#configuration-management)
- [Makefile Targets](#makefile-targets)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Docker and docker-compose installed
- Git repository cloned locally

### Basic Docker Build
```bash
# Setup Docker environment (one-time)
make setup-local-docker

# Test a specific platform
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality

# Run all tests
make tests-all-local-docker
```

## Docker Environment

### Overview
The repository includes a complete Docker-based development environment that provides:
- Consistent build environment across different systems
- All required dependencies (PlatformIO, Python, build tools)
- Isolated testing environment
- Automated CI/CD capabilities

### Docker Setup

#### Initial Setup
```bash
# Install Docker (Ubuntu/Debian)
sudo apt update && sudo apt install -y docker.io docker-compose

# Add user to docker group (requires logout/login to take effect)
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl start docker && sudo systemctl enable docker
```

#### Build Docker Container
```bash
# Build the development container
make setup-local-docker
# or manually:
docker-compose build
```

### Docker Files Structure
- `docker-compose.yml`: Main Docker Compose configuration
- `docker/Dockerfile`: Container definition with PlatformIO and dependencies
- `platformio-cache` volume: Persists PlatformIO libraries between runs

## Build Methods

### 1. Docker-based Building (Recommended)

#### Build Specific Configuration
```bash
# Build CR6 SE v4.5.3 configuration
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"

# Build BTT SKR CR6 configuration
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/btt-skr-cr6-with-btt-tft && platformio run -e STM32F103RE_btt_USB"
```

#### Interactive Docker Session
```bash
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

#### Creality Motherboards (v4.5.2, v4.5.3)
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

### PowerShell Scripts (Maintainers)
Located in `scripts/`:
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
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"
```

## Troubleshooting

### Common Issues

#### Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Then logout/login or run:
newgrp docker
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
docker-compose run --rm marlin bash -c "ulimit -m 2097152 && platformio run -e STM32F103RET6_creality"
```

### Debug Information

#### Check Available Platforms
```bash
docker-compose run --rm marlin platformio platform list
```

#### Verbose Build Output
```bash
make tests-single-local-docker TEST_TARGET=STM32F103RET6_creality VERBOSE_PLATFORMIO=1
```

#### Container Shell Access
```bash
docker-compose run --rm marlin bash
```

### Getting Help

- **Community Discord**: [CR6 Community Discord](https://discord.gg/RKrxYy3Q9N)
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
