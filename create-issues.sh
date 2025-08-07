#!/bin/bash
# GitHub CLI Bulk Issue Creation Script
# Repository Restructuring Project - All Issues

set -e  # Exit on any error

echo "🚀 Creating all GitHub issues for Repository Restructuring project..."
echo "This will create issues, labels, and milestones using GitHub CLI"
echo ""

# Check if gh CLI is installed and authenticated
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed. Please install it first:"
    echo "   Linux: sudo apt install gh"
    echo "   macOS: brew install gh" 
    echo "   Windows: winget install GitHub.CLI"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI. Please run:"
    echo "   gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Create labels first
echo "📋 Creating labels..."

# Function to create label with better error handling
create_label() {
    local name="$1"
    local description="$2"
    local color="$3"
    
    echo "  Creating label: $name"
    if gh label create "$name" --description "$description" --color "$color" --force 2>/dev/null; then
        echo "    ✅ Created: $name"
    else
        echo "    ⚠️  Already exists or updated: $name"
    fi
}

create_label "restructuring" "Main project label" "0052CC"
create_label "phase-1" "Core structure creation" "1D76DB"
create_label "phase-2" "Tool integration" "0E8A16"
create_label "phase-3" "Documentation updates" "FBCA04"
create_label "phase-4" "Testing and validation" "D93F0B"
create_label "file-movement" "Tasks involving moving files" "C5DEF5"
create_label "configuration" "Tasks updating config files" "BFD4F2"
create_label "documentation" "Documentation-related tasks" "0E8A16"
create_label "build-tools" "Build script related tasks" "5319E7"
create_label "docker" "Docker-related tasks" "006B75"
create_label "testing" "Testing and validation tasks" "D93F0B"
create_label "high-priority" "Critical path items" "B60205"
create_label "windows" "Windows-specific tasks" "0052CC"
create_label "linux" "Linux-specific tasks" "0052CC"
create_label "vscode" "VS Code related tasks" "5319E7"

echo "✅ Labels created successfully"
echo ""

# Create milestones
echo "🎯 Creating milestones..."

# Note: Milestones need to be created via API since gh doesn't have direct milestone commands
REPO_OWNER=$(gh repo view --json owner --jq '.owner.login')
REPO_NAME=$(gh repo view --json name --jq '.name')

# Function to create milestone with better error handling
create_milestone() {
    local title="$1"
    local description="$2"
    
    echo "  Creating milestone: $title"
    if gh api repos/$REPO_OWNER/$REPO_NAME/milestones \
        --method POST \
        --field title="$title" \
        --field description="$description" \
        --silent 2>/dev/null; then
        echo "    ✅ Created: $title"
    else
        echo "    ⚠️  Already exists: $title"
    fi
}

create_milestone "Phase 1: Core Structure" "Create new directory structure and move files to organized locations. This phase establishes the foundation for the new repository organization by creating the docs/, tools/, .dev/, and build/ directories, then moving existing files to their appropriate new locations. Success criteria: All files moved, directory structure established, no broken functionality."

create_milestone "Phase 2: Tool Integration" "Update all configuration files and scripts to work with the new directory structure. This includes updating Docker Compose files, Makefiles, build scripts, and other tools to reference the correct file paths. All existing functionality must be preserved while using the new organization. Success criteria: All build processes work, no broken references, tools function correctly."

create_milestone "Phase 3: Documentation Updates" "Update all documentation to reflect the new repository structure and create user-focused documentation. This phase creates separate entry points for 3D printer owners vs developers, updates existing docs with new file paths, and establishes dual-audience documentation strategy. Success criteria: Clear user guidance, updated developer docs, all links functional."

create_milestone "Phase 4: Testing & Validation" "Comprehensive testing of the restructured repository to ensure all functionality works correctly. This includes testing Docker builds, PlatformIO compilation, VS Code integration, CI/CD pipelines, and documentation accuracy. All workflows must function identically to the original structure. Success criteria: All tests pass, performance maintained, no regressions."

create_milestone "Phase 5: Future Integration" "Prepare integration points for future tools and establish organizational patterns for ongoing development. This phase ensures the temperature-monitoring tool can be cleanly integrated and creates guidelines to prevent future repository degradation during AI-guided development. Success criteria: Integration patterns documented, structure extensible."

