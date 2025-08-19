# Dual-Boot System Guidelines


If you use both Linux and Windows (or macOS and Windows) on the same computer (dual-boot) to maintain this repository:

- **Keep separate clones:**
    - Clone the repository to a Windows-accessible drive for Windows development.
    - Clone the repository to a Linux/macOS partition for Linux/macOS development.
    - Do not use the same physical folder or partition for both OSes.

- **Avoid shared working directories:**
    - Do not point both OSes to the same folder, even if it is on a shared or network drive (NTFS, exFAT, etc).
    - This prevents file permission conflicts, line ending issues, and Podman-related problems.
    - Linux/macOS and Windows handle file permissions, hidden files, and metadata differently.

- **Sync changes via Git:**
    - Make changes on one OS, push to GitHub, and pull those changes into your other OS.
    - This keeps your work in sync and avoids cross-platform permission problems.

- **Line endings:**
    - Consider using a `.gitattributes` file to enforce consistent line endings (e.g., `* text=auto`).
    - This helps prevent issues when switching between Windows (CRLF) and Linux/macOS (LF).

- **Podman builds:**
    - Run Podman builds only in the environment matching your clone (Linux, macOS, or Windows).
    - Each OS will handle file permissions and user mapping correctly in its own clone.
    - Podman/containers may not work correctly with NTFS/exFAT mounts due to permission limitations.

- **macOS-specific note:**
    - Use APFS or HFS+ partitions for your macOS clone, not NTFS/FAT32.

**Summary:**
Always use separate clones for Linux/macOS and Windows, and sync via Git. Never share the same working directory between OSes for Podman-based builds or development.
