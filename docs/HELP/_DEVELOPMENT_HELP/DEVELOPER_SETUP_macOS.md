# Build & Test Documentation (macOS)

This document provides users with basic instructions and workflows for configuring this repository and building CR6Community Firmware on a macOS platform.

> **Note:** If you use both macOS and Windows on the same computer to maintain this repository, see also the [DUAL_BOOT_GUIDELINES.md](../DUAL_BOOT_GUIDELINES.md).

## Table of Contents
- [Build \& Test Documentation (macOS)](#build--test-documentation-macos)
  - [Table of Contents](#table-of-contents)
  - [Script Usage Guidelines](#script-usage-guidelines)
    - [Examples:](#examples)
  - [Containerized (Podman) Environment](#containerized-podman-environment)
    - [Install Podman and Podman Compose](#install-podman-and-podman-compose)
    - [Use the configuration files in `tools/macos/build/podman/`.](#use-the-configuration-files-in-toolsmacosbuildpodman)
  - [Build Methods](#build-methods)
    - [1. Container-based Building, using Podman (Recommended)](#1-container-based-building-using-podman-recommended)
      - [Build Specific Configuration](#build-specific-configuration)
      - [Interactive Podman Session](#interactive-podman-session)
    - [2. Local PlatformIO Building](#2-local-platformio-building)
      - [Requirements](#requirements)
      - [Process](#process)
  - [macOS Build Scripts](#macos-build-scripts)
  - [Permission Management](#permission-management)
    - [Preventing Permission Issues](#preventing-permission-issues)
    - [Diagnosing Permission Problems](#diagnosing-permission-problems)
    - [Fixing Permission Issues](#fixing-permission-issues)
      - [Method 1: Fix Ownership (Quick Fix)](#method-1-fix-ownership-quick-fix)
      - [Method 2: Clean and Rebuild](#method-2-clean-and-rebuild)
      - [Method 3: Reset PlatformIO Environment](#method-3-reset-platformio-environment)
      - [Method 4: Podman User Mapping (Permanent Solution)](#method-4-podman-user-mapping-permanent-solution)
  - [Testing Infrastructure](#testing-infrastructure)
  - [Configuration Management](#configuration-management)
  - [Makefile Targets](#makefile-targets)
    - [Setup Targets](#setup-targets)
    - [Testing Targets](#testing-targets)
  - [Continuous Integration](#continuous-integration)
  - [Build Tools and Scripts](#build-tools-and-scripts)
  - [Focused Development Workflow](#focused-development-workflow)
  - [Troubleshooting (Podman \& PlatformIO)](#troubleshooting-podman--platformio)
    - [Common Issues \& Solutions](#common-issues--solutions)
  - [Performance Notes](#performance-notes)
  - [Security Guidelines](#security-guidelines)
- [Adding Automated Testing Support](#adding-automated-testing-support)
  - [Why?](#why)
  - [Installation Instructions](#installation-instructions)
  - [Usage](#usage)

---

## Script Usage Guidelines
← [ToC](#table-of-contents)

**Golden Rule: Always run scripts from their current location in the repository structure.**

All scripts in this repository are designed to work when you navigate to their directory and run them directly. This aids discovery by new and occasional users and provides a consistent, predictable experience.

### Examples:
```bash
# Build scripts - navigate to your platform's build directory
cd tools/macos/build
./build-configs.sh

# VS Code tools - navigate to your platform's vscode directory
cd tools/macos/vscode
```

## Containerized (Podman) Environment
← [ToC](#table-of-contents)

### Install Podman and Podman Compose
```bash
brew install podman podman-compose
```

- You may need to initialize and start the Podman machine (Podman runs in a lightweight VM on macOS):
  ```bash
  podman machine init
  podman machine start
  ```

### Use the configuration files in `tools/macos/build/podman/`.

## Build Methods
← [ToC](#table-of-contents)

### 1. Container-based Building, using Podman (Recommended)

#### Build Specific Configuration
```bash
cd tools/macos/build/podman
# Build CR6 SE v4.5.3 configuration
# Example:
podman-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"
```

#### Interactive Podman Session
```bash
cd tools/macos/build/podman
# Get shell inside container
podman-compose run --rm marlin bash
# Inside container, you can run any build commands:
platformio run -e STM32F103RET6_creality
./buildroot/bin/build_example config/cr6-se-v4.5.2-mb
```

### 2. Local PlatformIO Building

#### Requirements
- Visual Studio Code with PlatformIO extension
- Python 3.7+
- PlatformIO Core
- Xcode Command Line Tools (for build dependencies):
  ```bash
  xcode-select --install
  ```

#### Process
1. Copy configuration files from `config/[your-config]/` to `Marlin/`
2. Update `platformio.ini` `default_envs` to match `platformio-environment.txt`
3. Build using PlatformIO IDE or command line

## macOS Build Scripts
← [ToC](#table-of-contents)
← [ToC](#table-of-contents)

The build script (`tools/macos/build/build-configs.sh`) can build all or specific configuration examples. The script automatically detects the repository root and can be run from any directory within the repository.

**Basic usage (run from repository root):**
```bash
./tools/macos/build/build-configs.sh
```

**Basic usage (run from tools/macos/build directory):**
```bash
cd tools/macos/build && ./build-configs.sh
```

**Build with custom release name:**
```bash
./tools/macos/build/build-configs.sh v2.1.3.2
```

**Build single configuration:**
```bash
./tools/macos/build/build-configs.sh test-build cr6-se-v4.5.3-mb
```

**Dry run (test without building):**
```bash
./tools/macos/build/build-configs.sh test-build cr6-se-v4.5.3-mb true
```

**Custom touchscreen path:**
```bash
./tools/macos/build/build-configs.sh v2.1.3.2 "" "" ../path/to/CR-6-Touchscreen
```

**All parameters:**
```bash
./tools/macos/build/build-configs.sh release-name cr6-se-v4.5.3-mb false ../CR-6-Touchscreen
```

## Permission Management
← [ToC](#table-of-contents)
← [ToC](#table-of-contents)

Podman containers can create files owned by root, causing permission issues in development workflows. This section covers prevention and resolution strategies.

### Preventing Permission Issues

1. **Use Podman User Mapping** (Recommended):
   ```bash
   podman run --user $(id -u):$(id -g) ...
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
sudo chown -R $(id -u):$(id -g) .
sudo chown -R $(id -u):$(id -g) .pio/
```

#### Method 2: Clean and Rebuild
```bash
sudo rm -rf .pio/build/*
sudo chown -R $(id -u):$(id -g) .pio/
pio system prune --force
```

#### Method 3: Reset PlatformIO Environment
```bash
sudo rm -rf ~/.platformio/
sudo rm -rf .pio/
pip3 install --user platformio
```

#### Method 4: Podman User Mapping (Permanent Solution)
- `tools/build/podman/.env` file with your UID/GID
- Modified `tools/build/podman/podman-compose.yml` with user mapping
- Updated `Dockerfile` that creates a matching user

If you encounter permission issues, first try Method 1 (fix ownership), then rebuild the Podman environment:
```bash
sudo chown -R $(id -u):$(id -g) .
cd tools/build/podman
podman-compose down
podman-compose build --no-cache
```

## Testing Infrastructure
← [ToC](#table-of-contents)
The test infrastructure and documentation will be reviewed, revised, and expanded in a future update. Instructions for running and validating tests will be provided once the new system is in place.

## Configuration Management
← [ToC](#table-of-contents)
← [ToC](#table-of-contents)

Configuration directories are in `config/`. Each contains:
- `Configuration.h` - Main Marlin configuration
- `Configuration_adv.h` - Advanced settings
- `platformio-environment.txt` - PlatformIO environment specification

## Makefile Targets
← [ToC](#table-of-contents)
← [ToC](#table-of-contents)

### Setup Targets
```bash
make setup-local-podman          # Build Podman development environment
```

### Testing Targets
```bash
make tests-single-local          # Run single test locally
make tests-single-local-podman   # Run single test in Podman
make tests-all-local            # Run all tests locally  
make tests-all-local-podman     # Run all tests in Podman
make tests-single-ci            # Run single test (CI mode)
```

## Continuous Integration
← [ToC](#table-of-contents)

See `.github/workflows/test-builds.yml` for CI details. Matrix tests run on all supported platforms using Podman and PlatformIO.

## Build Tools and Scripts
← [ToC](#table-of-contents)

Core build tools are in `buildroot/bin/`:
```bash
build_all_examples      # Build all configuration examples
build_example          # Build specific example
run_tests              # Core test runner script
use_example_configs    # Apply example configuration
restore_configs        # Restore original configuration
```

## Focused Development Workflow
← [ToC](#table-of-contents)

For CR6-specific development, use the supported configurations in `config/` and test using the provided Makefile and Podman commands.

## Troubleshooting (Podman & PlatformIO)
← [ToC](#table-of-contents)

### Common Issues & Solutions

- **Permission denied errors in `.pio` or build directories:**
   - Usually caused by files created as `root` or by a mismatched user inside the container.
   - **Solution:** On your host, run:
      ```bash
      sudo chown -R $(id -u):$(id -g) /path/to/your/project
      sudo chown -R $(id -u):$(id -g) /path/to/your/project/.pio
      ```
   - If you use a Podman volume for PlatformIO cache, fix its permissions:
      ```bash
      podman run --rm -it -v cr6community-marlin_tb_platformio-cache:/data --user root alpine chown -R 1000:1000 /data
      ```

- **PlatformIO cannot find framework packages (e.g., `framework-arduinoststm32`):**
   - The PlatformIO cache volume may be empty or missing the required framework.
      ```bash
      podman run --rm -it \
         -v /path/to/your/project:/code \
         -v cr6community-marlin_tb_platformio-cache:/home/user/.platformio \
         -w /code marlin-dev bash
      # Inside the container:
      platformio run -e <your_env>
      ```

- **"Operation not permitted" when running `chown` inside the container:**
   - You may not have permission to change ownership of files created by root or another user.
   - **Solution:** Always fix permissions on the host using `sudo chown -R $(id -u):$(id -g) ...` or by deleting and recreating the `.pio` directory.

- **Podman volume overwrites pre-installed packages:**
   - If you mount a volume to `/home/user/.platformio`, it will hide any packages installed in the image. Always ensure the volume contains the required packages, or let PlatformIO install them during the first build.

- **General Podman Compose usage:**
   - Use `podman-compose` for orchestration.
   - Example:
      ```bash
      podman-compose up
      podman-compose run --rm marlin bash
      ```

---

## Performance Notes
← [ToC](#table-of-contents)

- Single platform test: ~2-3 minutes
- All platform tests: ~2-3 hours
- Podman container build: ~5-10 minutes (first time)
- RAM: ~2GB recommended for Podman builds
- Disk: ~5GB for complete environment
- Network: Initial setup downloads ~500MB

## Security Guidelines
← [ToC](#table-of-contents)
← [ToC](#table-of-contents)

For macOS users, GPG key management is essential for secure Podman and package installations. Please review [SECURITY.md](SECURITY.md) for:
- How to verify and manage GPG keys
- Best practices for key safety
- Troubleshooting common GPG-related issues

Proper key management helps prevent build failures and protects your system from untrusted packages.

---


# Adding Automated Testing Support
← [ToC](#table-of-contents)

To enable automated test extraction and local test runs (such as extracting build targets from GitHub Actions workflows), you need to install the PyYAML package for Python.

## Why?
Some developer scripts (e.g., `get_test_targets.py`) require the ability to parse YAML files, which is not supported by Python's standard library. The `yaml` module is provided by the third-party package PyYAML.

## Installation Instructions

1. **Install PyYAML using pip:**
  ```bash
  pip install pyyaml
  ```
  If you use a local virtual environment for this work, activate it first, to ensure the package is installed and used in the correct environment.  

2. **Verify installation:**
  ```bash
  python -c "import yaml; print(yaml.__version__)"
  ```
  This should print the installed PyYAML version without error.

3. **Troubleshooting:**
  - If you see `ModuleNotFoundError: No module named 'yaml'`, ensure you installed PyYAML in the correct Python environment.
  - For system-wide install (not recommended for all users):
    ```bash
    sudo pip install pyyaml
    ```

## Usage
- Any script that uses `import yaml` (such as `tools/linux_developers/test/get_test_targets.py`) requires PyYAML to be installed.
- If you use VS Code and see a Pylance warning about `yaml` not being resolved, installing PyYAML will fix it.