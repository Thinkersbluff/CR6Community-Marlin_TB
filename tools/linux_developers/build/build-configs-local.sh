#!/bin/bash
# ============================================================================
# CR6Community-Marlin_TB Multi-Config Build Script (Local Host Version)
# ----------------------------------------------------------------------------
# This script automates building, packaging, and archiving Marlin firmware for
# multiple board/configuration targets in the CR6Community-Marlin_TB repository.
# It uses the local host's PlatformIO and Python installations (no Docker).
#
# Usage Examples:
#   ./build-configs-local.sh my_release_name
#   ./build-configs-local.sh my_release_name btt-skr-cr6-with-btt-tft
#   ./build-configs-local.sh my_release_name "" true
#   ./build-configs-local.sh my_release_name "" false /path/to/CR-6-Touchscreen
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel 2>/dev/null)"

if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/platformio.ini" ]; then
    echo "ERROR: Could not detect repository root or not in a Marlin repository"
    exit 1
fi

RELEASE_NAME="${1:-test-build}"
SINGLE_BUILD="${2:-}"
DRY_RUN="${3:-}"
TOUCHSCREEN_REPO_PATH="${4:-../CR-6-Touchscreen}"

OUTPUT_DIR="$REPO_ROOT/.pio/build-output"
TIMESTAMP=$(date +%Y-%m-%d-%H-%M)

DWIN_SET_PATH="$TOUCHSCREEN_REPO_PATH/src/DWIN/DWIN_SET"
TOUCHSCREEN_AVAILABLE=false
if [ -d "$DWIN_SET_PATH" ]; then
    TOUCHSCREEN_AVAILABLE=true
fi

if [ -d "$OUTPUT_DIR" ]; then
    rm -rf "$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

CONFIGS=()
for config_dir in "$REPO_ROOT/config/"*/; do
    config_name=$(basename "$config_dir")
    if [ "$config_name" = "README.md" ]; then continue; fi
    if [ ! -f "$config_dir/Configuration.h" ]; then continue; fi
    if [ ! -f "$config_dir/Configuration_adv.h" ]; then continue; fi
    if [ ! -f "$config_dir/platformio-environment.txt" ]; then continue; fi
    CONFIGS+=("$config_name")
done

echo "Available configurations:"
for config in "${CONFIGS[@]}"; do
    echo "  - $config"
done

echo ""

