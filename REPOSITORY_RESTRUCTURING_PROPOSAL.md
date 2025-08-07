# Repository Restructuring Proposal

**Date:** August 7, 2025  
**Repository:** CR6Community-Marlin_TB  
**Current Branch:** extui  
**Proposed for:** New restructuring branch  

## Executive Summary

This document proposes a comprehensive restructuring of the CR6Community-Marlin_TB repository to improve organization, reduce root directory clutter, and create a more professional structure that better serves both inexperienced users and experienced programmers working across Windows and Linux platforms.

## Current Issues

The repository root directory currently contains a mix of different file types that lack logical organization:

- **Documentation files:** `BUILD_AND_TEST.md`, `CHANGELOG_6.1_to_6.2.md`, `SECURITY.md`
- **Build scripts:** `build-configs.sh`, `get_test_targets.py`, `get-docker.sh`, `run-powershell.sh`
- **IDE configuration:** `process-palette.json`, `compile_commands.json`
- **Docker configuration:** `docker-compose.yml`, `.env`
- **Project metadata:** Various configuration files
- **Hidden directories:** `.vscode/`, `.github/`, etc.

This organization creates several problems:
1. **Root directory clutter** making it hard to find important files
2. **Mixed concerns** with build tools, documentation, and configs intermixed
3. **Platform confusion** with both Linux and Windows scripts at root level
4. **Unclear entry points** for new contributors
5. **Non-standard structure** compared to modern open-source projects

## Proposed New Structure

```
CR6Community-Marlin_TB/
├── README.md                          # Keep main README in root
├── LICENSE                            # Keep license in root  
├── platformio.ini                     # Keep PlatformIO config in root
├── Makefile                          # Keep Makefile in root
├── .gitignore                        # Git files stay in root
├── .gitattributes
├── .editorconfig
├── 
├── Marlin/                           # Main firmware source (unchanged)
├── config/                           # Hardware configurations (unchanged)
├── buildroot/                        # Build system tools (unchanged)
├── ini/                              # PlatformIO configs (unchanged)
├── 
├── docs/                             # 📁 ENHANCED - All documentation
│   ├── README.md                     # Move from current docs/
│   ├── BUILD_AND_TEST.md             # Move from root
│   ├── CHANGELOG_6.1_to_6.2.md       # Move from root
│   ├── SECURITY.md                   # Move from root
│   ├── development/                  # New subdirectory
│   │   ├── Bresenham.md              # Move from docs/
│   │   ├── Queue.md                  # Move from docs/
│   │   └── Serial.md                 # Move from docs/
│   └── hardware/                     # New subdirectory for hardware docs
│
├── tools/                            # 📁 NEW - Development and build tools
│   ├── build/                        # Build-related scripts
│   │   ├── build-configs.sh          # Move from root
│   │   ├── get_test_targets.py       # Move from root
│   │   └── docker/                   # Docker-related files
│   │       ├── get-docker.sh         # Move from root
│   │       ├── docker-compose.yml    # Move from root
│   │       ├── Dockerfile            # Move from docker/
│   │       └── .env                  # Move from root
│   ├── scripts/                      # Platform-specific scripts
│   │   ├── powershell/               # Windows PowerShell scripts
│   │   │   ├── Common.ps1            # Move from scripts/
│   │   │   ├── Generate-ConfigExample.ps1
│   │   │   ├── Invoke-PioBuild.ps1
│   │   │   ├── Join-UpstreamChanges.ps1
│   │   │   ├── Run-ExampleConfigBuilds.ps1
│   │   │   ├── Update-ConfigExampleChanges.ps1
│   │   │   ├── Update-ConfigExamples.ps1
│   │   │   └── build-incl/           # Move from scripts/
│   │   └── linux/                    # Linux-specific scripts
│   │       └── run-powershell.sh     # Move from root
│   ├── vscode/                       # VS Code specific tools
│   │   ├── process-palette.json      # Move from root
│   │   └── compile_commands.json     # Move from root
│   └── temperature-monitoring/       # FUTURE: Integration point for new tools
│
├── .dev/                             # 📁 NEW - Development environment configs
│   ├── vscode/                       # VS Code configuration
│   │   ├── c_cpp_properties.json     # Move from .vscode/
│   │   ├── extensions.json           # Move from .vscode/
│   │   ├── launch.json               # Move from .vscode/
│   │   └── settings.json             # Move from .vscode/
│   └── github/                       # GitHub configuration  
│       ├── ISSUE_TEMPLATE/           # Move from .github/
│       ├── workflows/                # Move from .github/
│       ├── code_of_conduct.md        # Move from .github/
│       ├── issue_template.md         # Move from .github/
│       └── pull_request_template.md  # Move from .github/
│
└── build/                            # 📁 NEW - Build outputs and cache
    └── .gitkeep                      # Placeholder for build directory
```

