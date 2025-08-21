# Build & Test Documentation (Windows 10/11)


This document provides users with basic instructions and workflows for configuring this repository and building CR6Community Firmware on a Windows 10 or 11 platform.

> **Dual-Boot & Cross-Platform Note:**
> If you use both Windows and Linux/macOS on the same computer (dual-boot), you can use the same repository, Dockerfile, and docker-compose.yml files on both operating systems. On Windows, Docker Desktop is recommended. On Linux/macOS, Podman is supported and can use the same compose and Dockerfile, but some advanced features or volume paths may differ. See also [DUAL_BOOT_GUIDELINES.md](../DUAL_BOOT_GUIDELINES.md).

> **Note:** If you use both Windows and Linux/macOS on the same computer to maintain this repository, see also the [DUAL_BOOT_GUIDELINES.md](../DUAL_BOOT_GUIDELINES.md).

## Table of Contents
- [Build \& Test Documentation (Windows 10/11)](#build--test-documentation-windows-1011)
  - [Table of Contents](#table-of-contents)
  - [Script Usage Guidelines](#script-usage-guidelines)
    - [Examples:](#examples)
  - [Containerized (Docker Desktop) Environment](#containerized-docker-desktop-environment)
    - [Install Docker Desktop](#install-docker-desktop)
  - [Next Steps After Installing Docker Desktop](#next-steps-after-installing-docker-desktop)
  - [Build Methods](#build-methods)
    - [1. Docker-based Building (Recommended)](#1-docker-based-building-recommended)
      - [Build Specific Configuration](#build-specific-configuration)
      - [Interactive Docker Session](#interactive-docker-session)
    - [2. Local PlatformIO Building](#2-local-platformio-building)
      - [Requirements](#requirements)
      - [Process](#process)
  - [Windows Build Scripts](#windows-build-scripts)
  - [Permission Management](#permission-management)
  - [Testing Infrastructure](#testing-infrastructure)
  - [Configuration Management](#configuration-management)
  - [Makefile Targets](#makefile-targets)
    - [Setup Targets](#setup-targets)
    - [Testing Targets](#testing-targets)
  - [Continuous Integration](#continuous-integration)
  - [Build Tools and Scripts](#build-tools-and-scripts)
  - [Focused Development Workflow](#focused-development-workflow)
  - [Troubleshooting](#troubleshooting)
      - [AWK strftime Error When Running Build Scripts](#awk-strftime-error-when-running-build-scripts)
  - [Performance Notes](#performance-notes)
  - [Security Guidelines](#security-guidelines)
  - [Adding Automated Testing Support](#adding-automated-testing-support)
    - [Where to Install PyYAML](#where-to-install-pyyaml)
    - [Installation Instructions (WSL2)](#installation-instructions-wsl2)
    - [Usage](#usage)
  - [Appendix](#appendix)
    - [Why Docker Desktop on Windows?](#why-docker-desktop-on-windows)
    - [Checking WSL Integration in Docker Desktop](#checking-wsl-integration-in-docker-desktop)
  - [Managing Docker Compose Sessions](#managing-docker-compose-sessions)
    - [When and How to Use `docker compose up` and `docker compose down`](#when-and-how-to-use-docker-compose-up-and-docker-compose-down)
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
+- During installation, you will see an option: **"Allow Windows Containers to be used with this installation"**.
+  - **You should check this box.** Enabling Windows container support ensures maximum compatibility and avoids potential conflicts or limitations when switching between Windows and Linux/macOS environments, especially on dual-boot systems. This setting does not interfere with Linux container usage and is recommended for all users.
- Start Docker Desktop from the Start menu
- The tool will prompt you to also install the Windows Subsystem for Linux, which will also enable you to run Linux scripts and programs.
- You can use Docker Desktop for local Marlin firmware builds without creating an account or signing in. Just skip any sign-in prompt.
- When Docker Desktop prompts you to install Windows Subsystem for Linux (WSL), it is only so that Docker can use it in the background for Linux containers.
You can simply exit out of the WSL app (the Linux terminal window) unless you specifically want to use it for other purposes. You do not need to create a user on WSL for working with this repo.  You can just close the app, once it has been installed.

## Next Steps After Installing Docker Desktop

Once you have installed Docker Desktop:

1. **Tutorial Screen:**  
   When Docker Desktop opens, you may see a welcome screen or be prompted to go through a tutorial.  
   - You can safely skip the tutorial if you prefer.  
   - Skipping the tutorial does not affect your ability to use Docker Desktop for Marlin firmware development.

2. **Verify Docker is Running:**  
   - Look for the Docker whale icon in your system tray (bottom right of your screen).
   - Hover over the icon or click it to confirm Docker is running and says "Engine running" at the bottom left of the window.

3. **Map Your Repository Folder to Docker Desktop:**  
   - Open Docker Desktop.
   - Go to **Settings > Resources > File Sharing**.
   - Click the "+" button and add the drive or folder where your repository is located (for example, `B:\3D_Objects\GitHubClones\CR-6_Community - Marlin`).
   - Click "Apply & Restart" if prompted.
   - This step ensures Docker containers can access your files.

**WARNING:** Windows will NOT be able to mount a mapped network drive, so you will have to clone the repository to a local drive on your Windows platform!

4. **Open a Container Shell:**  
   In a PowerShell terminal on your local machine:
   1. Navigate to the root directory of the repo, where you have cloned it.
   2. Paste this command to open a Bash terminal in the marlin-dev container:
      ```
      docker compose run --rm marlin bash
      ```
   **NOTE:** The first run of that script will take a while, as docker creates a local image of the container. (Subsequent runs of this script will go much faster.)

5. **Proceed to Build Firmware:**  
   - Follow the rest of this document to build Marlin firmware using Docker Desktop.
   - Use the provided Docker Compose and build scripts as described in the [Build Methods](#build-methods) section.

---

**If you encounter issues starting Docker Desktop or with WSL integration, see the [Troubleshooting](#troubleshooting) section**


1. **Proceed to Build Firmware:**  
   - Follow the rest of this document to build Marlin firmware using Docker Desktop.
   - Use the provided Docker Compose and build scripts as described in the [Build Methods](#build-methods) section.

---

**If you encounter issues starting Docker Desktop or with WSL integration, see the [Troubleshooting](#troubleshooting) section


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

PowerShell build scripts are provided in `tools/windows_developers/build/`. Example usage:
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
- **Docker/WSL version issues:**  
  - Docker Desktop requires WSL 2 and a recent WSL kernel to run Linux containers.
  - If Docker claims your WSL is "too old" but WSL says it is up to date, you may need to update the WSL kernel manually:
  - 
    1. Open PowerShell and run:
       ```
       wsl --status
       ```
       If your kernel is outdated, a link to the latest kernel update package will be shown.
    2. To update automatically (Windows 10 21H1 or later), run:
       ```
       wsl --update
       ```
    3. Or download and install the latest WSL2 kernel update package from:  
       https://aka.ms/wsl2kernel
    4. Restart your computer after updating.
    5. To check your installed WSL versions, run:
       ```
       wsl --list --verbose
       ```
       Make sure your distributions are using Version 2.
    6. To set WSL 2 as default:
       ```
       wsl --set-default-version 2
       ```
  - After updating, Docker Desktop should recognize your WSL as up to date.

#### AWK strftime Error When Running Build Scripts

**Symptom:**  
You encounter an error similar to:
```
awk: line 2: function strftime never defined
```

**Cause:**  
The version of `awk` available in your WSL2 Linux environment does not support the `strftime` function, which is required by the build scripts for timestamped logging. This is often due to using an outdated or unsupported Linux distribution (such as Ubuntu 18.04 or Debian Buster) in WSL2, which may no longer have access to up-to-date package repositories.

**Solution:**  
You need to upgrade your WSL2 Linux distribution to a supported and up-to-date version (such as Ubuntu 22.04 or later).  
Do not run `apt-get` commands inside the Docker container terminal. Instead, perform the upgrade in your WSL2 terminal.

**To upgrade your WSL2 Ubuntu distribution:**

1. **Edit the Release Upgrade Configuration:**
    ```sh
    sudo nano /etc/update-manager/release-upgrades
    ```
    - Find the line:  
       `Prompt=lts`
    - Change it to:  
       `Prompt=normal`
    - Save and exit (Ctrl+O, Enter, Ctrl+X).

2. **Run the Upgrade Command:**
    ```sh
    sudo do-release-upgrade
    ```
    - Follow the prompts to upgrade to the latest Ubuntu release.

**Important Notes:**
- **LTS vs. Non-LTS:** LTS versions (e.g., 20.04, 22.04) are stable and supported for 5 years. Non-LTS versions (e.g., 22.10) are supported for only 9 months. For most users, LTS is recommended for stability.
- **Next LTS Release:** If you are already on an LTS version (e.g., 22.04), you will need to wait for the next LTS release (e.g., 24.04) to upgrade, unless you set `Prompt=normal` to allow non-LTS upgrades.

**After upgrading, re-run your build script.**  
This will ensure your environment has access to up-to-date packages (including `gawk`), and the required `strftime` function will be available.

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

---

## Adding Automated Testing Support
← [ToC](#table-of-contents)

To enable automated test extraction and local test runs (such as extracting build targets from GitHub Actions workflows), you need to install the PyYAML package for Python.

### Where to Install PyYAML

If you are running Python scripts (such as `get_test_targets.py`) from WSL2 (Ubuntu), you only need to install PyYAML in your WSL2 environment. This will allow you to run Python test scripts directly from WSL2, regardless of Docker.

You do NOT need to install PyYAML in the container unless you plan to run those Python scripts inside the container itself. For most developer workflows, installing PyYAML in WSL2 is sufficient and recommended.

### Installation Instructions (WSL2)

1. **Install PyYAML using pip:**
   ```bash
   pip install pyyaml
   ```
   If you use a virtual environment, activate it first.

2. **Verify installation:**
   ```bash
   python -c "import yaml; print(yaml.__version__)"
   ```
   This should print the installed PyYAML version without error.

3. **Troubleshooting:**
   - If you see `ModuleNotFoundError: No module named 'yaml'`, ensure you installed PyYAML in the correct Python environment in WSL2.
   - For system-wide install (not recommended for all users):
     ```bash
     sudo pip install pyyaml
     ```

### Usage
- Any script that uses `import yaml` (such as `tools/linux_developers/test/get_test_targets.py`) requires PyYAML to be installed in WSL2.
- If you use VS Code and see a Pylance warning about `yaml` not being resolved, installing PyYAML in WSL2 will fix it.

---

## Appendix
← [ToC](#table-of-contents)

### Why Docker Desktop on Windows?

While Podman is used for containerization on Linux and macOS, Docker Desktop is currently recommended for Windows because it is more mature and stable on this platform. Podman Desktop for Windows is still evolving and may not provide the same level of integration or reliability as Docker Desktop, especially for complex development workflows. If Podman Desktop becomes equally robust on Windows in the future, this recommendation may change.

---

### Checking WSL Integration in Docker Desktop

If you plan to use WSL for other Linux workflows, verify that Docker Desktop is properly integrated with WSL:

1. Open Docker Desktop.
2. Go to **Settings > Resources > WSL Integration**.
3. Ensure your desired Linux distributions are enabled for integration.
4. You can also check WSL status in PowerShell:
   ```sh
   wsl --status
   wsl --list --verbose
   ```
   Make sure your distributions are using Version 2.

---

## Managing Docker Compose Sessions
← [ToC](#table-of-contents)

### When and How to Use `docker compose up` and `docker compose down`

- **`docker compose up`**
  - Use this command to start all services defined in your `compose.yaml` file.
  - It builds images (if needed), creates containers, and starts them in the background.
  - Example:
    ```powershell
    docker compose up -d
    ```
    The `-d` flag runs the containers in detached mode (in the background).
  - Use this if you want to start the full development environment or run multiple services at once.

- **`docker compose down`**
  - Use this command to stop and remove all containers, networks, and volumes created by `docker compose up`.
  - Example:
    ```powershell
    docker compose down
    ```
  - Use this when you are finished working and want to clean up resources, or if you need to reset the environment.

- **Typical Workflow:**
  1. Start your environment:
     ```powershell
     docker compose up -d
     ```
  2. Open a shell in the running container (if needed):
     ```powershell
     docker compose exec marlin bash
     ```
  3. When finished, stop and clean up:
     ```powershell
     docker compose down
     ```

> **Note:**  
> If you use `docker compose run --rm marlin bash` for one-off tasks, you do not need to run `docker compose up` first.  
> Use `docker compose down` to clean up any networks or volumes left by previous `up` commands.

---

*Add any other background or advanced tips here as needed!*