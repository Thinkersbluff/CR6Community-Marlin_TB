# Plan for Splitting Help Documentation: JUST_BUILD vs DEVELOPER

## 1. Audience Definitions

### JUST_BUILD_SETUP_*
For users who only want to build a firmware.bin file for their printer using the provided GUI tool.
- No prior experience with Git, GitHub, VSCode, or command-line tools.
- Needs simple, step-by-step, jargon-free instructions.
- Only needs to know how to launch the GUI, select options, and copy the resulting firmware.bin to an SD card.

### DEVELOPERS_SETUP_*
For users who want to modify, configure, or contribute to the repository and firmware.
- Comfortable with GitHub, VSCode, and basic development tools.
- May want to fork, branch, or submit PRs.
- Needs to know about build scripts, containerization, advanced troubleshooting, and configuration management.

---

## 2. Document Structure Proposal

For each OS (Linux, macOS, Windows), create:
- `JUST_BUILD_SETUP_<OS>.md`
- `DEVELOPERS_SETUP_<OS>.md`

---

## 3. Content Division

### JUST_BUILD_SETUP_<OS>.md
**Should include:**
- What the tool does (builds firmware for your printer)
- Where to find the GUI tool (python/tkinter app)
- How to launch the GUI tool (double-click, or simple command if needed)
- How to use the GUI (step-by-step, with screenshots if possible)
- Where to find the output firmware.bin
- How to copy firmware.bin to SD card and flash the printer
- Basic troubleshooting (e.g., “I don’t see the GUI”, “No firmware.bin produced”)
- Platform-specific:
  - How to install Python (if needed)
  - How to install Tkinter (if not bundled)
  - How to run the tool on each OS (double-click, right-click, or terminal command)
  - Any OS-specific quirks (e.g., Gatekeeper on macOS, SmartScreen on Windows)

**Should NOT include:**
- Git/GitHub instructions
- VSCode or PlatformIO setup
- Containerization (Docker/Podman)
- Build scripts or Makefiles
- Advanced troubleshooting or developer workflows

---

### DEVELOPERS_SETUP_<OS>.md
**Should include:**
- How to clone/fork the repository
- How to set up VSCode and PlatformIO (if used)
- How to use build scripts, Makefiles, or containerized environments (Docker/Podman)
- How to run tests, manage configs, and contribute changes
- How to use advanced tools (e.g., command-line PlatformIO, CI, custom scripts)
- How to manage permissions, troubleshoot builds, and fix common developer issues
- Platform-specific:
  - Container engine setup (Docker/Podman/WSL2)
  - Any OS-specific developer tips or caveats

**Should NOT include:**
- GUI-only instructions for the python/tkinter tool (except perhaps a brief mention for completeness)
- Step-by-step “copy firmware to SD card” instructions (unless relevant for developer testing)

---

## 4. Example Division for macOS

### JUST_BUILD_SETUP_macOS.md
- Introduction: “This guide helps you build firmware for your printer using our easy GUI tool.”
- Step 1: Install Python 3 (with Tkinter)
- Step 2: Download or locate the GUI tool
- Step 3: How to launch the GUI (double-click or `python3 configurator.py`)
- Step 4: How to use the GUI (select printer, options, build)
- Step 5: Where to find firmware.bin
- Step 6: How to copy firmware.bin to SD card and flash printer
- Troubleshooting: “GUI won’t open”, “No firmware.bin”, “Permission denied”
- Platform-specific notes: Gatekeeper, permissions

### DEVELOPERS_SETUP_macOS.md
- Introduction: “This guide is for developers who want to modify, build, or contribute to the firmware.”
- Step 1: Clone/fork the repo (with GitHub instructions)
- Step 2: Install VSCode, PlatformIO, and/or Podman
- Step 3: How to use build scripts, Makefiles, or containers
- Step 4: How to run tests, manage configs, and contribute changes
- Step 5: Advanced troubleshooting, permissions, and CI
- Platform-specific notes: Podman setup, file permissions, Xcode CLI tools

---

## 5. How to Proceed

### A. Review your current `docs/HELP` files.
- Identify sections that are GUI-only, beginner-friendly, or firmware flashing related → move to JUST_BUILD_SETUP_*
- Identify sections that are about repo management, scripts, containers, or developer workflows → move to DEVELOPERS_SETUP_*

### B. Create new files:
- `JUST_BUILD_SETUP_Windows.md`
- `JUST_BUILD_SETUP_macOS.md`
- `JUST_BUILD_SETUP_Linux.md`
- `DEVELOPERS_SETUP_Windows.md`
- `DEVELOPERS_SETUP_macOS.md`
- `DEVELOPERS_SETUP_Linux.md`

### C. Remove or reword content as needed:
- Remove developer content from JUST_BUILD docs.
- Remove GUI/flashing-only content from DEVELOPER docs (except for brief references).

---

## 6. Platform-Specific Advice

- **Windows:**  
  - Emphasize Python/Tkinter install, running GUI by double-click, and SD card formatting.
  - Warn about mapped network drives and Docker Desktop file sharing (for developers).
- **macOS:**  
  - Gatekeeper and permissions for running Python scripts.
  - Homebrew for Python/Podman.
- **Linux:**  
  - Package manager commands for Python/Tkinter.
  - Podman install and permissions.

---

## 7. Summary Table

| Document                      | Audience      | Content Focus                                      |
|-------------------------------|--------------|----------------------------------------------------|
| JUST_BUILD_SETUP_Windows.md    | End-user     | GUI tool, Python, SD card, basic troubleshooting   |
| JUST_BUILD_SETUP_macOS.md      | End-user     | GUI tool, Python, SD card, Gatekeeper, troubleshooting |
| JUST_BUILD_SETUP_Linux.md      | End-user     | GUI tool, Python, SD card, troubleshooting         |
| DEVELOPERS_SETUP_Windows.md    | Developer    | Git, VSCode, PlatformIO, Docker, scripts, CI       |
| DEVELOPERS_SETUP_macOS.md      | Developer    | Git, VSCode, PlatformIO, Podman, scripts, CI       |
| DEVELOPERS_SETUP_Linux.md      | Developer    | Git, VSCode, PlatformIO, Podman, scripts, CI       |

---

## 8. Next Steps

- Extract and rewrite content from current docs into the new structure.
- Remove or reword content as needed for each audience.
- Add platform-specific advice where necessary.

---

*Let the maintainers know if you want a sample outline or draft for any of these new files!*