## Key Changes and Benefits

### 1. Enhanced Documentation Structure (`docs/`)

**Changes:**
- Consolidate all documentation in one logical location
- Create subdirectories for different types of documentation
- Move build documentation, changelog, and security info from root

**Benefits:**
- **Single entry point** for all documentation
- **Organized by audience:** general docs vs development docs vs hardware docs
- **Easy maintenance** with related docs grouped together
- **Professional presentation** following open-source conventions

### 2. Dedicated Tools Directory (`tools/`)

**Changes:**
- Create platform-specific script organization
- Group build tools, Docker tools, and VS Code tools separately
- Clear separation between PowerShell (Windows) and Linux scripts

**Benefits:**
- **Reduced root clutter** by moving 8+ files to organized subdirectories
- **Platform clarity** - users immediately know which scripts to use
- **Functional grouping** - build tools separate from development tools
- **Extensible structure** - easy to add new tool categories

### 3. Development Environment Configuration (`.dev/`)

**Changes:**
- Move hidden configuration directories to visible, organized location
- Separate VS Code configs from GitHub configs
- Maintain tool-specific organization

**Benefits:**
- **Visible to developers** - not hidden in dot directories
- **Professional structure** similar to modern development frameworks
- **Easy to find and modify** development configurations
- **Clear separation** between runtime configs and development configs

### 4. Improved Cross-Platform Support

**Changes:**
- Dedicated directories for Windows (`tools/scripts/powershell/`) and Linux (`tools/scripts/linux/`)
- Updated documentation to point to correct platform-specific tools
- Clear separation of platform-specific concerns

**Benefits:**
- **Eliminates confusion** about which scripts to use on which platform
- **Better onboarding** for developers on different operating systems
- **Maintained compatibility** with existing workflows
- **Future-ready** for additional platform support

### 5. Build Output Organization

**Changes:**
- Create dedicated `build/` directory for generated files
- Establish convention for build artifact organization

**Benefits:**
- **Keeps root clean** of build artifacts
- **Standard practice** in professional projects
- **Clear separation** between source and generated files
- **Improved .gitignore** management

## Migration Benefits

### For Inexperienced Users
- **Less overwhelming** root directory with clear entry points
- **Obvious documentation location** at `docs/`
- **Platform-specific guidance** eliminates confusion
- **Professional appearance** builds confidence in the project

### For Experienced Programmers
- **Familiar structure** following modern conventions (similar to Rust, Go, Node.js projects)
- **Logical separation of concerns** (source, tools, docs, configs)
- **Easy navigation** and tool discovery
- **Standard patterns** for build and development workflows

### For Cross-Platform Development
- **Clear platform separation** in scripts and documentation
- **Maintained backward compatibility** where possible
- **Better IDE integration** with organized configurations
- **Simplified CI/CD** with organized GitHub configurations

## Implementation Strategy

### Phase 1: Core Restructuring
1. Create new directory structure
2. Move files to new locations
3. Update internal references in scripts and configs
4. Update documentation to reflect new paths

### Phase 2: Tool Integration
1. Update build scripts to use new paths
2. Modify VS Code configurations for new structure
3. Update Docker configurations for new file locations
4. Test all build and development workflows

### Phase 3: Documentation and Communication
1. Update main README with new structure guide
2. Create migration guide for existing contributors
3. Update BUILD_AND_TEST.md with new tool locations
4. Document new conventions for future development

### Phase 4: Future Tool Integration
1. Integrate `tools/temperature-monitoring/` when ready
2. Establish patterns for adding new tools
3. Document tool organization conventions

