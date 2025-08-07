# GitHub Issues for Repository Restructuring

## Issue Templates (Copy-Paste Ready)

### Core Structure Issues

```markdown
**Title:** Create docs/ directory structure

**Description:**
Create the new documentation directory structure as part of repository restructuring.

**Tasks:**
- [ ] Create `docs/` root directory
- [ ] Create `docs/development/` subdirectory  
- [ ] Create `docs/hardware/` subdirectory
- [ ] Add `.gitkeep` files to maintain empty directories

**Acceptance Criteria:**
- All directories exist
- Directory structure matches proposal
- Empty directories preserved with .gitkeep

**Labels:** restructuring, documentation, phase-1
**Milestone:** Phase 1: Core Structure
**Estimate:** 1 story point
```

```markdown
**Title:** Create tools/ directory structure

**Description:**
Create the new tools directory structure to organize build scripts and development utilities.

**Tasks:**
- [ ] Create `tools/` root directory
- [ ] Create `tools/build/` subdirectory
- [ ] Create `tools/build/docker/` subdirectory
- [ ] Create `tools/scripts/` subdirectory
- [ ] Create `tools/scripts/powershell/` subdirectory
- [ ] Create `tools/scripts/linux/` subdirectory
- [ ] Create `tools/vscode/` subdirectory
- [ ] Create `tools/temperature-monitoring/` placeholder

**Acceptance Criteria:**
- All directories exist
- Structure supports both Windows and Linux development
- Placeholder ready for future tool integration

**Labels:** restructuring, tools, phase-1
**Milestone:** Phase 1: Core Structure
**Estimate:** 2 story points
```

```markdown
**Title:** Move documentation files to docs/

**Description:**
Move all documentation files from root and docs/ to new organized structure.

**Tasks:**
- [ ] Move `BUILD_AND_TEST.md` from root to `docs/development/repo_guidelines/BUILD_AND_TEST.md`
- [ ] Move `CHANGELOG_6.1_to_6.2.md` from root to `docs/project/release_6.2/CHANGELOG_6.1_to_6.2.md`
- [ ] Move `SECURITY.md` from root to `docs/development/repo_guidelines/SECURITY.md`
- [ ] Move `docs/Bresenham.md` → `docs/development/Marlin FAQ/Bresenham.md`
- [ ] Move `docs/Queue.md` → `docs/development/Marlin FAQ/Queue.md`
- [ ] Move `docs/Serial.md` → `docs/development/Marlin FAQ/Serial.md`

**Acceptance Criteria:**
- All files moved to correct locations
- No broken links within moved files
- Git history preserved for moved files

**Labels:** restructuring, documentation, file-movement
**Milestone:** Phase 1: Core Structure
**Estimate:** 3 story points
**Dependencies:** Create docs/ directory structure
```

```markdown
**Title:** Move build scripts to tools/build/

**Description:**
Move build-related scripts from root to organized tools directory.

**Tasks:**
- [ ] Move `build-configs.sh` → `tools/build/build-configs.sh`
- [ ] Move `get_test_targets.py` → `tools/build/get_test_targets.py`
- [ ] Update execute permissions on moved scripts
- [ ] Test script functionality after move

**Acceptance Criteria:**
- Scripts moved to correct location
- Execute permissions preserved
- Scripts function correctly from new location

**Labels:** restructuring, build-tools, file-movement
**Milestone:** Phase 1: Core Structure
**Estimate:** 2 story points
**Dependencies:** Create tools/ directory structure
```

