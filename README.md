# Community firmware for the Creality CR-6 3D printer

```
CAUTION:
This version of the CR6Community Firmware is compiled from the code last posted on the CR6Community - Marlin repository in 2021.
Although it is labelled as being based on Marlin 2.0.9.1, a comparison of the files between this version and the official
Marlin 2.0.9.1 release reveals numerous differences between the two.
We can not be certain that all of the functionality (or indeed of the bugs) in the official Marlin release are also captured in this release 6.2.
We have done our best to ensure that this release is stable and fully-functional.  Please check the Issues before deciding to download and use this firmware.
If you find issues with this code on your printer, please advise Thinkersbluff, either in an Issue here or on the CR6Community Discord.
```

<details>
<summary><strong>Where are the Downloads?</strong></summary>

To download a pre-release "bugfix" version of the pre-compiled firmware.bin for a CR6-SE or CR6-MAX printer in stock configuration, see [the LATEST RELEASE FILES folder](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/tree/debug_e-steps/LATEST%20RELEASE%20FILES). 
To download the formally released firmware.bin for a CR6-SE or CR6-MAX printer in stock configuration, see the Assets section of the latest Release. 

 
If your printer is a CR6-SE or CR-6-MAX in stock condition, you will see a .zip file in the Assets section of the latest Release, whose name best describes your printer.
Download and extract that file, read any included notes, and flash the included firmware to your printer.
</details>

<details>
<summary><strong>Where is the Display Firmware?</strong></summary>
There is a copy of the DWIN_SET folder in the .zip file you download (unless your printer does not use the stock TFT). 

If you are upgrading your CR6Community motherboard firmware from v6.1 to v6.2, you have no display firmware changes to make.  
Version 6.2 of the motherboard firmware works with [the refactored v1.1.x display firmware.](https://github.com/CR6Community/CR-6-touchscreen)
 
If you are upgrading from Creality stock firmware to CR6Community v6.2, you should install the display firmware first for the most seamless experience as you then flash the motherboard.    

If you encounter problems installing the display firmware, try looking for help [here in the documentation:](https://github.com/CR6Community/CR-6-touchscreen)
</details>

<details>
<summary><strong>How Do I Customize This Firmware for My Printer?</strong></summary>
You actually have 'too many' options for customizing this firmware for your own printer(s), and documenting all of the possibilities for all levels of comfort and expertise is just proving too confusing, not helpful.  

For users comfortable using VSCode, Platformio, and shell scripts, this firmware compiles the same way as any other Marlin release.  

To make customizing the firmware 'accessible' for the rest of us, Thinkersbluff has built and provided a gui-based desktop utility that enables you to customize your firmware with 'a few clicks.'
 - See the quick-start guide, to get started.  
 - Let us know how we could do better, in the Discussions.

For the latest guidance on how to build a customized firmware.bin file for your specific printer (e.g. with a higher max nozzle temperature), please read [./docs/quick-start/readme.md](https://github.com/Thinkersbluff/CR6Community-Marlin_TB/blob/main/docs/quick-start/readme.md)
</details>

<details>
<summary><strong>Can I Run The Latest Marlin on a CR6 Printer, Instead?</strong></summary>
Yes, you can.  

### Option 1: Octoprint
You can use Octoprint as your display/control firmware and flash the latest Marlin to your printer motherboard.
You will not be able to use the stock firmware or Community Firmware to activate the t TFT any more, but that might not matter to you.

### Option 2: BTT TFT in LCD Mode
If you have a BTT SKR CR6 motherboard and a BTT TFT display, you might find that you can flash the current version of Marlin to your printer, and use it with the Marlin UI.

### Option 3: Use one of the Integrated Extui Interface Firmwares 
There are several 3rd party (external UI) options named in the code, but this Community Firmware is not one of them.

### Option 4: "Roll Your Own"
It looks like the DGUS-Reloaded display firmware for Marlin - one of the third-party firmwares for which an extui interface is still defined and maintained in the latest Marlin - was archived in 2022.
A bold "developer type" may be able to exploit that interface to integrate the CR6Community firmware with Marlin, just like the original project imagined...


_Please visit us on the Discord, or in the Discussions forum here, to let us know what you achieve, if you try any of the above options._
</details>

<details>
<summary><strong>A note about the original project</strong></summary>

The developers of the original CR6Community Firmware had hoped that the upstream Marlin3D team would merge their work back into the Marlin3D mainstream.
Unfortunately, the upstream developers pulled an early version of the project, just before the Community Firmware went therough a major refactoring.  By the time this code achieved its own feature enhancement goals, the GitHub Diff functionality could no longer support remerging the two streams.

Version 6.1 thus has become a dead-ended fork of Marlin, based on Marlin release 2.0.8.1.
Our development team had, however, also begun rebaselining to Marlin 2.9.0.1, when they stopped work back in 2021.
That code does not compile, and it contains a couple of bugs, but otherwise works fine with the refactored display firmware at version 1.1.

This project takes a snapshot of that work, fixes the bugs, and updates it to compile with the current versions of Platformio, VSCode, Git, and Python 3.12.3.
It also continues to use and extend the original accompanying test and development automation suite.
</details>

<details>
<summary><strong> What is the Purpose of this Repository?</strong></summary>

This fork of Marlin is meant for:

- Providing a stable version of the CR6 Community Firmware at version 6.2 (which is based on Marlin 2.0.9.1) for the CR-6 SE and MAX printers with Creality 4.5.2, 4.5.3 or 1.1.0.3 ERA motherboards or the [BTT SKR CR6](https://damsteen.nl/blog/2020/11/25/how-to-btt-skr-cr6-installation) motherboard
- Updating and documenting the accompanying development and test environment, to make it easier for non-programmers like Thinkersbluff who wish to support other printer variants.
</details>
<details>
<summary><strong>We are a Community</strong></summary>
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
</details>

<details>
<summary><strong>Credits</strong></summary>

The current core CR-6 Community firmware dev team consists of:

 - Sebastiaan Dammann [[@Sebazzz](https://github.com/Sebazzz)] - Netherlands &nbsp; ([Donate](https://www.paypal.com/donate?hosted_button_id=YCH72S6WZQ5X4) ([Profile](https://www.paypal.com/paypalme/sebastiaandammann)) | [Website](https://damsteen.nl))
 - Juan Rodriguez [[@Nushio](https://github.com/Nushio)] - Mexico
 - Romain [[@grobux](https://github.com/grobux)] - France ([Donate](https://www.paypal.com/donate?hosted_button_id=CP2SAW4W9RBT4))
 - Nick Acker [[@nickacker](https://github.com/nickacker)] - USA
 - And more...

We stand on the shoulders of giants. Don't forget to send your love [upstream too](https://github.com/MarlinFirmware/Marlin)!
</details>

<details>
<summary><strong>License</strong></summary>

Marlin and the Creality CR-6 Community Firmware is published under the [GPL license](/LICENSE) because we believe in open development. The GPL comes with both rights and obligations. Whether you use Marlin firmware as the driver for your open or closed-source product, you must keep Marlin open, and you must provide your compatible Marlin source code to end users upon request. The most straightforward way to comply with the Marlin license is to make a fork of Marlin on Github, perform your modifications, and direct users to your modified fork.

While we can't prevent the use of this code in products (3D printers, CNC, etc.) that are closed source or crippled by a patent, we would prefer that you choose another firmware or, better yet, make your own.
</details>
