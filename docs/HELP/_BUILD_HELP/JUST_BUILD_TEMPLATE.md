# Quick Start: Build Your Own Firmware (for <OS Name>)

This guide will help you create a custom firmware file for your 3D printer using our easy-to-use tool.  
**No programming or GitHub experience required!**

---

## 1. What You Need

- A computer running <OS Name> (e.g., Windows 10/11, macOS, or Linux)
- An SD card and SD card reader
- [Optional] Internet access to download Python (if not already installed)

---

## 2. Install Python (if needed)

- Download Python 3.x from [python.org](https://www.python.org/downloads/).
- During installation, make sure to check the box: **"Add Python to PATH"** (Windows only).
- On macOS: You may already have Python 3. If not, install it using [Homebrew](https://brew.sh/) or download from python.org.
- On Linux: Use your package manager (e.g., `sudo apt install python3 python3-tk`).

---

## 3. Download the Firmware Tool

- Locate or download the `configurator.py` tool from the project’s releases or repository.
- Place it in a folder you can easily find (e.g., your Desktop or Documents).

---

## 4. Launch the Firmware Tool

- **Windows:** Double-click `configurator.py` (or right-click and choose "Open with Python").
- **macOS/Linux:** Open a terminal, navigate to the folder, and run:
  ```sh
  python3 configurator.py
  ```
- If you see a security warning, allow the app to run (see Troubleshooting below).

---

## 5. Use the Tool to Build Firmware

1. Select your printer model from the list.
2. Choose any options or settings you want to change.
3. Click the **Build** button.
4. Wait for the process to finish. The tool will tell you where your new `firmware.bin` file is saved.

---

## 6. Flash the Firmware to Your Printer

1. Insert your SD card into your computer.
2. Copy the `firmware.bin` file to the root of the SD card.
3. Safely eject the SD card.
4. Insert the SD card into your printer and power it on.
5. Wait for the update to complete (follow your printer’s instructions).

---

## 7. Troubleshooting

- **The tool won’t open:**  
  Make sure Python 3 and Tkinter are installed. Try running from a terminal/command prompt.
- **No firmware.bin file is created:**  
  Check for error messages in the tool. Make sure you have write permissions to the folder.
- **Security warning (macOS):**  
  Go to System Preferences > Security & Privacy and allow the app to run.
- **Other issues:**  
  See the [FAQ](../FAQ.md) or ask for help on the community forum.

---

## 8. Need More Help?

- See the [FAQ](../FAQ.md)
- Visit the [community support forum](https://community.cr6.com)
- Contact the project maintainers

---

*Happy printing!*
