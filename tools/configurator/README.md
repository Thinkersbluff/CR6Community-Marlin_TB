# 🛠️ CR6Community Marlin Configurator

Welcome to the CR6Community Marlin Configurator! This tool helps you customize your Marlin firmware with ease.  

Whether you're new to 3D printing or a seasoned tinkerer, this guide will walk you through setup and usage across Windows, Linux, and macOS.

---

## So, FIRST You Installed the Repository, Right?
This guide assumes that you started by following the instructions in the [Quick-Start README.md](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/main/docs/quick-start/readme.md), and now you have landed here.
HINT: (If you have not yet installed the repository files, please go back and start there...)

## 🧰 What Else You’ll Need to Install
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

## 1. Install Python and Tkinter
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

### Troubleshooting
- If you see `ImportError: No module named '_tkinter'`, rerun the Python installer and select "Modify", then ensure "tcl/tk and IDLE" is checked.
- If `python` is not recognized, you may need to add Python to your PATH manually or use `py` instead of `python`.

## 2. Install PlatformIO

PlatformIO is required to build Marlin firmware from source. You can install it either as a Python package (for command-line use) or as a Visual Studio Code extension.

### Step-by-step Instructions
1. Open the Command Prompt (Windows+R, type `cmd`, press Enter).
2. Install PlatformIO globally:
   ```sh
   python -m pip install --user platformio
   ```
3. After installation, check that PlatformIO is available, by typing this into the Command Window:
   ```sh
   platformio --version
   ```
   You should see the version number printed in the Command Window. 
   
### Troubleshooting   
   If you get an error like 'platformio is not recognized', platformio may not yet be in the path.  Close and reopen your Command Prompt, or log out and back in, and retry.

</details>

<details>
<summary><strong>🍏 macOS</strong></summary>

## 1. Install Python and Tkinter
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

## 2. Install PlatformIO

PlatformIO is required to build Marlin firmware from source. 
You can install it as a Python package.

### Step-by-step Instructions

1. Open Terminal (`Cmd + Space`, type `Terminal`, press Enter).
2. Install PlatformIO using pip:
   ```sh
   python3 -m pip install --user platformio
   ```
   If you're using Homebrew Python, you may need to use pip3 directly:
   ```sh
   pip3 install --user platformio
   ```
   After installation, verify PlatformIO is available:
   ```sh
   platformio --version
   ```
   You should see the version number printed in the Terminal.

### Troubleshooting

If you get an error like 'platformio' command not found, it may not be in your shell’s PATH yet.
Close and reopen Terminal, or restart your computer.

If the issue persists, try running PlatformIO directly from its install location:
```sh
~/.local/bin/platformio --version
```
To permanently fix the PATH, add this line to your shell profile (~/.zprofile, ~/.bash_profile, or ~/.zshrc depending on your shell):
```sh
export PATH="$HOME/.local/bin:$PATH"
```
Then restart Terminal for the change to take effect.

</details>

<details>
<summary><strong>🐧 Linux (Ubuntu/Debian)</strong></summary>

## 1. Install Python and Tkinter
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

## 2. Install PlatformIO

PlatformIO is required to build Marlin firmware from source. You can install it either as a Python package (for command-line use) or as a Visual Studio Code extension.

### Step-by-step Instructions
1. Open the Command Prompt (Windows+R, type `cmd`, press Enter).
2. Install PlatformIO globally:
   ```sh
   python -m pip install --user platformio
   ```
3. After installation, check that PlatformIO is available, by typing this into the Command Window:
   ```sh
   platformio --version
   ```
   You should see the version number printed. If you get an error, close and reopen your Command Prompt, or log out and back in.

## Troubleshooting
If you get an error like 'platformio: command not found', it may not be in your shell’s PATH yet.
- Restart your terminal session — sometimes the PATH update takes effect only after logging out or reopening the terminal.
- Try running PlatformIO directly from its install location:
```sh
~/.local/bin/platformio --version
```
Add PlatformIO to your PATH manually by editing your shell profile. Depending on your shell, open one of the following files:

~/.bashrc (for Bash)

~/.zshrc (for Zsh)

~/.profile (for general login shells)

Then add this line at the end:
```sh
export PATH="$HOME/.local/bin:$PATH"
```
Apply the changes by running:
```sh
source ~/.bashrc
```
(or the appropriate file for your shell)

After that, retry:
```sh
platformio --version
```
You should see the version number printed. If not, double-check the installation path and shell configuration.

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
### Troubleshooting

Rather than try to document precise instructions for troubleshooting installation on other multiple other Linux distros, I will leave you with these wisdoms and my best wishes:

🐧 Platform-Specific Considerations

1. Package Manager Differences

Ubuntu/Debian: Uses apt for installing dependencies.

Fedora/RHEL: Uses dnf or yum.

Arch Linux: Uses pacman.

If PlatformIO or Python dependencies were installed via a package manager, the install location might differ.

2. Shell Defaults

Ubuntu typically defaults to bash, while newer distros (like Fedora or Arch) may default to zsh or fish.

That affects which profile file you need to edit (.bashrc, .zshrc, etc.).

3. User Directory Structure

Some distros use different conventions for where user-installed binaries go. While ~/.local/bin is common, others might use:

~/bin

/usr/local/bin

Or even custom paths set by the user or system policies.

4. SELinux or AppArmor Restrictions

On Fedora or RHEL, SELinux might block execution from certain directories unless explicitly allowed.

Ubuntu uses AppArmor, which can also restrict access depending on the profile.

5. Systemd vs. Init

If you're automating PlatformIO tasks or launching services, the init system (e.g., systemd vs. SysVinit) might affect how you configure those.

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


---

## 📚 Getting Help

- For help with the configurator tool, visit the [CR6Community GitHub repository](https://github.com/CR6Community/CR6Community-Marlin_TB/issues).

---

Happy printing! 🖨️


Need "More input?” – <a href="README_tldr-not.md" title="Input overload initiated!">🤖 <strong>Johnny 5!</strong></a>