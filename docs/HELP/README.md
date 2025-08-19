# Welcome!

Finding things in this repository is intended to be accessible and intuitive, for all levels of user experience and comfort-level.  

We have done our best to place things into folder structures that suggest what you might find therein and then into subfolders that then optimize your path to the item you seek.

Some users will be highly experienced in software development and Integrated Development Environment (IDE) organizational structures.  To you, we tip our hats in admiration and respectfully beg your indulgence when we use non-standard language.

Some users will find GitHub's structures and conventions a bit strange, maybe confusing.  For you, we are particularly concerned that we also be respectful with the measures we use to keep the site accessible for all.  

If any of you notice places where we have left a ""bump" in your path, please let us know in the Discussions and we will do our best to smooth that out.

## Let's Get Started!

Which of the following best describes you, today?

### I Just Want to Download the Latest Firmware!
If you just want to be able to download pre-compiled firmware for your "*stock"-configuration CR6 printer (* including those printers using the BTT SKR CR6 replacement motherboard), you can just download the zip file that best describes your printer.  
[See LATEST_BUGFIX_RELEASE_FILES].

### I Just Want to Customize the Firmware for My Particular Printer(s).  _Please Don't Make Me Learn to 'Compile' Stuff!_
WARNING: This is where the conversation gets a little more complicated.  Stay with us, while we do our best to help you get this done, without being 'boring'.

#### "Some Assembly Required"
This firmware is a customized version of Marlin.

To customize Marlin firmware, users typically have two options:
1. The many the parameters which Marlin stores in Electronically Eraseable Programmable Read-Only Memory (EEPROM) can be made modifiable through the user interface. 
``` 
   - This is one of the main reasons that the CR6Community Firmware has become so popular with our user base. Version 6.1.1 of the CR6Community Display Firmware supports a lot of customization from the display. 
   - Try navigating to the Setup menu area on your display and browse to see whether you can find a way to edit what it is that you want to change.
```
2. The rest of the user-specifiable parameters can only be modified by editing the text in one or both of the two Configuration*.h files and then recompiling the firmware.bin file.
```
   - If you just felt "cold chills" at the thought of having to "edit and compile", Keep Calm and Carry On a bit further, we have a tool we think will hide (most of) that complexity from you.  
   - If you can double-click an icon to launch a program, or if you prefer to use a command-line interface (CLI), we have you covered!
```
#### Fear not!  Behold, the 'Configurator'!
A lot of CR6 Discord Community members post questions about how to increase the maximum nozzle temperature limit or maybe how to reverse the direction of a pancake stepper-motor.

It is with those users in mind, whose spirits may have fallen a little when faced for the first time with having to figure out 'just enough' of the Professional Softwware Developer's language and tools and concepts, to be able to install, launch, configure, troubleshoot, repair and (finally) use Visual Code Studio to edit one line in a file and then recompile (do what?) the firmware.bin, that Thinkersbluff proudly presents: configurator.py.

Just run this one application, follow the workflow steps shown in the app, click a couple of buttons, and the Configurator will build your firmware.bin file for you.

On Windows (10 or 11), you can browse to the folder containing that application and double-click the icon, to launch the app.

On any of the three OS's, you can create a desktop shortcut to launch the gui app.

Alternatively, you can open a Terminal window (Command or Powershell on Windows, Bash on Linus or macOS) and run the app by typing "python3 configurator.py" and tapping the keyboard 'Return' key.

### If You Need 'More Input'...
The _BUILD_HELP documentation is there as a resource for you.
If you cannot find the info there - or if you find one of our famous 'mistake' Easter Eggs - please drop us a comment in Discussions or raise an Issue and we will do our best to make it better.

### TL;DR This is NOT My First GitHub/VSCode Rodeo!

If you are very comfortable with CLIs and IDEs, git, etc.., you probably skipped straight past the first section. You may not have bothered reading this at all...

If you are now reading this because we have moved or hidden something you expected to find, the _DEVELOPMENT_HELP section is there as a backup reference for you.

ENJOY!