echo "✅ Milestones created successfully"
echo ""

# Create issues
echo "📝 Creating issues..."

# Phase 1 Issues
echo "  Creating Phase 1 issues..."

gh issue create \
  --title "Create docs/ directory structure" \
  --body "Create the new documentation directory structure as part of repository restructuring.

**Tasks:**
- [ ] Create \`docs/\` root directory
- [ ] Create \`docs/development/\` subdirectory  
- [ ] Create \`docs/hardware/\` subdirectory
- [ ] Add \`.gitkeep\` files to maintain empty directories

**Acceptance Criteria:**
- All directories exist
- Directory structure matches proposal
- Empty directories preserved with .gitkeep

**Estimate:** 1 story point" \
  --label "restructuring,documentation,phase-1" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Create tools/ directory structure" \
  --body "Create the new tools directory structure to organize build scripts and development utilities.

**Tasks:**
- [ ] Create \`tools/\` root directory
- [ ] Create \`tools/build/\` subdirectory
- [ ] Create \`tools/build/docker/\` subdirectory
- [ ] Create \`tools/scripts/\` subdirectory
- [ ] Create \`tools/scripts/powershell/\` subdirectory
- [ ] Create \`tools/scripts/linux/\` subdirectory
- [ ] Create \`tools/vscode/\` subdirectory
- [ ] Create \`tools/temperature-monitoring/\` placeholder

**Acceptance Criteria:**
- All directories exist
- Structure supports both Windows and Linux development
- Placeholder ready for future tool integration

**Estimate:** 2 story points" \
  --label "restructuring,build-tools,phase-1" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Create .dev/ directory structure" \
  --body "Create the new development environment configuration directory structure.

**Tasks:**
- [ ] Create \`.dev/\` root directory
- [ ] Create \`.dev/vscode/\` subdirectory
- [ ] Create \`.dev/github/\` subdirectory
- [ ] Add \`.gitkeep\` files to maintain empty directories

**Acceptance Criteria:**
- All directories exist
- Structure ready for development config files
- Empty directories preserved with .gitkeep

**Estimate:** 1 story point" \
  --label "restructuring,configuration,phase-1" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Create build/ directory" \
  --body "Create the build output directory and configure .gitignore.

**Tasks:**
- [ ] Create \`build/\` directory
- [ ] Add \`.gitkeep\` file
- [ ] Update \`.gitignore\` to handle build artifacts

**Acceptance Criteria:**
- Build directory exists
- .gitignore properly configured
- Directory preserved in git

**Estimate:** 1 story point" \
  --label "restructuring,configuration,phase-1" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move documentation files to docs/" \
  --body "Move all documentation files from root and docs/ to new organized structure.

**Tasks:**
- [ ] Move \`BUILD_AND_TEST.md\` from root to \`docs/BUILD_AND_TEST.md\`
- [ ] Move \`CHANGELOG_6.1_to_6.2.md\` from root to \`docs/CHANGELOG_6.1_to_6.2.md\`
- [ ] Move \`SECURITY.md\` from root to \`docs/SECURITY.md\`
- [ ] Move \`docs/Bresenham.md\` → \`docs/development/Bresenham.md\`
- [ ] Move \`docs/Queue.md\` → \`docs/development/Queue.md\`
- [ ] Move \`docs/Serial.md\` → \`docs/development/Serial.md\`

**Acceptance Criteria:**
- All files moved to correct locations
- No broken links within moved files
- Git history preserved for moved files

**Dependencies:** Create docs/ directory structure
**Estimate:** 3 story points" \
  --label "restructuring,documentation,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move build scripts to tools/build/" \
  --body "Move build-related scripts from root to organized tools directory.

**Tasks:**
- [ ] Move \`build-configs.sh\` → \`tools/build/build-configs.sh\`
- [ ] Move \`get_test_targets.py\` → \`tools/build/get_test_targets.py\`
- [ ] Update execute permissions on moved scripts
- [ ] Test script functionality after move

**Acceptance Criteria:**
- Scripts moved to correct location
- Execute permissions preserved
- Scripts function correctly from new location

**Dependencies:** Create tools/ directory structure
**Estimate:** 2 story points" \
  --label "restructuring,build-tools,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move Docker configuration to tools/build/docker/" \
  --body "Consolidate Docker-related files into organized tools structure.

**Tasks:**
- [ ] Move \`get-docker.sh\` → \`tools/build/docker/get-docker.sh\`
- [ ] Move \`docker-compose.yml\` → \`tools/build/docker/docker-compose.yml\`
- [ ] Move \`docker/Dockerfile\` → \`tools/build/docker/Dockerfile\`
- [ ] Move \`.env\` → \`tools/build/docker/.env\`
- [ ] Remove empty \`docker/\` directory

**Acceptance Criteria:**
- All Docker files in tools/build/docker/
- Docker Compose functionality preserved
- Old directory removed

**Dependencies:** Create tools/ directory structure
**Estimate:** 2 story points" \
  --label "restructuring,docker,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move PowerShell scripts to tools/scripts/powershell/" \
  --body "Move all PowerShell scripts to organized platform-specific directory.

**Tasks:**
- [ ] Move \`scripts/Common.ps1\` → \`tools/scripts/powershell/Common.ps1\`
- [ ] Move \`scripts/Generate-ConfigExample.ps1\` → \`tools/scripts/powershell/Generate-ConfigExample.ps1\`
- [ ] Move \`scripts/Invoke-PioBuild.ps1\` → \`tools/scripts/powershell/Invoke-PioBuild.ps1\`
- [ ] Move \`scripts/Join-UpstreamChanges.ps1\` → \`tools/scripts/powershell/Join-UpstreamChanges.ps1\`
- [ ] Move \`scripts/Run-ExampleConfigBuilds.ps1\` → \`tools/scripts/powershell/Run-ExampleConfigBuilds.ps1\`
- [ ] Move \`scripts/Update-ConfigExampleChanges.ps1\` → \`tools/scripts/powershell/Update-ConfigExampleChanges.ps1\`
- [ ] Move \`scripts/Update-ConfigExamples.ps1\` → \`tools/scripts/powershell/Update-ConfigExamples.ps1\`
- [ ] Move \`scripts/build-incl/\` → \`tools/scripts/powershell/build-incl/\`

**Acceptance Criteria:**
- All PowerShell scripts moved to new location
- Execute permissions preserved
- Scripts function correctly from new location

**Dependencies:** Create tools/ directory structure
**Estimate:** 2 story points" \
  --label "restructuring,windows,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move Linux scripts to tools/scripts/linux/" \
  --body "Move Linux-specific scripts to organized platform directory.

**Tasks:**
- [ ] Move \`run-powershell.sh\` → \`tools/scripts/linux/run-powershell.sh\`
- [ ] Update execute permissions on moved scripts
- [ ] Test script functionality after move

**Acceptance Criteria:**
- Scripts moved to correct location
- Execute permissions preserved
- Scripts function correctly from new location

**Dependencies:** Create tools/ directory structure
**Estimate:** 1 story point" \
  --label "restructuring,linux,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move VS Code tools to tools/vscode/" \
  --body "Move VS Code specific configuration files to tools directory.

**Tasks:**
- [ ] Move \`process-palette.json\` → \`tools/vscode/process-palette.json\`
- [ ] Move \`compile_commands.json\` → \`tools/vscode/compile_commands.json\`
- [ ] Test VS Code functionality after move

**Acceptance Criteria:**
- Files moved to correct location
- VS Code tools function correctly

**Dependencies:** Create tools/ directory structure
**Estimate:** 1 story point" \
  --label "restructuring,vscode,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move VS Code configuration to .dev/vscode/" \
  --body "Move VS Code development configuration to .dev directory.

**Tasks:**
- [ ] Move \`.vscode/c_cpp_properties.json\` → \`.dev/vscode/c_cpp_properties.json\`
- [ ] Move \`.vscode/extensions.json\` → \`.dev/vscode/extensions.json\`
- [ ] Move \`.vscode/launch.json\` → \`.dev/vscode/launch.json\`
- [ ] Move \`.vscode/settings.json\` → \`.dev/vscode/settings.json\`

**Acceptance Criteria:**
- All VS Code config files moved
- Configuration preserved

**Dependencies:** Create .dev/ directory structure
**Estimate:** 1 story point" \
  --label "restructuring,vscode,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Move GitHub configuration to .dev/github/" \
  --body "Move GitHub-specific configuration files to .dev directory.

**Tasks:**
- [ ] Move \`.github/ISSUE_TEMPLATE/\` → \`.dev/github/ISSUE_TEMPLATE/\`
- [ ] Move \`.github/workflows/\` → \`.dev/github/workflows/\`
- [ ] Move \`.github/code_of_conduct.md\` → \`.dev/github/code_of_conduct.md\`
- [ ] Move \`.github/issue_template.md\` → \`.dev/github/issue_template.md\`
- [ ] Move \`.github/pull_request_template.md\` → \`.dev/github/pull_request_template.md\`

**Acceptance Criteria:**
- All GitHub config files moved
- CI/CD workflows preserved

**Dependencies:** Create .dev/ directory structure
**Estimate:** 2 story points" \
  --label "restructuring,configuration,file-movement" \
  --milestone "Phase 1: Core Structure"

gh issue create \
  --title "Clean up old empty directories" \
  --body "Remove old empty directories after files have been moved.

**Tasks:**
- [ ] Remove \`scripts/\` directory (after files moved)
- [ ] Remove \`docker/\` directory (after files moved)
- [ ] Remove \`.vscode/\` directory (after files moved)
- [ ] Remove \`.github/\` directory (after files moved)

**Acceptance Criteria:**
- All old directories removed
- No broken references remain

**Dependencies:** All file movement tasks completed
**Estimate:** 1 story point" \
  --label "restructuring,file-movement" \
  --milestone "Phase 1: Core Structure"

# Phase 2 Issues
echo "  Creating Phase 2 issues..."

gh issue create \
  --title "Update Docker Compose file paths" \
  --body "Update docker-compose.yml to work from new location and reference correct paths.

**Tasks:**
- [ ] Update Dockerfile path reference in docker-compose.yml
- [ ] Update volume mount paths for new structure
- [ ] Update working directory references
- [ ] Test Docker build process with new paths

**Acceptance Criteria:**
- Docker Compose builds successfully
- All volume mounts work correctly
- Container functionality unchanged

**Dependencies:** Move Docker configuration to tools/build/docker/
**Estimate:** 3 story points" \
  --label "restructuring,docker,configuration" \
  --milestone "Phase 2: Tool Integration"

gh issue create \
  --title "Update Makefile references" \
  --body "Update Makefile to use new paths for Docker and build scripts.

**Tasks:**
- [ ] Update path to Docker Compose file
- [ ] Update paths to build scripts
- [ ] Update any hardcoded directory references
- [ ] Test all make targets

**Acceptance Criteria:**
- All make targets work with new structure
- No hardcoded paths to moved files
- Build process unchanged

**Dependencies:** Move Docker configuration, Move build scripts
**Estimate:** 2 story points" \
  --label "restructuring,configuration" \
  --milestone "Phase 2: Tool Integration"

gh issue create \
  --title "Update build scripts references" \
  --body "Update build scripts to work with new directory structure.

**Tasks:**
- [ ] Update \`tools/build/build-configs.sh\` Docker Compose references
- [ ] Update \`tools/build/get_test_targets.py\` workflow path references
- [ ] Update any hardcoded paths in scripts
- [ ] Test script execution

**Acceptance Criteria:**
- All scripts work with new structure
- No broken path references
- Script functionality unchanged

**Dependencies:** Move build scripts, Move GitHub configuration
**Estimate:** 2 story points" \
  --label "restructuring,build-tools,configuration" \
  --milestone "Phase 2: Tool Integration"

gh issue create \
  --title "Update PowerShell script cross-references" \
  --body "Update PowerShell scripts to work with new directory structure.

**Tasks:**
- [ ] Update imports/includes between PowerShell scripts
- [ ] Update any hardcoded paths to repository files
- [ ] Test PowerShell script execution
- [ ] Update script documentation

**Acceptance Criteria:**
- All PowerShell scripts work with new structure
- Script cross-references functional
- No broken path references

**Dependencies:** Move PowerShell scripts
**Estimate:** 2 story points" \
  --label "restructuring,windows,configuration" \
  --milestone "Phase 2: Tool Integration"

gh issue create \
  --title "Create VS Code configuration bridge" \
  --body "Create new .vscode/ directory that references .dev/ configuration.

**Tasks:**
- [ ] Create new \`.vscode/\` directory
- [ ] Create \`.vscode/settings.json\` with references to \`.dev/vscode/\`
- [ ] Test VS Code functionality
- [ ] Document configuration approach

**Acceptance Criteria:**
- VS Code works with new configuration structure
- Development environment functional
- Configuration approach documented

**Dependencies:** Move VS Code configuration
**Estimate:** 2 story points" \
  --label "restructuring,vscode,configuration" \
  --milestone "Phase 2: Tool Integration"

gh issue create \
  --title "Create GitHub configuration bridge" \
  --body "Create new .github/ directory structure that works with .dev/ location.

**Tasks:**
- [ ] Create new \`.github/\` directory structure
- [ ] Create symlinks or copies referencing \`.dev/github/\`
- [ ] Test CI/CD pipeline functionality
- [ ] Update workflow paths if needed

**Acceptance Criteria:**
- GitHub Actions work with new structure
- CI/CD pipelines functional
- Workflow references updated

**Dependencies:** Move GitHub configuration
**Estimate:** 3 story points" \
  --label "restructuring,configuration,high-priority" \
  --milestone "Phase 2: Tool Integration"

# Phase 3 Issues
echo "  Creating Phase 3 issues..."

gh issue create \
  --title "Update main README with dual-audience approach" \
  --body "Update root README.md to serve both 3D printer owners and developers.

**Tasks:**
- [ ] **PRIMARY SECTION**: Clear path for 3D printer owners
  - \"I just want firmware\" quick start
  - Download links and basic flashing instructions
  - Hardware compatibility checker
  - Common troubleshooting (friendly language)
- [ ] **SECONDARY SECTION**: Developer and contributor information
  - Link to detailed build documentation
  - Repository structure explanation
  - Contribution guidelines
- [ ] **TERTIARY SECTION**: Repository organization (for reference)

**Acceptance Criteria:**
- README serves both user types effectively
- All links work correctly
- New users can follow setup instructions
- Professional appearance maintained

**Dependencies:** Move documentation files
**Estimate:** 4 story points" \
  --label "restructuring,documentation,high-priority" \
  --milestone "Phase 3: Documentation Updates"

gh issue create \
  --title "Create USERS_START_HERE.md documentation" \
  --body "Create primary user documentation for 3D printer owners.

**Tasks:**
- [ ] **\"I Just Want Firmware\"** section with download links
- [ ] **Hardware Compatibility Guide** with simple decision tree
- [ ] **Flashing Instructions** with pictures and simple language
- [ ] **Basic Configuration** for common modifications
- [ ] **Troubleshooting** in plain English
- [ ] **When to Ask for Help** and community support info

**Acceptance Criteria:**
- Non-technical users can successfully use firmware
- Simple, jargon-free language throughout
- Clear decision trees for hardware compatibility
- Troubleshooting covers common issues

**Dependencies:** Move documentation files
**Estimate:** 5 story points" \
  --label "restructuring,documentation,high-priority" \
  --milestone "Phase 3: Documentation Updates"

gh issue create \
  --title "Create DEVELOPERS_START_HERE.md documentation" \
  --body "Create developer-focused documentation and onboarding guide.

**Tasks:**
- [ ] **Development Environment Setup** (Docker, VS Code, etc.)
- [ ] **Repository Structure Guide** explaining new organization
- [ ] **Contribution Workflow** and coding standards
- [ ] **Testing Requirements** and validation procedures
- [ ] **Advanced Configuration** and customization

**Acceptance Criteria:**
- Developers can set up environment following docs alone
- Both novice and experienced developers find appropriate detail
- Contribution process clearly documented
- Testing procedures comprehensive

**Dependencies:** Move documentation files
**Estimate:** 4 story points" \
  --label "restructuring,documentation" \
  --milestone "Phase 3: Documentation Updates"

gh issue create \
  --title "Update BUILD_AND_TEST.md for new structure" \
  --body "Update build documentation to reflect new directory structure.

**Tasks:**
- [ ] Update all script paths to new locations
- [ ] Update Docker setup instructions with new paths
- [ ] Update examples with new directory structure
- [ ] Add troubleshooting for development environment
- [ ] Include beginner-friendly explanations alongside technical details

**Acceptance Criteria:**
- All build instructions work with new structure
- Docker setup functional
- Examples use correct paths
- Both novice and expert developers can follow

**Dependencies:** Move documentation files, Phase 2 completion
**Estimate:** 3 story points" \
  --label "restructuring,documentation,build-tools" \
  --milestone "Phase 3: Documentation Updates"

gh issue create \
  --title "Create AI Development Guidelines" \
  --body "Create guidelines to prevent AI-guided development degradation.

**Tasks:**
- [ ] **Structure Preservation Rules** for AI-guided development
- [ ] **File Placement Decision Trees** (\"Where should this go?\")
- [ ] **Naming Conventions** and organizational patterns
- [ ] **Quality Gates** to prevent degradation
- [ ] **Review Checklist** for AI-generated additions

**Acceptance Criteria:**
- Clear rules for maintaining repository structure
- Decision trees for file placement
- Quality gates prevent degradation
- Review process documented

**Estimate:** 3 story points" \
  --label "restructuring,documentation" \
  --milestone "Phase 3: Documentation Updates"

gh issue create \
  --title "Create tools/ directory documentation" \
  --body "Document the tools directory organization and usage.

**Tasks:**
- [ ] Create \`tools/README.md\` with organization guide
- [ ] Document how to add new tools without degrading structure
- [ ] Include \"where does my new tool belong?\" decision tree
- [ ] Create \`tools/scripts/powershell/README.md\` (Windows)
- [ ] Create \`tools/scripts/linux/README.md\` (Linux)
- [ ] Document platform-specific setup and usage

**Acceptance Criteria:**
- Tools directory purpose clearly explained
- Platform-specific guidance available
- New tool placement patterns documented
- Setup instructions for both platforms

**Dependencies:** Move files to tools/
**Estimate:** 3 story points" \
  --label "restructuring,documentation" \
  --milestone "Phase 3: Documentation Updates"

gh issue create \
  --title "Create migration guide for existing contributors" \
  --body "Create comprehensive migration guide for existing contributors.

**Tasks:**
- [ ] Document what changed and where things moved
- [ ] Provide command-line helpers for finding moved files
- [ ] Add troubleshooting for common migration issues
- [ ] Include \"before and after\" directory structure comparison
- [ ] Add transition timeline and deprecation notices

**Acceptance Criteria:**
- Existing contributors understand all changes
- Command-line helpers work correctly
- Troubleshooting covers common issues
- Transition process clearly documented

**Dependencies:** All file movements completed
**Estimate:** 2 story points" \
  --label "restructuring,documentation" \
  --milestone "Phase 3: Documentation Updates"

# Phase 4 Issues
echo "  Creating Phase 4 issues..."

gh issue create \
  --title "Validate Docker-based build process" \
  --body "Comprehensive testing of Docker build process with new file structure.

**Tasks:**
- [ ] Test Docker Compose build with new paths
- [ ] Test all Docker build configurations
- [ ] Validate build output locations
- [ ] Test volume mounts and file access
- [ ] Test build script execution in container

**Acceptance Criteria:**
- All Docker builds pass
- Build outputs in correct locations
- No path-related errors
- Performance unchanged

**Dependencies:** Update Docker Compose file paths, Update build scripts
**Estimate:** 5 story points" \
  --label "restructuring,testing,docker" \
  --milestone "Phase 4: Testing & Validation"

gh issue create \
  --title "Validate PlatformIO builds and VS Code integration" \
  --body "Test PlatformIO build system and VS Code development environment.

**Tasks:**
- [ ] Verify VS Code integration still works
- [ ] Test command-line PlatformIO builds
- [ ] Validate all target platforms
- [ ] Test debugging and IntelliSense
- [ ] Validate Process Palette commands

**Acceptance Criteria:**
- All PlatformIO builds successful
- VS Code integration functional
- All target platforms work
- Development experience maintained

**Dependencies:** VS Code configuration updates
**Estimate:** 4 story points" \
  --label "restructuring,testing,vscode" \
  --milestone "Phase 4: Testing & Validation"

gh issue create \
  --title "Validate CI/CD pipelines" \
  --body "Test GitHub Actions and CI/CD functionality with new structure.

**Tasks:**
- [ ] Verify GitHub Actions work with new structure
- [ ] Test all build matrix configurations
- [ ] Validate artifact generation
- [ ] Test workflow triggers
- [ ] Validate deployment processes

**Acceptance Criteria:**
- All GitHub Actions pass
- Build matrix works correctly
- Artifacts generated properly
- Deployment processes functional

**Dependencies:** GitHub configuration bridge
**Estimate:** 4 story points" \
  --label "restructuring,testing,configuration" \
  --milestone "Phase 4: Testing & Validation"

gh issue create \
  --title "Test build scripts functionality" \
  --body "Validate all build scripts work correctly with new structure.

**Tasks:**
- [ ] Test \`tools/build/build-configs.sh\` on Linux
- [ ] Test PowerShell scripts on Windows (if available)
- [ ] Validate script cross-references work
- [ ] Test script error handling
- [ ] Validate output generation

**Acceptance Criteria:**
- All build scripts functional
- Cross-references work correctly
- Error handling preserved
- Output generation works

**Dependencies:** Build script updates
**Estimate:** 3 story points" \
  --label "restructuring,testing,build-tools" \
  --milestone "Phase 4: Testing & Validation"

gh issue create \
  --title "Validate documentation accuracy" \
  --body "Test all documentation links and instructions.

**Tasks:**
- [ ] Verify internal links work with new structure
- [ ] Test external links still function
- [ ] Validate code examples and paths
- [ ] Test onboarding process with new contributors
- [ ] Verify platform-specific guidance

**Acceptance Criteria:**
- All documentation links functional
- Code examples work correctly
- Onboarding process smooth
- Platform guidance accurate

**Dependencies:** Documentation updates completed
**Estimate:** 3 story points" \
  --label "restructuring,testing,documentation" \
  --milestone "Phase 4: Testing & Validation"

# Phase 5 Issues
echo "  Creating Phase 5 issues..."

gh issue create \
  --title "Prepare temperature monitoring tool integration" \
  --body "Prepare integration point for temperature monitoring tool.

**Tasks:**
- [ ] Ensure \`tools/temperature-monitoring/\` placeholder exists
- [ ] Document integration pattern for future tools
- [ ] Plan merge strategy with temperature monitoring branch
- [ ] Create integration documentation
- [ ] Test integration workflow

**Acceptance Criteria:**
- Integration point ready
- Documentation complete
- Merge strategy planned
- Integration workflow tested

**Estimate:** 2 story points" \
  --label "restructuring,configuration" \
  --milestone "Phase 5: Future Integration"

gh issue create \
  --title "Establish tool organization patterns" \
  --body "Document patterns for adding new tools and maintaining structure.

**Tasks:**
- [ ] Create guidelines for new tool placement
- [ ] Document naming conventions
- [ ] Establish integration testing requirements
- [ ] Create tool addition checklist
- [ ] Document structure maintenance procedures

**Acceptance Criteria:**
- Tool addition patterns documented
- Naming conventions established
- Testing requirements clear
- Maintenance procedures documented

**Estimate:** 3 story points" \
  --label "restructuring,documentation" \
  --milestone "Phase 5: Future Integration"

echo ""
echo "✅ All issues created successfully!"
echo ""
echo "📊 Summary:"
echo "   - 15 labels created"
echo "   - 5 milestones created"
echo "   - 25+ issues created across all phases"
echo ""
echo "🎯 Next steps:"
echo "   1. Go to your GitHub repository Issues tab"
echo "   2. Review and organize issues in your Project board"
echo "   3. Start with Phase 1 issues"
echo "   4. Begin implementation!"
echo ""
echo "🚀 Happy restructuring!"
