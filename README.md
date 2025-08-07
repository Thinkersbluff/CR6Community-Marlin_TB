# Community firmware for the Creality CR-6 3D printer

**The extui branch is pre-configured for Thinkersbluff's own Creality CR-6 SE with:
- stock v1.1.0.3 ERA motherboard
- PT1000 hotend thermistor (sensor_0 = 1047)
- Orbiter v1.5 extruder (690 steps/mm)
- Phaetus Dragon HF all-metal hotend
- stock TFT display.

To download a pre-compiled firmware.bin for a CR6-SE or CR6-MAX printer in stock configuration, see the Assets section of the latest Release.

_To compile a unique version of this firmware tailored for your own customized CR6-SE or MAX, clone the repo or download Sources.zip from the latest Release and follow the instructions in the [Development and compile-it-yourself](#development-and-compile-it-yourself) section below._

This repository comes complete with the original comprehensive automation suite and new [documentation on how to install and use that suite](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/extui/BUILD_AND_TEST.md), for anyone who decides to clone this repo and work with it locally.
Note: The new documentation assumes you are working on a Linux PC, and guides you through installing the development and test suites into a docker container.
      There are also Powershell scripts and documentation on how to use those on Windows and in the VSCode terminal window.

## Downloads

Please find official releases in the [Releases section](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/releases/tag/v2.0.9.1-cr6-community-release-6.2) . 
Please read the release notes *carefully* and ensure that you download the right asset.

If your printer is a CR6-SE or CR-6-MAX in stock condition, you will see a .zip file whose name describes your printer.
Download and extract that file, read any included notes and flash the included firmware to your printer. 

### About the display firmware
Version 6.2 of the motherboard firmware still works with the refactored v1.1.x display firmware.
If you are upgrading your CR6Community motherboard firmware from v6.1 to v6.2, you have no display firmware changes to make.
If you are upgrading from Creality stock firmware to CR6Community v6.2, you should install the display firmware first for the most seamless experience.
If you need it, there is a copy of the DWIN_SET folder in the .zip file you download.  If you encounter problems installing it, try looking for help [here in the documentation:](https://github.com/CR6Community/CR-6-touchscreen)

### Notes:
*The same firmware[suffix].bin that supports the Creality v4.5.3 motherboard also supports the Creality v1.1.03 (ERA) board.*
*Additional support for the [BTT SKR board](https://damsteen.nl/blog/2020/11/25/how-to-btt-skr-cr6-installation) is available.*

If you want to modify the default Configuration.h or Configuration_adv.h file(s) and recompile the firmware for your own system, then you should instead download the Source.zip file.

### Development and compile-it-yourself

There are several example configurations available for your convenience which can be found in the [`config`](./config) directory. Delete the Configuration.h and Configuration_adv files already in the root of the [`Marlin`](./Marlin) directory and copy/paste the equivalent files from the config subdirectory named for the target hardware configuration. 

To do your own compilation, you will need to download and install Microsoft Visual Studio Code and install at least the Platform.io extension.
There is an optional Auto Build Marlin extension for VSCode, you could also install.
Edit the configuration files as you wish.  Ensure that the Platform.io environment variable `default_envs` in the platformio.ini file is set to the text in the `platformio-environment.txt` file in that same config folder, before you try to build the firmware.

If you run into troubles figuring out how to install, configure and compile with VSCode and Platform.io, you can look for help on YouTube or try asking the GitHub CoPilot to troubleshoot and repair your setup, right in VSCode!

Validated configuration examples and pre-compiled flashable assets using those configurations are maintained here for the following hardware configurations:

- Creality stock TFT with:
   - Creality v4.5.2 motherboard (CR-6 SE)
   - Creality v4.5.3 or 1.1.0.3 ERA motherboard (CR-6 SE and CR-6 MAX)
   - BigTreeTech SKR CR-6 (CR-6 SE and CR-6MAX)
- BigTreeTech SKR CR-6 with BigTreeTech TFT v3.0

In 2025, the only board still being sold for the CR6 is the 1.1.0.3 ERA board, but you might still own (or find a second-hand) one of the other boards, so we continue to support all four.

The original project also experimented with examples for other printers with compatible display hardware, but that is more than Thinkersbluff has time to research.
Those examples remain in this repo, and may work for you, but they are not supported here.

_NOTE: If you have a BTT SKR CR6 motherboard and a BTT TFT display, you might find that you can flash the current version of Marlin to your printer, and use it with the Marlin UI.
Please let us know what you achieve, if you try that._

## A note about the original project

The developers of the original CR6Community Firmware had hoped that the upstream Marlin3D team would merge their work back into the Marlin3D mainstream.
Unfortunately, the upstream developers pulled an early version of the project, just before the Community Firmware went therough a major refactoring.  By the time this code achieved its own feature enhancement goals, the GitHub Diff functionality could no longer support remerging the two streams.

Version 6.1 thus has become a dead-ended fork of Marlin, based on Marlin release 2.0.8.1.
Our development team had, however, also begun rebaselining to Marlin 2.9.0.1, when they stopped work back in 2021.
That code does not compile, and it contains a couple of bugs, but otherwise works fine with the refactored display firmware at version 1.1.

This project takes a snapshot of that work, fixes the bugs, and updates it to compile with the current versions of Platformio, VSCode, Git, and Python 3.12.3.
It also continues to use and extend the original accompanying test and development automation suite.

## Purpose of this repository

This fork of Marlin is meant for:

- Providing a stable version of the CR6 Community Firmware at version 6.2 (which is based on Marlin 2.0.9.1) for the CR-6 SE and MAX printers with Creality 4.5.2, 4.5.3 or 1.1.0.3 ERA motherboards or the [BTT SKR CR6](https://damsteen.nl/blog/2020/11/25/how-to-btt-skr-cr6-installation) motherboard
- Updating and documenting the accompanying development and test environment, to make it easier for non-programmers like Thinkersbluff who wish to support other printer variants.
- Taking advantage of the Marlin firmware change activities and online commitment/release history, to cherry-pick critical fixes for bugs in Marlin 2.0.9.1, which were only discovered and resolved in later releases.

## Community firmware support & communities

Get in touch with the original developers or Thinkersbluff! We [have our own Discord server](https://discord.gg/RKrxYy3Q9N).

This YouTube channel directly supports our CR6Community:

 - [Making Things Real 101 - CR6Community Support](https://youtube.com/@makingthingsreal101?feature=shared)

Other CR-6 communities exist:

- [Facebook independent CR-6 community](https://www.facebook.com/groups/cr6community)
- [Reddit /r/CR6](https://www.reddit.com/r/CR6/)

Communities hosted by Creality:

- [Official CR-6 user group](https://www.facebook.com/groups/CR6SECR6MAX)
- [Official Creality user group](https://www.facebook.com/groups/creality3dofficial)

Other communities:

- [Reddit /r/3dprinting](https://www.reddit.com/r/3dprinting/)

### General Marlin support

For general Marlin support, please check:

- [Marlin Documentation](http://marlinfw.org) - Official Marlin documentation
- [Marlin Discord](https://discord.gg/n5NJ59y) - Discuss issues with Marlin users and developers
- Facebook Group ["Marlin Firmware"](https://www.facebook.com/groups/1049718498464482/)
- RepRap.org [Marlin Forum](http://forums.reprap.org/list.php?415)
- Facebook Group ["Marlin Firmware for 3D Printers"](https://www.facebook.com/groups/3Dtechtalk/)
- [Marlin Configuration](https://www.youtube.com/results?search_query=marlin+configuration) on YouTube


## Reporting issues
- Please submit your questions and concerns in the [issue tracker](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/issues)
- Submit **bug fixes** as pull requests to the current active default branch (`extui`)
- Follow the [coding standards](https://marlinfw.org/docs/development/coding_standards.html)

## Credits

The current core CR-6 Community firmware dev team consists of:

 - Sebastiaan Dammann [[@Sebazzz](https://github.com/Sebazzz)] - Netherlands &nbsp; ([Donate](https://www.paypal.com/donate?hosted_button_id=YCH72S6WZQ5X4) ([Profile](https://www.paypal.com/paypalme/sebastiaandammann)) | [Website](https://damsteen.nl))
 - Juan Rodriguez [[@Nushio](https://github.com/Nushio)] - Mexico
 - Romain [[@grobux](https://github.com/grobux)] - France ([Donate](https://www.paypal.com/donate?hosted_button_id=CP2SAW4W9RBT4))
 - Nick Acker [[@nickacker](https://github.com/nickacker)] - USA
 - And more...

We stand on the shoulders of giants. Don't forget to send your love [upstream too](https://github.com/MarlinFirmware/Marlin)!

## License

Marlin and the Creality CR-6 Community Firmware is published under the [GPL license](/LICENSE) because we believe in open development. The GPL comes with both rights and obligations. Whether you use Marlin firmware as the driver for your open or closed-source product, you must keep Marlin open, and you must provide your compatible Marlin source code to end users upon request. The most straightforward way to comply with the Marlin license is to make a fork of Marlin on Github, perform your modifications, and direct users to your modified fork.

While we can't prevent the use of this code in products (3D printers, CNC, etc.) that are closed source or crippled by a patent, we would prefer that you choose another firmware or, better yet, make your own.
