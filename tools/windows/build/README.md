# Windows Build Tools

Build tools and PowerShell scripts for Windows users.

## Available Scripts

All scripts are PowerShell (.ps1) files that require PowerShell Core (version 6.0+). Run them from this directory.

### Core Build Scripts

#### Run-ExampleConfigBuilds.ps1
Main build script for creating release packages. Builds all or specific configuration examples.

**Usage:**
```powershell
# Build all configurations for release
./Run-ExampleConfigBuilds.ps1 -ReleaseName "v2.1.3.2"

# Build single configuration
./Run-ExampleConfigBuilds.ps1 -ReleaseName "test-build" -SingleBuild "cr6-se-v4.5.3-mb"

# Dry run (no actual building)
./Run-ExampleConfigBuilds.ps1 -ReleaseName "test" -DryRun

# Custom touchscreen repository path
./Run-ExampleConfigBuilds.ps1 -ReleaseName "v2.1.3.2" -TouchscreenRepositoryPath "C:\Dev\CR-6-Touchscreen"
```

#### Invoke-PioBuild.ps1
Interactive build script for individual configurations with deployment options.

**Usage:**
```powershell
# Interactive mode (will prompt for configuration)
./Invoke-PioBuild.ps1

# Build specific configuration
./Invoke-PioBuild.ps1 -ConfigName "cr6-se-v4.5.3-mb"

# Build and deploy to drive
./Invoke-PioBuild.ps1 -ConfigName "cr6-se-v4.5.3-mb" -Drive "E:"

# Clean build
./Invoke-PioBuild.ps1 -ConfigName "cr6-se-v4.5.3-mb" -ForceClean
```

### Configuration Management Scripts

#### Generate-ConfigExample.ps1
Creates new configuration examples from current Marlin configuration.

**Usage:**
```powershell
# Create new configuration
./Generate-ConfigExample.ps1 -Name "my-new-config"

# Create with interactive merge conflict resolution
./Generate-ConfigExample.ps1 -Name "my-config" -InteractiveResolve

# Create from specific git revision
./Generate-ConfigExample.ps1 -Name "my-config" -GitRevision "abc123def"
```

#### Update-ConfigExamples.ps1
Updates all configuration examples after base configuration changes.

**Usage:**
```powershell
# Update all configurations
./Update-ConfigExamples.ps1

# Update with interactive merge resolution
./Update-ConfigExamples.ps1 -InteractiveResolve

# Update from specific git revision
./Update-ConfigExamples.ps1 -GitRevision "abc123def"
```

#### Update-ConfigExampleChanges.ps1
Interactive tool for merging upstream changes using TortoiseGitMerge.

**Usage:**
```powershell
# Launch interactive merge tool
./Update-ConfigExampleChanges.ps1
```

**Requirements:**
- TortoiseGitMerge.exe must be in PATH
- Interactive GUI session required

### Version Control Scripts

#### Join-UpstreamChanges.ps1
Merges upstream Marlin changes and updates configuration examples.

**Usage:**
```powershell
# Merge upstream changes
./Join-UpstreamChanges.ps1
```

**What it does:**
1. Fetches upstream changes
2. Merges upstream/bugfix-2.1.x branch
3. Updates all configuration examples
4. Resolves merge conflicts interactively

### Common.ps1
Shared functions and utilities used by other scripts. Not meant to be run directly.

**Functions provided:**
- `Write-FatalError()` - Error handling with exit
- `Get-ExampleNames()` - Lists all configuration directories
- Repository root detection
- Common path constants

## Build Includes

The `build-incl/` directory contains files that are included in release packages:

- `CR-6 community firmware discord.url` - Discord community link
- `CR-6 community firmware home page.url` - Project homepage link  
- `README.txt` - Instructions for end users

## Prerequisites

1. **PowerShell Core 6.0+**
   ```powershell
   # Check version
   $PSVersionTable.PSVersion
   ```

2. **PlatformIO CLI**
   ```powershell
   # Should be available in PATH
   pio --version
   ```

3. **Git**
   ```powershell
   # Should be available in PATH
   git --version
   ```

4. **Visual Studio Code** (recommended)
   - PlatformIO IDE extension
   - PowerShell extension

## Getting Started

1. **Open PowerShell in this directory:**
   ```powershell
   cd tools\windows\build
   ```

2. **Test with a single build:**
   ```powershell
   .\Invoke-PioBuild.ps1 -ConfigName "cr6-se-v4.5.3-mb"
   ```

3. **Create a release build:**
   ```powershell
   .\Run-ExampleConfigBuilds.ps1 -ReleaseName "test-build"
   ```

## Troubleshooting

**PowerShell Execution Policy:**
```powershell
# If you get execution policy errors
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**PlatformIO Not Found:**
- Run scripts from VS Code terminal with PlatformIO extension installed
- Or install PlatformIO CLI manually and ensure it's in PATH

**Permission Errors:**
- Ensure you have write permissions to repository directory
- Run PowerShell as Administrator if necessary

For more detailed information, see the main [BUILD_AND_TEST.md](../../../docs/BUILD_AND_TEST.md) documentation.
