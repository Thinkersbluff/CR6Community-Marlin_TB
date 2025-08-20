
# Welcome!

This repository includes:

./ LATEST_BUGFIX_RELEASE_FILES:
 - a set of .zip files, containing both the motherboard firmware and its matching display firmware, from which any stock-configuration CR6 printer can be flashed with this firmware

./Marlin:
 - a fork of the Marlin firmware, based on - but different from - Marlin 2.0.9.1, specifically tailored to support using the CR6Community Display Firmware to control your CR6 printer.

./config:
 - a set of example Configuration*.h files and Platformio files, from which this Marlin firmware can be compiled to run on specific motherboards

./tools:
 - a set of tools from which you can modify the Configuration*.h files and build a customized version of the motherboard firmware for your specific printer(s)

 ./docs:
 - a set of documentation like this, to help you make sense of it all, set it up and use it on your own Windows (10/11), Linux or MAC computer.

There are also a whole lot of "other" files that you can ignore, while you get started.  If you need them, we will introduce you to them as we go.

---

# Quick-Start Workflows:
These are the key steps we recommend you follow, in this order:

## 1. Decide whether you want to customize this firmware
No need to suffer the endless pain & confusion that is the life of a professional Software Developer (":wink:") if you don't need to know anything about compiling!  You may have much simpler alternatives.

## 2. Clone this Repository to Your Local Hard-Drive
Breathe! 
Stay with me! 
Step-by-step instructions follow, below.


### Step-by-step Instructions:
See!?

1. To just copy everything you need to your hard drive:

- Go to: [github.com/Thinkersbluff/CR6Community-Marlin_TB](https://github.com/Thinkersbluff/CR6Community-Marlin_TB)
- Click the green Code button
- Select Download ZIP
- Open your Downloads folder
- Right-click the file CR6Community-Marlin_TB-main.zip → choose Extract All…
- Choose where you want to keep the project (e.g., D:\Firmware)
- Open the folder: CR6Community-Marlin_TB-main\tools\configurator
- Open README.md in that folder for the next steps
💡 If Python, pip, or PlatformIO aren’t installed yet, you’ll also need them, to build the firmware.

2. To make a copy of the repository that you can keep up to date with the online version:

1. Install git on your system
2. Use git to clone this repository directly to your computer. 

This option allows you to easily keep your local copy up to date with the latest changes by running a simple git pull command in a terminal window. 

## 3. Install/Activate the Build Environment
### As a Firmware User:
No containers required.
Just install python and platformio globally 
AND use ./tools/configurator/configurator.py

### As a Firmware Developer:
Recommended: Use the containerized build environment (compose.yaml, Dockerfile), located in the root of the repository

Optionally: 
Linux/macOS: Install platformio and python on your platform and run the Bash shell scripts in a local terminal.

Windows: Install WSL2 and create your own docker-based build environment 
OR Use the Powershell scripts located at ./tools/windows/build

## 4. Customize and build your own firmware.bin(s)

### As a Firmware User
If you prefer using GUI-based apps, you may find [**the CR6Community Marlin Configurator desktop gui app**](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/main/tools/configurator) to be exactly the tool you need.

If you prefer Command-Line Interfaces, you can install platformio and python locally and edit/run build-single.sh in a bash window.
---

For more detailed help - refer to the appropriate guide specific to your operating system. 

- [_BUILD_HELP](_BUILD_HELP)

---

### As a Firmware Developer:
Developers will likely be familiar with the Microsoft Visual Studio Code application.
Recommended VSCode extensions for Developers include:
 - Platformio
 - Auto Build Marlin
 - C\C++
 - C\C++ Extension Pack
 - Python
 - Pylint
 - GitHub Respositories
 - GitHub Co-Pilot and 
 - GitHub Co-Pilot Chat


**NOTE:** IF you do plan to make changes to the repository contents that you would like to share with us, upstream, please fork the repository to your own GitHub account, and use PRs to submit recommended changes to us.

---

For more detailed help - refer to the appropriate guide specific to your operating system. 

- [_DEVELOPMENT_HELP](_DEVELOPMENT_HELP)

---

### Of Great Importance to ALL!

There are also these guidelines which are important to all of our users:

- [_GUIDELINES_FOR_ALL_USERS](_GUIDELINES_FOR_ALL_USERS)

Honest!  
Don't skip 'em!!
You may suffer more than regrets if you skip those!!!
