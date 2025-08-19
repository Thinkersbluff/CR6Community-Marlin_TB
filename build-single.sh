#!/bin/bash
set -e

BOARD_CONFIG_DIR="config/btt-skr-cr6-with-btt-tft"  # Change as needed

# Backup your own config files
cp Marlin/Configuration.h Marlin/Configuration.h.userbak
cp Marlin/Configuration_adv.h Marlin/Configuration_adv.h.userbak

# Copy board-specific config files
cp "$BOARD_CONFIG_DIR/Configuration.h" Marlin/Configuration.h
cp "$BOARD_CONFIG_DIR/Configuration_adv.h" Marlin/Configuration_adv.h

# Run your build (adjust as needed)
platformio run -e STM32F103RE_btt_USB

# Restore your own config files
mv Marlin/Configuration.h.userbak Marlin/Configuration.h
mv Marlin/Configuration_adv.h.userbak Marlin/Configuration_adv.h