## Future Tool Integration

The proposed structure specifically accommodates future tool additions:

- **`tools/temperature-monitoring/`** can be added as a peer to other tool directories
- **Additional platform scripts** can be added under `tools/scripts/`
- **New build tools** can be organized under `tools/build/`
- **Development utilities** can be added under appropriate tool categories

This makes the repository structure **extensible** while maintaining **organization**.

## File Movement Summary

### Files Moving to `docs/`:
- `BUILD_AND_TEST.md` (from root)
- `CHANGELOG_6.1_to_6.2.md` (from root)
- `SECURITY.md` (from root)
- `docs/Bresenham.md` → `docs/development/Bresenham.md`
- `docs/Queue.md` → `docs/development/Queue.md`
- `docs/Serial.md` → `docs/development/Serial.md`

### Files Moving to `tools/`:
- `build-configs.sh` → `tools/build/build-configs.sh`
- `get_test_targets.py` → `tools/build/get_test_targets.py`
- `get-docker.sh` → `tools/build/docker/get-docker.sh`
- `docker-compose.yml` → `tools/build/docker/docker-compose.yml`
- `docker/Dockerfile` → `tools/build/docker/Dockerfile`
- `.env` → `tools/build/docker/.env`
- `run-powershell.sh` → `tools/scripts/linux/run-powershell.sh`
- `scripts/*` → `tools/scripts/powershell/*`
- `process-palette.json` → `tools/vscode/process-palette.json`
- `compile_commands.json` → `tools/vscode/compile_commands.json`

### Files Moving to `.dev/`:
- `.vscode/*` → `.dev/vscode/*`
- `.github/*` → `.dev/github/*`

### Files Staying in Root:
- `README.md`
- `LICENSE`
- `platformio.ini`
- `Makefile`
- `.gitignore`
- `.gitattributes`
- `.editorconfig`
- `Marlin/` (directory)
- `config/` (directory)
- `buildroot/` (directory)
- `ini/` (directory)

## Branching Strategy Considerations

### Current Approach Assessment
Creating a dedicated branch for this restructuring is **excellent practice** because:

1. **Isolated changes** - Large structural changes don't interfere with ongoing development
2. **Safe experimentation** - Can test the new structure thoroughly before merging
3. **Easy rollback** - If issues arise, the original structure remains intact
4. **Clear review process** - Changes can be reviewed as a cohesive unit
5. **Controlled integration** - Can merge when ready without rushing

### Future Tool Integration
The absence of `tools/temperature-monitoring` in the current branch is **not a problem** because:

1. **Forward compatibility** - The new structure specifically accommodates this addition
2. **Clean integration** - When ready, `temperature-monitoring` can be added to `tools/` easily
3. **Independent timelines** - Restructuring and new tool development can proceed independently
4. **Merge flexibility** - The temperature monitoring tool can be merged into the restructured branch later

### Recommended Next Steps
1. **Complete restructuring** on the dedicated branch
2. **Test all workflows** to ensure nothing breaks
3. **Update documentation** to reflect new structure
4. **Review and refine** the organization based on testing
5. **Merge temperature-monitoring** tool when ready (fits perfectly in `tools/`)
6. **Merge to main** when restructuring is validated

## Success Metrics

This restructuring will be successful when:

- [ ] Root directory contains ≤10 files (vs current ~15+)
- [ ] All documentation is discoverable in `docs/`
- [ ] Platform-specific scripts are clearly separated
- [ ] Build workflows function identically to current setup
- [ ] New contributors can easily understand project structure
- [ ] Existing contributors can adapt to new structure quickly
- [ ] Future tools can be integrated following established patterns

## Conclusion

This restructuring transforms the CR6Community-Marlin_TB repository from an organically-grown file collection into a professionally-structured project that serves users across platforms effectively. The proposed organization follows modern open-source conventions while specifically addressing the unique needs of firmware development with complex build requirements and cross-platform support.

The dedicated branch approach for implementing this change is optimal, and the absence of the temperature-monitoring tool presents no obstacles - the new structure is designed to accommodate that addition seamlessly when ready.