build_config() {
    local config_name="$1"
    local config_dir="$REPO_ROOT/config/$config_name"
    echo "=== Building $config_name ==="
    if [ -f "$config_dir/no-autobuild.txt" ] && [ "$config_name" != "$SINGLE_BUILD" ]; then
        echo "Skipping $config_name (marked no-autobuild)"
        return 0
    fi
    local platform_env
    if [ -f "$config_dir/platformio-environment.txt" ]; then
        platform_env=$(cat "$config_dir/platformio-environment.txt" | tr -d '\n\r')
    else
        echo "ERROR: platformio-environment.txt not found in $config_dir"
        return 1
    fi
    if [ -z "$platform_env" ]; then
        echo "ERROR: platformio-environment.txt in $config_dir is empty or invalid."
        return 1
    fi
    local build_output_dir="$OUTPUT_DIR/$RELEASE_NAME-$config_name-$TIMESTAMP"
    local firmware_dir="$build_output_dir/Firmware/Motherboard firmware"
    local display_dir="$build_output_dir/Firmware/Display Firmware"
    local config_copy_dir="$build_output_dir/configs"
    mkdir -p "$firmware_dir" "$display_dir" "$config_copy_dir"
    cp "$config_dir"/Configuration*.h "$REPO_ROOT/Marlin/"
    local has_touchscreen=true
    if [ -f "$config_dir/no-touchscreen.txt" ]; then
        has_touchscreen=false
    fi
    if [ "$DRY_RUN" != "true" ]; then
        # Build with local platformio
        BUILD_OUT_FILE="$build_output_dir/platformio-build.log"
        echo "[DEBUG] Running platformio for $config_name (platform_env: $platform_env)" | tee "$BUILD_OUT_FILE"
        sed -i "s/^default_envs = .*/default_envs = $platform_env/" "$REPO_ROOT/platformio.ini"
        platformio run -e "$platform_env" --target clean >> "$BUILD_OUT_FILE" 2>&1
        platformio run -e "$platform_env" >> "$BUILD_OUT_FILE" 2>&1
        local firmware_file=$(ls -1t "$REPO_ROOT/.pio/build/$platform_env"/firmware*.bin 2>/dev/null | head -n1)
        if [ -z "$firmware_file" ]; then
            echo "ERROR: No firmware binary found for $config_name. See $BUILD_OUT_FILE for build output." | tee -a "$BUILD_OUT_FILE"
            return 1
        fi
        cp "$firmware_file" "$firmware_dir/"
        echo "Firmware copied: $(basename "$firmware_file")" | tee -a "$BUILD_OUT_FILE"
    else
        echo "DRY RUN: Would build $config_name with platform $platform_env"
    fi
    cp "$config_dir"/*.h "$config_copy_dir/" 2>/dev/null || true
    if [ "$has_touchscreen" = true ]; then
        if [ "$TOUCHSCREEN_AVAILABLE" = true ] && [ "$DRY_RUN" != "true" ]; then
            local dwin_zip="$display_dir/DWIN_SET.zip"
            (cd "$(dirname "$DWIN_SET_PATH")" && zip -r "$(basename "$dwin_zip")" "$(basename "$DWIN_SET_PATH")")
            mv "$(dirname "$DWIN_SET_PATH")/DWIN_SET.zip" "$dwin_zip"
        elif [ "$DRY_RUN" = "true" ]; then
            echo "DRY RUN: Would create DWIN_SET.zip from $DWIN_SET_PATH"
        else
            cat > "$display_dir/CR-6-Touchscreen-Download.url" <<EOF
[InternetShortcut]
URL=https://github.com/CR6Community/CR-6-touchscreen
IconFile=https://github.com/favicon.ico
IconIndex=0
EOF
        fi
    else
        if [ -f "$config_dir/no-touchscreen.txt" ] && [ "$DRY_RUN" != "true" ]; then
            cp "$config_dir/no-touchscreen.txt" "$display_dir/"
        fi
    fi
    if [ -f "$config_dir/description.txt" ]; then
        cp "$config_dir/description.txt" "$build_output_dir/"
    else
        echo "Configuration: $config_name" > "$build_output_dir/description.txt"
        echo "Platform: $platform_env" >> "$build_output_dir/description.txt"
        echo "Built: $TIMESTAMP" >> "$build_output_dir/description.txt"
    fi
    if [ "$DRY_RUN" != "true" ]; then
        cat > "$build_output_dir/CR6Community-Marlin-Repository.url" << EOF
[InternetShortcut]
URL=https://github.com/Thinkersbluff/CR6Community-Marlin_TB
IconFile=https://github.com/favicon.ico
IconIndex=0
EOF
        local zip_file="$OUTPUT_DIR/$RELEASE_NAME-$config_name-$TIMESTAMP.zip"
        (cd "$build_output_dir" && zip -r "$zip_file" .)
        local sha256=$(sha256sum "$zip_file" | cut -d' ' -f1)
        echo "$sha256  $(basename "$zip_file")" >> "$OUTPUT_DIR/checksums.txt"
        echo "Created: $(basename "$zip_file")"
        echo "SHA256: $sha256"
    fi
    echo "Completed: $config_name"
    echo "Build output available in: $build_output_dir"
}

# Backup user's original Marlin/Configuration*.h files
ORIG_CONFIG_H="$REPO_ROOT/Marlin/Configuration.h"
ORIG_CONFIG_ADV_H="$REPO_ROOT/Marlin/Configuration_adv.h"
ORIG_CONFIG_H_BAK="$REPO_ROOT/Marlin/Configuration.h.userbak"
ORIG_CONFIG_ADV_H_BAK="$REPO_ROOT/Marlin/Configuration_adv.h.userbak"
cp "$ORIG_CONFIG_H" "$ORIG_CONFIG_H_BAK"
cp "$ORIG_CONFIG_ADV_H" "$ORIG_CONFIG_ADV_H_BAK"

if [ -n "$SINGLE_BUILD" ]; then
    build_config "$SINGLE_BUILD"
else
    for config in "${CONFIGS[@]}"; do
        build_config "$config"
    done
fi

cp "$ORIG_CONFIG_H_BAK" "$ORIG_CONFIG_H"
cp "$ORIG_CONFIG_ADV_H_BAK" "$ORIG_CONFIG_ADV_H"
rm -f "$ORIG_CONFIG_H_BAK" "$ORIG_CONFIG_ADV_H_BAK"
