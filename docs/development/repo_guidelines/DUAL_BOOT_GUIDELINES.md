# Dual-Boot System Guidelines

If you use both Linux and Windows on the same computer (dual-boot):

- **Keep separate clones:**
    - Clone the repository to a Windows-accessible drive for Windows development.
    - Clone the repository to a Linux partition for Linux development.
    - Do not use the same physical folder or partition for both OSes.

- **Avoid shared working directories:**
    - Do not point both OSes to the same folder, even if it is on a shared or network drive.
    - This prevents file permission conflicts and Docker-related issues.

- **Sync changes via Git:**
    - Make changes on one OS, push to GitHub, and pull those changes into your other OS.
    - This keeps your work in sync and avoids cross-platform permission problems.

- **Docker builds:**
    - Run Docker builds only in the environment matching your clone (Linux or Windows).
    - Each OS will handle file permissions and user mapping correctly in its own clone.

**Summary:**
Always use separate clones for Linux and Windows, and sync via Git. Never share the same working directory between OSes for Docker-based builds.
