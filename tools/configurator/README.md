# 🛠️ CR6Community Marlin Configurator

Welcome to the CR6Community Marlin Configurator! This tool helps you customize your Marlin firmware with ease.  

Whether you're new to 3D printing or a seasoned tinkerer, this guide will walk you through setup and usage across Windows, Linux, and macOS.

---

## 📦 Setup Instructions

1. Download the ZIP file from the repository
2. Extract it to a folder of your choice

> 📁 **Default path after extracting the ZIP:**  
> `<your chosen folder>/CR6Community-Marlin_TB-main/tools/configurator`  
> *(Adjust the path to where you actually extracted CR6Community-Marlin_TB-main.zip)*

---
## 🧰 What Else You’ll Need
Before you run the Configurator, your computer needs a few helpers installed:
- **Python 3** – a free tool that runs the Configurator
- ***Tkinter** – lets Python show windows and buttons (included with most Python installations.)
- **PlatformIO** – builds the Marlin firmware for your printer
> 🧠 ***A nod to the nerds:**  
> The GUI toolkit formerly known as `Tkinter` (capital T in Python 2) now lives on as `tkinter` (lowercase) in Python 3.  
> Same toolkit, new casing.

If you’ve never installed anything like this before, don’t worry. Choose your operating system below and follow the steps.


<details>
<summary><strong>🪟 Windows</strong></summary>


### Step-by-step Instructions
1. Download Python 3 from the [official website](https://www.python.org/downloads/).
2. Run the installer.  **Important:** On the first screen, check the box that says "Add Python to PATH".
3. Proceed with the installation. On the "Optional Features" screen, ensure that "tcl/tk and IDLE" is selected (this installs Tkinter).
4. After installation, open the Command Prompt (Windows+R, type cmd) and type this into the Command window:
   ```sh
   python --version
   ```
   You should see a confirmation appear in the Command Window showing the version of python that is now installed.

   Now type:
   ```sh
   python -m tkinter
   ```
   If a small window appears, Tkinter is working. If you get an error, rerun the installer and make sure "tcl/tk and IDLE" is checked.

5. (Optional) If you use VS Code, install the Python extension for best experience.

### Troubleshooting
- If you see `ImportError: No module named '_tkinter'`, rerun the Python installer and select "Modify", then ensure "tcl/tk and IDLE" is checked.
- If `python` is not recognized, you may need to add Python to your PATH manually or use `py` instead of `python`.

</details>

<details>
<summary><strong>🍏 macOS</strong></summary>

### Prerequisites
- Python 3 (pre-installed on most recent macOS versions)
- Tkinter (included with Python)

### Step-by-step Instructions
1. Open Terminal.
2. Check your Python version:
   ```sh
   python3 --version
   python3 -m tkinter
   ```
   If a small window appears, Tkinter is working. If not, install Python 3 from [python.org](https://www.python.org/downloads/).
3. If you use Homebrew, you can also install Python 3 with:
   ```sh
   brew install python3
   ```

### Troubleshooting
- If you see `ModuleNotFoundError: No module named 'tkinter'`, try reinstalling Python from python.org, as some Homebrew builds may lack Tkinter.

</details>

<details>
<summary><strong>🐧 Linux (Ubuntu/Debian)</strong></summary>

### Prerequisites
- Python 3
- Tkinter (may require separate package)

### Step-by-step Instructions
1. Open Terminal.
2. Update your package list:
   ```sh
   sudo apt update
   ```
3. Install Python 3 and Tkinter:
   ```sh
   sudo apt install python3 python3-tk
   ```
4. Check installation:
   ```sh
   python3 --version
   python3 -m tkinter
   ```
   If a small window appears, Tkinter is working.

### Troubleshooting
- If you see `ModuleNotFoundError: No module named 'tkinter'`, make sure you installed `python3-tk`.
- On other distributions, the package name may be `tk` or `tkinter`.

</details>

<details>
<summary><strong>Other Linux</strong></summary>

- Use your package manager to install Python 3 and Tkinter. For example, on Fedora:
  ```sh
  sudo dnf install python3 python3-tkinter
  ```
- On Arch Linux:
  ```sh
  sudo pacman -S python tk
  ```
- Always check with:
  ```sh
  python3 -m tkinter
  ```

</details>

---

## 🚀 Run the Configurator

<details>
<summary>🪟 Windows</summary>

**🟢 Option 1: Using the Terminal**

1. Press `Windows + R`, type `cmd`, and press Enter  
2. In the terminal window, type:
   ```sh
   cd "<your chosen folder>\CR6Community-Marlin_TB-main\tools\configurator"
   python -m configurator.py
   ```
3. Follow the on-screen instructions to select your firmware version and configuration options.
4. Once configured, download the customized firmware files.

**🟢 Option 2: Using the File Explorer**

1. Open File Explorer and navigate to the configurator folder:
   `<your chosen folder>\CR6Community-Marlin_TB-main\tools\configurator`
2. Double-click on `configurator.py` to run the tool.
3. Follow the on-screen instructions to select your firmware version and configuration options.
4. Once configured, download the customized firmware files.

</details>

<details>
<summary>🍏 macOS</summary>

**🟢 Option 1: Using the Terminal**

1. Open the Terminal application.
2. In the terminal window, type:
   ```sh
   cd "<your chosen folder>/CR6Community-Marlin_TB-main/tools/configurator"
   python3 -m configurator.py
   ```
3. Follow the on-screen instructions to select your firmware version and configuration options.
4. Once configured, download the customized firmware files.

**🟢 Option 2: Using the Finder**

1. Open Finder and navigate to the configurator folder:
   `<your chosen folder>/CR6Community-Marlin_TB-main/tools/configurator`
2. Double-click on `configurator.py` to run the tool.
3. Follow the on-screen instructions to select your firmware version and configuration options.
4. Once configured, download the customized firmware files.

</details>

<details>
<summary>🐧 Linux</summary>

**🟢 Option 1: Using the Terminal**

1. Open a terminal window.
2. In the terminal, type:
   ```sh
   cd "<your chosen folder>/CR6Community-Marlin_TB-main/tools/configurator"
   python3 -m configurator.py
   ```
3. Follow the on-screen instructions to select your firmware version and configuration options.
4. Once configured, download the customized firmware files.

**🟢 Option 2: Using the File Manager**

1. Open your file manager and navigate to the configurator folder:
   `<your chosen folder>/CR6Community-Marlin_TB-main/tools/configurator`
2. Double-click on `configurator.py` to run the tool.
3. Follow the on-screen instructions to select your firmware version and configuration options.
4. Once configured, download the customized firmware files.

</details>

---

## ❓ Troubleshooting

- **Issue:** Configurator fails to start.
  - **Solution:** Ensure Python 3 and Tkinter are correctly installed. Try running the configurator from the terminal to see error messages.

- **Issue:** Downloaded firmware files are not appearing.
  - **Solution:** Check your internet connection and ensure you have write permissions in the download directory. Try changing the download location in the configurator settings.

For more troubleshooting tips, visit the [CR6Community forums](https://community.cr6.com).

---

## 📚 Getting Help

- For help with the configurator tool, visit the [CR6Community GitHub repository](https://github.com/CR6Community/CR6Community-Marlin_TB/issues).
- For 3D printing and firmware questions, check the [CR6Community forums](https://community.cr6.com).

---

Happy printing! 🖨️


Need "More input?” – <a href="./README_tldr-not.md" title="Input overload initiated!">🤖 <strong>Johnny 5!</strong></a>