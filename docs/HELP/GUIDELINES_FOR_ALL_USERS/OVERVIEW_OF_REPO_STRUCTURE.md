# Structural Overview

This repository is structured as a set of purpose-specific folders:

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

# Deliberate Deviations:

## Tools in the repo root

As we developed the HELP documentation, we found a few specific situations where the tools, in particular, did not work reliably unless they were placed directly into the root folder of the repository.

The initial development work started on a Linux Mint platform, and the Windows platform installation and testing work came later, when some decisions had already been made.

By the time we had Docker (and the WSL2) installed and working on Windows, we realized that we did not need separate "containers" on each OS platform.  Rather, we were able to make a couple of small adjustments to the compose.yaml file and enable the same containerized environment and the same shell scripts to work on all 3 platforms.

For that reason, we removed the tools/<platform>/build/docker folders from the structure