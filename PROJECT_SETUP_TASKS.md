# GitHub Project Setup: Repository Restructuring

## Project Overview
**Name:** Repository Restructuring 2025  
**Goal:** Transform CR6Community-Marlin_TB from organically-grown structure to professional organization  
**Target:** Reduce root directory from 15+ files to ≤10 files with logical organization  

## Phase 1: Core Directory Structure

### 1.1 Create New Directory Structure
- [ ] **Create `docs/` directory structure**
  - Create `docs/` root directory
  - Create `docs/development/` subdirectory
  - Create `docs/hardware/` subdirectory
  - Add `.gitkeep` files to maintain empty directories

- [ ] **Create `tools/` directory structure**
  - Create `tools/` root directory
  - Create `tools/build/` subdirectory
  - Create `tools/build/docker/` subdirectory
  - Create `tools/scripts/` subdirectory
  - Create `tools/scripts/powershell/` subdirectory
  - Create `tools/scripts/linux/` subdirectory
  - Create `tools/vscode/` subdirectory
  - Create `tools/temperature-monitoring/` placeholder (for future)

- [ ] **Create `.dev/` directory structure**
  - Create `.dev/` root directory
  - Create `.dev/vscode/` subdirectory
  - Create `.dev/github/` subdirectory

- [ ] **Create `build/` directory**
  - Create `build/` directory
  - Add `.gitkeep` file
  - Update `.gitignore` to handle build artifacts