```markdown
**Title:** Move Docker configuration to tools/build/docker/

**Description:**
Consolidate Docker-related files into organized tools structure.

**Tasks:**
- [ ] Move `get-docker.sh` → `tools/build/docker/get-docker.sh`
- [ ] Move `docker-compose.yml` → `tools/build/docker/docker-compose.yml`
- [ ] Move `docker/Dockerfile` → `tools/build/docker/Dockerfile`
- [ ] Move `.env` → `tools/build/docker/.env`
- [ ] Remove empty `docker/` directory

**Acceptance Criteria:**
- All Docker files in tools/build/docker/
- Docker Compose functionality preserved
- Old directory removed

**Labels:** restructuring, docker, file-movement
**Milestone:** Phase 1: Core Structure
**Estimate:** 2 story points
**Dependencies:** Create tools/ directory structure
```

### Configuration Update Issues

```markdown
**Title:** Update Docker Compose file paths

**Description:**
Update docker-compose.yml to work from new location and reference correct paths.

**Tasks:**
- [ ] Update Dockerfile path reference in docker-compose.yml
- [ ] Update volume mount paths for new structure
- [ ] Update working directory references
- [ ] Test Docker build process with new paths

**Acceptance Criteria:**
- Docker Compose builds successfully
- All volume mounts work correctly
- Container functionality unchanged

**Labels:** restructuring, docker, configuration, phase-2
**Milestone:** Phase 2: Tool Integration
**Estimate:** 3 story points
**Dependencies:** Move Docker configuration to tools/build/docker/
```

```markdown
**Title:** Update Makefile references

**Description:**
Update Makefile to use new paths for Docker and build scripts.

**Tasks:**
- [ ] Update path to Docker Compose file
- [ ] Update paths to build scripts
- [ ] Update any hardcoded directory references
- [ ] Test all make targets

**Acceptance Criteria:**
- All make targets work with new structure
- No hardcoded paths to moved files
- Build process unchanged

**Labels:** restructuring, makefile, configuration, phase-2
**Milestone:** Phase 2: Tool Integration
**Estimate:** 2 story points
**Dependencies:** Move Docker configuration, Move build scripts
```

### Testing Issues

```markdown
**Title:** Validate Docker-based build process

**Description:**
Comprehensive testing of Docker build process with new file structure.

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

**Labels:** restructuring, testing, docker, phase-4
**Milestone:** Phase 4: Testing and Validation
**Estimate:** 5 story points
**Dependencies:** Update Docker Compose file paths, Update build scripts
```

### Documentation Issues

```markdown
**Title:** Update main README with new structure

**Description:**
Update root README.md to reflect new repository organization.

**Tasks:**
- [ ] Add section explaining new repository structure
- [ ] Update links to documentation (now in docs/)
- [ ] Update quick start instructions with new paths
- [ ] Add migration guide for existing contributors

**Acceptance Criteria:**
- README reflects new structure
- All links work correctly
- New users can follow setup instructions
- Existing users understand changes

**Labels:** restructuring, documentation, readme, phase-3
**Milestone:** Phase 3: Documentation Updates
**Estimate:** 3 story points
**Dependencies:** Move documentation files
```

## Project Labels

```
restructuring - Main project label
phase-1 - Core structure creation
phase-2 - Tool integration
phase-3 - Documentation updates  
phase-4 - Testing and validation
file-movement - Tasks involving moving files
configuration - Tasks updating config files
documentation - Documentation-related tasks
build-tools - Build script related tasks
docker - Docker-related tasks
testing - Testing and validation tasks
high-priority - Critical path items
windows - Windows-specific tasks
linux - Linux-specific tasks
vscode - VS Code related tasks
```

## Project Milestones

```
Phase 1: Core Structure - Create new directories and move files
Phase 2: Tool Integration - Update configurations and references
Phase 3: Documentation - Update all documentation  
Phase 4: Testing & Validation - Comprehensive testing
Phase 5: Future Integration - Prepare for additional tools
```

## Custom Fields for GitHub Project

```
Priority: High/Medium/Low
Complexity: 1-5 story points  
Platform: Windows/Linux/Both
Category: Structure/Config/Docs/Testing
Status: Todo/In Progress/Review/Done
Phase: 1/2/3/4/5
```
