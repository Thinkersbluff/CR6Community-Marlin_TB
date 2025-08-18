# Guidebook: Building Marlin Firmware with `build-configs.sh`

## Overview
This guide explains how to use the `build-configs.sh` script from the `tools/linux/build` directory to build and package multiple Marlin firmware configurations using a containerized build environment. It also includes a troubleshooting section based on real-world issues and solutions.

---

## Prerequisites
- Podman and Podman Compose installed and running on your system.
- All required configuration files (`Configuration.h`, `Configuration_adv.h`, `platformio-environment.txt`) present in each `config/<config-name>/` folder.
- The repository cloned to your local machine.

---

## Quick Start
1. **Open a terminal.**
2. **Navigate to the build directory:**
   ```bash
   cd /home/stephen/CR6Community-Marlin_TB/tools/linux/build
   ```
3. **Run the build script:**
   ```bash
   ./build-configs.sh <release-name>
   ```
   Example:
   ```bash
   ./build-configs.sh 6.2_fixed
   ```
   This will build all available configurations and place the output `.zip` files in `.pio/build-output/` in the repo root.

---

## How It Works
- The script auto-detects the repository root.
- It uses Podman Compose to launch a container with the repo mounted at `/code`.
- Each configuration in `config/` is built using its own settings.
- Output firmware and config files are packaged into zip files for distribution.

---

## Troubleshooting
If you encounter errors, follow these steps:

### 1. Podman Cannot Find Files or Configs
- **Symptom:** Errors like `cp: cannot stat .../Configuration*.h: No such file or directory` or missing configs.
- **Solution:**
  - Ensure your `podman-compose.yml` has the correct absolute path for the repo root:
    ```yaml
    volumes:
      - /home/stephen/CR6Community-Marlin_TB:/code
      - platformio-cache:/home/user/.platformio
    ```
  - Make sure you run the script from `tools/linux/build/`.
  - Confirm the files exist on your host:
    ```bash
    ls /home/stephen/CR6Community-Marlin_TB/config/<config-name>/Configuration*.h
    ```
  - Check inside the container:
    ```bash
    podman-compose -f podman/podman-compose.yml run --rm marlin bash
    ls -l /code/config/<config-name>/Configuration*.h
    ```

### 2. File Permissions
- **Symptom:** Files exist but are not readable in podman.
- **Solution:**
  - Ensure files and directories are at least `rw-r--r--` and owned by your user.
  - Avoid symlinks that point outside the repo root.

### 3. Build Succeeds for Some Configs, Fails for Others
- **Symptom:** Only some configs produce firmware, others fail with missing files or environment errors.
- **Solution:**
  - Check that each config folder contains all required files: `Configuration.h`, `Configuration_adv.h`, and `platformio-environment.txt`.
  - Review warnings in the script output for missing files.

### 4. No Firmware Binary Found
- **Symptom:** `ERROR: No firmware binary found for <config-name>`
- **Solution:**
  - The build may have failed due to a misconfiguration or missing dependency. Check the build logs for errors.
  - Ensure the correct PlatformIO environment is specified in `platformio-environment.txt`.

### 5. General Debugging
- Add debug lines to the script before the copy command:
  ```bash
  echo "DEBUG: Listing files in $config_dir"
  ls -l "$config_dir"
  echo "DEBUG: Copying $config_dir/Configuration*.h to Marlin/"
  ```
- This will help you see what files are present and what the script is doing.

---

## Notes
- If you move the repository, update the absolute path in `podman-compose.yml`.
- For portability, add a comment in `podman-compose.yml` to remind users to update the path if they clone the repo elsewhere.
- Always run the script from `tools/linux/build/` for consistent results.

---

## Support
If you encounter issues not covered here, please provide:
- The exact error message
- The output of `ls -l` for the relevant config folder (both on host and in Podman)
- The relevant section of your `podman-compose.yml`

This will help others assist you more quickly.