### 1.2 Move Documentation Files
- [ ] **Move `BUILD_AND_TEST.md`** from root to `docs/BUILD_AND_TEST.md`
- [ ] **Move `CHANGELOG_6.1_to_6.2.md`** from root to `docs/CHANGELOG_6.1_to_6.2.md`
- [ ] **Move `SECURITY.md`** from root to `docs/SECURITY.md`
- [ ] **Move existing docs/** files to development subdirectory
  - Move `docs/Bresenham.md` → `docs/development/Bresenham.md`
  - Move `docs/Queue.md` → `docs/development/Queue.md`
  - Move `docs/Serial.md` → `docs/development/Serial.md`
- [ ] **Move `docs/README.md`** to `docs/README.md` (stays in docs root)

### 1.3 Move Build and Script Files
- [ ] **Move build scripts to `tools/build/`**
  - Move `build-configs.sh` → `tools/build/build-configs.sh`
  - Move `get_test_targets.py` → `tools/build/get_test_targets.py`

- [ ] **Move Docker files to `tools/build/docker/`**
  - Move `get-docker.sh` → `tools/build/docker/get-docker.sh`
  - Move `docker-compose.yml` → `tools/build/docker/docker-compose.yml`
  - Move `docker/Dockerfile` → `tools/build/docker/Dockerfile`
  - Move `.env` → `tools/build/docker/.env`

- [ ] **Move PowerShell scripts to `tools/scripts/powershell/`**
  - Move `scripts/Common.ps1` → `tools/scripts/powershell/Common.ps1`
  - Move `scripts/Generate-ConfigExample.ps1` → `tools/scripts/powershell/Generate-ConfigExample.ps1`
  - Move `scripts/Invoke-PioBuild.ps1` → `tools/scripts/powershell/Invoke-PioBuild.ps1`
  - Move `scripts/Join-UpstreamChanges.ps1` → `tools/scripts/powershell/Join-UpstreamChanges.ps1`
  - Move `scripts/Run-ExampleConfigBuilds.ps1` → `tools/scripts/powershell/Run-ExampleConfigBuilds.ps1`
  - Move `scripts/Update-ConfigExampleChanges.ps1` → `tools/scripts/powershell/Update-ConfigExampleChanges.ps1`
  - Move `scripts/Update-ConfigExamples.ps1` → `tools/scripts/powershell/Update-ConfigExamples.ps1`
  - Move `scripts/build-incl/` → `tools/scripts/powershell/build-incl/`

- [ ] **Move Linux scripts to `tools/scripts/linux/`**
  - Move `run-powershell.sh` → `tools/scripts/linux/run-powershell.sh`

- [ ] **Move VS Code tools to `tools/vscode/`**
  - Move `process-palette.json` → `tools/vscode/process-palette.json`
  - Move `compile_commands.json` → `tools/vscode/compile_commands.json`

### 1.4 Move Development Configuration Files
- [ ] **Move VS Code configuration to `.dev/vscode/`**
  - Move `.vscode/c_cpp_properties.json` → `.dev/vscode/c_cpp_properties.json`
  - Move `.vscode/extensions.json` → `.dev/vscode/extensions.json`
  - Move `.vscode/launch.json` → `.dev/vscode/launch.json`
  - Move `.vscode/settings.json` → `.dev/vscode/settings.json`

- [ ] **Move GitHub configuration to `.dev/github/`**
  - Move `.github/ISSUE_TEMPLATE/` → `.dev/github/ISSUE_TEMPLATE/`
  - Move `.github/workflows/` → `.dev/github/workflows/`
  - Move `.github/code_of_conduct.md` → `.dev/github/code_of_conduct.md`
  - Move `.github/issue_template.md` → `.dev/github/issue_template.md`
  - Move `.github/pull_request_template.md` → `.dev/github/pull_request_template.md`

### 1.5 Clean Up Old Directories
- [ ] **Remove old empty directories**
  - Remove `scripts/` directory (after files moved)
  - Remove `docker/` directory (after files moved)
  - Remove `.vscode/` directory (after files moved)
  - Remove `.github/` directory (after files moved)

## Phase 2: Update File References

### 2.1 Update Docker Configuration
- [ ] **Update `tools/build/docker/docker-compose.yml`**
  - Update Dockerfile path reference
  - Update volume mount paths if needed
  - Test Docker build process

- [ ] **Update Makefile references**
  - Update paths to Docker Compose file
  - Update paths to build scripts
  - Test make targets

### 2.2 Update Build Scripts
- [ ] **Update `tools/build/build-configs.sh`**
  - Update references to Docker Compose location
  - Update any hardcoded paths
  - Test script execution

- [ ] **Update `tools/build/get_test_targets.py`**
  - Update path to GitHub workflows (now in `.dev/github/workflows/`)
  - Test script functionality

### 2.3 Update PowerShell Scripts
- [ ] **Update PowerShell script cross-references**
  - Update imports/includes between PowerShell scripts
  - Update any hardcoded paths to repository files
  - Test PowerShell script execution

### 2.4 Update VS Code Configuration
- [ ] **Create new `.vscode/` directory with references to `.dev/`**
  - Create `.vscode/settings.json` with references to `.dev/vscode/settings.json`
  - Or create symlinks (platform dependent)
  - Test VS Code functionality

- [ ] **Update `tools/vscode/process-palette.json`**
  - Update command paths to new build script locations
  - Test VS Code Process Palette functionality

### 2.5 Update GitHub Workflows
- [ ] **Create new `.github/` directory structure**
  - Create symlinks or copies referencing `.dev/github/`
  - Or update GitHub to look in `.dev/github/`
  - Test CI/CD pipeline functionality

## Phase 3: Documentation Updates

### 3.1 Update Main Documentation (User-Focused)
- [ ] **Update root `README.md` with dual-audience approach**
  - **PRIMARY SECTION**: Clear, simple path for 3D printer owners
    - "I just want firmware for my printer" quick start
    - Download links and basic flashing instructions
    - Hardware compatibility checker
    - Common troubleshooting (friendly language)
  - **SECONDARY SECTION**: Developer and contributor information
    - Link to detailed build documentation
    - Repository structure explanation
    - Contribution guidelines
  - **TERTIARY SECTION**: Repository organization (for reference)

- [ ] **Update `docs/BUILD_AND_TEST.md` for developer audience**
  - Update all script paths to new locations
  - Update Docker setup instructions with new paths
  - Update examples with new directory structure
  - Add troubleshooting section for development environment
  - Include beginner-friendly explanations alongside technical details

### 3.2 Create New Documentation (Audience-Specific)
- [ ] **Create `docs/USERS_START_HERE.md` (Primary User Documentation)**
  - **"I Just Want Firmware"** section with download links
  - **Hardware Compatibility Guide** with simple decision tree
  - **Flashing Instructions** with pictures and simple language
  - **Basic Configuration** for common modifications
  - **Troubleshooting** in plain English
  - **When to Ask for Help** and where to find community support

- [ ] **Create `docs/DEVELOPERS_START_HERE.md` (Developer Documentation)**
  - **Development Environment Setup** (Docker, VS Code, etc.)
  - **Repository Structure Guide** explaining new organization
  - **Contribution Workflow** and coding standards
  - **Testing Requirements** and validation procedures
  - **Advanced Configuration** and customization

- [ ] **Create `docs/REPOSITORY_STRUCTURE.md` (Reference Documentation)**
  - Document the new directory organization
  - Explain purpose of each directory
  - Provide developer onboarding guide
  - Include decision trees for "where does X belong?"

- [ ] **Create migration guide for existing contributors**
  - Document what changed and where things moved
  - Provide command-line helpers for finding moved files
  - Add troubleshooting for common migration issues
  - Include "AI Development Guidelines" to prevent future degradation

### 3.3 Update Tool Documentation (Developer-Focused)
- [ ] **Create `tools/README.md` (Tool Organization Guide)**
  - Explain the tools directory organization
  - Document how to add new tools without degrading structure
  - **Include AI Development Guidelines** to maintain organization
  - Provide platform-specific usage instructions
  - Include "where does my new tool belong?" decision tree

- [ ] **Create platform-specific documentation**
  - Create `tools/scripts/powershell/README.md` (Windows developers)
  - Create `tools/scripts/linux/README.md` (Linux developers)
  - Document platform-specific setup and usage
  - Include beginner-friendly setup instructions
  - Add troubleshooting for common platform issues

- [ ] **Create `docs/AI_DEVELOPMENT_GUIDELINES.md`**
  - **Structure Preservation Rules** for AI-guided development
  - **File Placement Decision Trees** ("Where should this go?")
  - **Naming Conventions** and organizational patterns
  - **Quality Gates** to prevent degradation
  - **Review Checklist** for AI-generated additions

## Phase 4: Testing and Validation

### 4.1 Build System Testing
- [ ] **Test Docker-based builds**
  - Verify Docker Compose works with new paths
  - Test all Docker build configurations
  - Validate build output locations

- [ ] **Test PlatformIO builds**
  - Verify VS Code integration still works
  - Test command-line PlatformIO builds
  - Validate all target platforms

- [ ] **Test build scripts**
  - Test `tools/build/build-configs.sh` on Linux
  - Test PowerShell scripts on Windows (if available)
  - Validate script cross-references work

### 4.2 Development Environment Testing
- [ ] **Test VS Code integration**
  - Verify extensions work with new configuration
  - Test debugging and IntelliSense
  - Validate Process Palette commands

- [ ] **Test CI/CD pipelines**
  - Verify GitHub Actions work with new structure
  - Test all build matrix configurations
  - Validate artifact generation

### 4.3 Documentation Testing
- [ ] **Test all documentation links**
  - Verify internal links work with new structure
  - Test external links still function
  - Validate code examples and paths

- [ ] **Test onboarding process**
  - Follow new contributor documentation
  - Verify setup instructions work for new users
  - Test platform-specific guidance

## Phase 5: Future Integration Preparation

### 5.1 Temperature Monitoring Tool Integration
- [ ] **Prepare integration point**
  - Ensure `tools/temperature-monitoring/` placeholder exists
  - Document integration pattern for future tools
  - Plan merge strategy with temperature monitoring branch

### 5.2 Establish Tool Organization Patterns
- [ ] **Document tool addition patterns**
  - Create guidelines for new tool placement
  - Document naming conventions
  - Establish integration testing requirements

## Strategic Goals Integration

### Goal 1: Prevent AI-Guided Development Degradation
**Implementation Strategy:**
- Create explicit organizational patterns and decision trees
- Document "where does X belong?" guidelines in `tools/README.md`
- Establish quality gates and review checklists
- Include structure preservation rules in contribution guidelines

**Success Metrics:**
- New AI-guided additions follow established patterns
- Repository structure remains clean after multiple development cycles
- Contributors can easily determine correct placement for new components

### Goal 2: Clarity for 3D Printer Owners (End Users)
**Implementation Strategy:**
- **Primary User Path**: Root README prioritizes "I just want firmware" workflow
- **Simplified Language**: Avoid technical jargon in user-facing documentation
- **Clear Decision Trees**: Hardware compatibility guides with simple questions
- **Visual Aids**: Include pictures and diagrams where helpful
- **Separate Technical Details**: Keep advanced information in developer sections

**Success Metrics:**
- Non-technical users can find and install firmware without confusion
- User documentation tested with actual 3D printer owners
- Support requests focus on hardware issues, not documentation confusion

### Goal 3: Developer Environment Documentation
**Implementation Strategy:**
- Comprehensive containerized environment documentation
- Platform-specific setup guides (Windows/Linux)
- Validation procedures and testing requirements
- Troubleshooting sections for common issues
- Both beginner and expert-level explanations

**Success Metrics:**
- New developers can set up environment following documentation alone
- Both novice and experienced developers find appropriate level of detail
- Development environment setup is consistently successful

### Goal 4: Dual-Audience Optimization
**Implementation Strategy:**
- **Layered Documentation**: Start simple, provide progressively more detail
- **Clear Audience Indicators**: Mark sections as "Users", "Developers", "Advanced"
- **Multiple Entry Points**: Different starting documents for different audiences
- **Cross-References**: Easy navigation between user and developer content
- **Plain English Summaries**: Technical concepts explained in accessible language

**Success Metrics:**
- Both technical and non-technical users report positive documentation experience
- Users don't feel overwhelmed by technical details they don't need
- Developers can find the technical depth they require
- Documentation feedback indicates successful dual-audience serving

## Documentation Strategy: Addressing the "Doomed to Fail" Challenge

### Multi-Layered Approach
1. **Surface Layer** (Root README): Simple, friendly, immediate value
2. **Functional Layer** (User/Developer docs): Task-focused, audience-specific
3. **Reference Layer** (Technical docs): Complete, detailed, searchable

### Language Strategy
- **User Documentation**: Plain English, avoid jargon, explain necessary terms
- **Developer Documentation**: Technical precision with beginner-friendly explanations
- **Reference Documentation**: Complete technical accuracy with cross-references

### Validation Strategy
- Test user documentation with actual 3D printer owners
- Test developer documentation with both novice and experienced programmers
- Collect feedback and iterate on documentation effectiveness

## Success Criteria

### Quantitative Metrics
- [ ] Root directory contains ≤10 files (currently ~15+)
- [ ] All build workflows pass with new structure
- [ ] All VS Code functionality works with new configuration
- [ ] All documentation links function correctly
- [ ] CI/CD pipelines pass with new structure

### Qualitative Metrics
- [ ] **End users can find and use firmware without technical expertise**
- [ ] **3D printer owners have clear path from "need firmware" to "working printer"**
- [ ] **Developers can set up environment following documentation**
- [ ] New contributors can easily understand project structure
- [ ] Platform-specific guidance eliminates user confusion
- [ ] Professional appearance matches modern open-source standards
- [ ] Tool organization supports future extensibility
- [ ] **AI-guided development maintains structural integrity**
- [ ] **Documentation serves both technical and non-technical audiences effectively**

## Risk Mitigation

### High Risk Items
- [ ] **VS Code configuration compatibility** - Test thoroughly, provide fallback
- [ ] **CI/CD pipeline disruption** - Test in separate branch, have rollback plan
- [ ] **Docker build path issues** - Validate all mount points and paths
- [ ] **Script cross-reference breakage** - Map all dependencies before moving

### Rollback Plan
- [ ] Keep original branch intact until validation complete
- [ ] Document all changes for easy reversal
- [ ] Test rollback procedure on copy of repository
- [ ] Prepare communication for contributors if rollback needed

## Post-Implementation Tasks

### Immediate Follow-up
- [ ] Update contributor documentation with new structure
- [ ] Create announcement explaining changes
- [ ] Monitor for issues and user feedback
- [ ] Update any external documentation referencing old structure

### Long-term Maintenance
- [ ] Establish patterns for future tool additions
- [ ] Regular review of directory organization effectiveness
- [ ] Update documentation as repository evolves
- [ ] Consider additional organizational improvements based on usage
