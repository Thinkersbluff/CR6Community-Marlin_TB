# Tools Directory

This directory contains platform-specific tools for building, testing, and developing with the CR6 Community Marlin firmware.

## Directory Structure

```
tools/
├── linux/          # Tools for Linux/macOS users
│   ├── build/       # Build scripts and configuration
│   ├── test/        # Testing utilities
│   └── vscode/      # VS Code integration tools
├── windows/         # Tools for Windows users
│   ├── build/       # Build scripts and configuration
│   ├── test/        # Testing utilities
│   └── vscode/      # VS Code integration tools
└── analysis/        # Cross-platform analysis and monitoring tools
    └── temperature-monitoring/  # Performance analysis and data gathering
```

## Quick Start

### Linux/macOS Users
```bash
# Navigate to Linux tools
cd tools/linux

# For building firmware
cd build
./build-configs.sh

# For running PowerShell scripts via Docker
./run-powershell.sh ../../../tools/windows/build/Run-ExampleConfigBuilds.ps1 -ReleaseName test
```

### Windows Users
```powershell
# Navigate to Windows tools
cd tools/windows

# For building firmware
cd build
./Run-ExampleConfigBuilds.ps1 -ReleaseName test

# For individual builds
./Invoke-PioBuild.ps1 -ConfigName cr6-se-v4.5.3-mb
```

### Analysis Tools (All Platforms)
```bash
# Navigate to analysis tools
cd tools/analysis

# Temperature monitoring and performance analysis
cd temperature-monitoring
# (Python tools will be available after integration)
```

## Philosophy

The tools are organized by **platform** to provide the most intuitive user experience:

- **If you're on Linux/macOS** → go to `tools/linux/`
- **If you're on Windows** → go to `tools/windows/`

Within each platform directory, tools are organized by **function**:

- **`build/`** → Everything related to building firmware
- **`test/`** → Everything related to testing
- **`vscode/`** → Everything related to VS Code integration

For **cross-platform analysis tools**:

- **`analysis/`** → Performance monitoring, data gathering, and comparative analysis tools

This structure follows the principle that users should be able to navigate to their platform once, then find all related functionality in a logical hierarchy. Analysis tools are kept platform-agnostic since they're typically Python-based and serve users on all platforms.
