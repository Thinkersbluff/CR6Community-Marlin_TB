# Linux Build Tools

Build tools and scripts for Linux and macOS users.

## Available Scripts

### build-configs.sh
Linux equivalent of the Windows `Run-ExampleConfigBuilds.ps1` script. Builds all or specific configuration examples.

**Usage:**
```bash
# Run from this directory
cd tools/linux/build
./build-configs.sh

# Or run with parameters
./build-configs.sh [release-name] [single-config] [dry-run] [touchscreen-repo-path]

# Examples
./build-configs.sh v2.1.3.2                           # Build all with release name
./build-configs.sh test-build cr6-se-v4.5.3-mb        # Build single config
./build-configs.sh test-build cr6-se-v4.5.3-mb true   # Dry run
```

**Features:**
- Docker-based building using PlatformIO
- Automatic ZIP packaging with organized directory structure
- SHA256 checksum generation
- Touchscreen firmware integration
- Configuration validation
- Progress reporting

### run-powershell.sh
Wrapper script for running PowerShell scripts on Linux via Docker.

**Usage:**
```bash
# Run PowerShell script from repository root
./run-powershell.sh ../windows/build/Run-ExampleConfigBuilds.ps1 -ReleaseName test

# Other PowerShell scripts
./run-powershell.sh ../windows/build/Generate-ConfigExample.ps1 -Name my-config
./run-powershell.sh ../windows/build/Invoke-PioBuild.ps1 -ConfigName cr6-se-v4.5.3-mb
```

## Docker Configuration

The `docker/` subdirectory contains the complete Docker development environment:

- `docker-compose.yml` - Main Docker Compose configuration
- `Dockerfile` - Container definition with PlatformIO and dependencies
- `get-docker.sh` - Docker installation helper script
- `.env` - Environment variables for user mapping

**Usage:**
```bash
# Navigate to docker directory first
cd docker

# Build the container
docker-compose build

# Run interactive shell
docker-compose run --rm marlin bash

# Run specific build
docker-compose run --rm marlin bash -c "./buildroot/bin/use_example_configs config/cr6-se-v4.5.3-mb && platformio run -e STM32F103RET6_creality"
```

## Output Structure

Built packages are organized in `.pio/build-output/`:
```
.pio/build-output/
├── [release-name]-[config-name]-[timestamp].zip
│   ├── Firmware/
│   │   ├── Motherboard firmware/
│   │   │   └── firmware.bin
│   │   └── Display Firmware/
│   │       ├── DWIN_SET.zip  (if available)
│   │       └── CR-6-Touchscreen-Download.url  (if not available)
│   ├── configs/
│   │   ├── Configuration.h
│   │   └── Configuration_adv.h
│   └── description.txt
└── checksums.txt
```

## Getting Started

1. **Setup Docker environment:**
   ```bash
   cd docker
   docker-compose build
   ```

2. **Test with a single build:**
   ```bash
   cd ..  # Back to tools/linux/build
   ./build-configs.sh test-build cr6-se-v4.5.3-mb
   ```

3. **Build all configurations:**
   ```bash
   ./build-configs.sh v2.1.3.2
   ```

For more detailed information, see the main [BUILD_AND_TEST.md](../../../docs/BUILD_AND_TEST.md) documentation.
