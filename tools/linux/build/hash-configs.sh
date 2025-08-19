#!/bin/bash
# hash-configs.sh: Compute and print SHA256 hashes for Marlin/Configuration*.h
# Usage: ./hash-configs.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CONFIG_H="$REPO_ROOT/Marlin/Configuration.h"
CONFIG_ADV_H="$REPO_ROOT/Marlin/Configuration_adv.h"

if [ ! -f "$CONFIG_H" ] || [ ! -f "$CONFIG_ADV_H" ]; then
    echo "ERROR: Configuration.h or Configuration_adv.h not found in Marlin/"
    exit 1
fi

HASH_H=$(sha256sum "$CONFIG_H" | awk '{print $1}')
HASH_ADV=$(sha256sum "$CONFIG_ADV_H" | awk '{print $1}')

# Output hashes in a parseable format
cat <<EOF
CONFIG_H_SHA256=$HASH_H
CONFIG_ADV_H_SHA256=$HASH_ADV
EOF
