# Quick Start: Build Your Own Firmware (for <Windows (10, 11))

This guide will help you create a custom firmware file for your 3D printer(s), using our easy-to-use Configurator tool.  
**No programming or GitHub experience required!**

---

## 1. What You Need

- A computer running Windows 10 or 11, Python, and Platformio
- A copy (a.k.a "clone") of the repository (see step#2)
- An SD card and SD card reader
- Internet access

---

## 2. "Download ZIP" the Repository to a Local Hard Drive

- Go to: [github.com/Thinkersbluff/CR6Community-Marlin_TB](https://github.com/Thinkersbluff/CR6Community-Marlin_TB)
- Click the green Code button
- Select Download ZIP
- Open your Downloads folder
- Right-click the file CR6Community-Marlin_TB-main.zip → choose Extract All…
- Choose where you want to keep the project (e.g., D:\Firmware)
- Open the folder: CR6Community-Marlin_TB-main\tools\configurator

---

## 3. Install Python (if not already installed)

- Download Python 3.x from [python.org](https://www.python.org/downloads/).
- During installation, make sure to check the box: **"Add Python to PATH"** (Windows only).

---

## 4. Install the Platformio Client Tool

This is the tool that actually builds your firmware.bin file.

- Go to [platformio.org](https://platformio.org/install/cli) and follow the instructions for Windows to install the PlatformIO Core (CLI) tool.

**NOTE:** You do NOT need the full PlatformIO IDE—just the command-line tool (Core).

If you have trouble, see the troubleshooting tips on the PlatformIO website.
---

## 5. Launch the Configurator Application
Either:

Double-click `configurator.py` 

OR: 

Open a terminal window (WindowsKey+R, type cmd, press Enter)
In the terminal window, navigate to the root folder of your copy of the repository.
Then, in the window, enter:

```
cd ./tools/configurator
python configurator.py
```

The Configurator application should open on your screen.
 - If it does not, see Troubleshooting, below.
 - If it does, proceed to step 6.

---

## 6. Use the Tool to Build Firmware

1. Read-through the process checklist displayed in the app.
2. [Optionally] Tick the boxes as you work your way through the process.
3. Select your (target) printer model from the list.
4. Verify that the Platformio.ini default environment text is green.  
  If, instead, the text is red: 
      1. Click the button **copy env to platformio.ini**. 
      2. Read the confirmation message and click OK to close.
      3. The text will now be green.
5. Click the **Select objective** button.
   - browse through the objectives listed
   - if there is one there that describes your objective, select it
   - if your objective is not listed, please consider giving us feedback, so that we can consider adding one.
6. Using the "Select file to edit" pulldown menu, to choose either Configuration.h or Configuration_adv.h.
7. If you want to edit the Configuration*.h files already in the ./Marlin folder of this repository, then click the Load Base button. ("Base" refers to the files that the Build Firmware function uses.)
   If you want to use the example configuration files that were supplied by Marlin for your target printer (from the ./config/ folder), click the "Load Config Example" button.
   If you want to load a Configuration*.h file from anywhere else on your system, click the "Load Other..." button and browse to that file.
8. Whichever file you have elected to load will now appear in the editor window.
9. If you did select an objective at step 5, now click the checkbox beside a displayed keyword, the editor window will display only the line(s) containing that keyword.
   Alternatively or additionally:
    - typing into the keyword filter field will filter the displayed lines.
    - checking the box beside "Hide Comments" will hide all comment lines and blank lines.
    - 
   NOTE: The effect of all filters is additive, so take care to clear any that you no longer want to apply.  

   WARNING: You can scroll through the displayed lines, but the tkinter tool used to build the graphics was not able to support displaying the entire file at once, so it only displays 200 lines at a time.
   To work around that limitation, the filter "View in Context" allows you to click on a displayed line and "jump"to the location of that line in the file, with +/- 99 lines above and below that line available for viewing by scrolling up/down.
10. When you have found a line you wish to change, click on it and type in your changes.
11. If you wish to keep your change, click the **Save Edit** button before changing any of the display filters.
12. When you have made all of the edits you wish to make, click the **Save File** button.
    If you want to overwrite the base file with your modified file, click the **Yes** button.
    If you want to save it elsewhere (or to Cancel the Save action), click the **No** button.
    Either browse to where you want to save the file, or click **Cancel** if that is your wish.
    ```
    **NOTE:** The Configurator tool will not allow saving a file into the ./config/ example folders.
    ```
13. When you are satisfied that you have made all of the required changes and have saved the file, then check the box beside the corresponding Configuration*.h OK.
**WARNING:** Even if you do not need to make any changes to either of the Configuration*.h files, you will still need to Load them both and Save them both, to overwrite the base files, if you used the Load Examples button!
15. When you have checked both of the "OK" boxes AND the correct environment has been loaded into platformio.ini (ref step 4, above), th**e Build Firmware button will turn green and become available for use.
16. As long as you have platformio installed, clicking **Build Firmware** will now open a new "tk" window where you can watch reports on the build process progress.
17. Wait for the process to finish. The tool will tell you where your new `firmware.bin` file is saved.
18. Navigate to the .pio/build/<environment name> folder and locate the most recent firmware*.bin file.

---

## 7. Flash the Firmware to Your Printer

1. Insert your SD card into your computer.
2. Copy the `firmware.bin` file to the root of the SD card.
3. Safely eject the SD card.
4. Insert the SD card into your printer and power it on.
5. Wait for the update to complete (follow your printer’s instructions).
6. Test your printer to confirm that you have successfully implemented the changes you meant to make.

---

## 8. Troubleshooting

- **The tool won’t open:**  
  If there is a file configurator_debug.log, open that in a text editor like Notepad and look for clues.
  Make sure Python 3 and Tkinter are installed. Try running from a terminal/command prompt.
- **No firmware.bin file is created:**  
  Check for error messages in the tool. Make sure you have write permissions to the folder.
- **Security warning (macOS):**  
  Go to System Preferences > Security & Privacy and allow the app to run.
- **Other issues:**  
  See the [FAQ](../FAQ.md) or ask for help on the community forum.

---

## 9. Need More Help?

- See the [FAQ](../FAQ.md)
- Visit the [community support forum](https://community.cr6.com)
- Contact the project maintainers

---

*Happy printing!*
