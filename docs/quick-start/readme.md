# Quick-Start Guide to CR6Community-Marlin_TB

## What is here?
This repository contains:
-   the CR6Community Marlin Firmware, at release 6.2
-   tools and documents designed to facilitate the configuration, build and distribution of this firmware

### Where is the firmware?
**Pre-compiled builds** ready to download and flash are listed in [the Assets section of the latest Release, here.](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/releases/tag/v2.0.9.1-cr6-community-release-6.2)

### How do I "roll my own" firmware?
**You can use [the configurator.py desktop GUI tool](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/main/tools/configurator)** to define and build your own customized version of this firmware. 
The configurator.py app runs on either Windows or Linux systems.  It uses the Marlin3D tool [auto_build.py](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/main/tools/build), which in-turn uses the app platformio to perform the actual build.

#### What can I do with configurator.py?
The configurator.py app includes:
- a recommended workflow checklist
- a series of "objective-specific flash cards", which detail how to perform the most common Marlin customizations (e.g. increasing the maximum nozzle temperature threshold).  These cards include a recommended keyword filter that makes finding the line(s) to change as easy as clicking a box.
- a text editor that facilitates the loading, filtering, modifying and saving of the Configuration.h and Configuration_adv.h files specifically prepared for each of the *cr6* printers named in ./config.
- text display filters that facilitate finding the fields to change, view filtered lines in context, hiding comments and blank lines.
- a colour-coded display of the current platformio.ini development environment setting and the correct value according to platformio-environment.txt in the selected target printer ./config/<example> folder.
- a one-click function to update the platformio.ini file with the correct compilation environment text.
- the ability to load or save either the files in the ./Marlin folder, or in the ./config/<example> folder, or elsewhere in your file system
- a one-click function to build the customized firmware.

Robust error-checking and prevention logic guides the user through the recommended workflow, helping to ensure success.

### Do I need to install anything else, for this stuff to work?
**Maybe...**
The python tools require python version 3.6+ to be installed on your system.
The auto_build.py tool requires platformio to be installed.

If you are using a Linux platform, python is probably already installed.
If you are using a Windows platform, you may need to download and install python. (Python nstallers are available from Python.org (recommended) or from the Microsoft Store.)

Any AI agent (e.g. Microsoft CoPilot on Windows) can guide you through the process of installing and configuring python, platformio, etc.


### What about all the other stuff, here?
If you just want to make a customized build for your printer(s), you can safely disregard all of "the other stuff" and just use [configurator.py]{https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/main/tools/configurator/configurator.py}.

That is not to say that you can safely delete or move that other stuff.  
 - Some of it is used by Platformio, when building the firmware.
 - Some of it is tools and documentation provided by the development team at Marlin3D.org.
It is best to leave everything right where it is, for simple stable operation.

If you decide to explore more sophisticated installations and operations, like using the Docker-based containerized environment, everything is here to help you do that, too.