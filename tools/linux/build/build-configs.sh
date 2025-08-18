#!/bin/bash
# ============================================================================
# CR6Community-Marlin_TB Multi-Config Build Script
# ----------------------------------------------------------------------------
# This script automates building, packaging, and archiving Marlin firmware for
# multiple board/configuration targets in the CR6Community-Marlin_TB repository.
#
# It is the Linux equivalent of Run-ExampleConfigBuilds.ps1
#
# Features:
#   - Scans all valid config/* directories for buildable configurations
#   - Backs up and restores your own Marlin/Configuration*.h files
#   - Copies config-specific Configuration.h/adv.h and builds with PlatformIO (via podman)
#   - Captures all build output and errors with timestamps
#   - Packages firmware and (optionally) touchscreen firmware for each config
#   - Creates per-build logs, checksums, and ZIP archives for easy release
#
# Requirements:
#   - Must be run from within the CR6Community-Marlin_TB repository (any subdir)
#   - podman and podman-compose must be installed and working
#   - The repo must have a valid platformio.ini and config/*/platformio-environment.txt files
#
# Usage Examples:
#   ./build-configs.sh my_release_name
#     - Builds all valid configs, output in .pio/build-output/my_release_name-*
#
#   ./build-configs.sh my_release_name btt-skr-cr6-with-btt-tft
#     - Builds only the specified config (by directory name)
#
#   ./build-configs.sh my_release_name "" true
#     - Dry run: shows what would be built, but does not actually build
#
#   ./build-configs.sh my_release_name "" false /path/to/CR-6-Touchscreen
#     - Uses a custom path for the touchscreen repo
#
# Output:
#   - Firmware, logs, and ZIPs in .pio/build-output/
#   - Original Marlin/Configuration*.h always restored after build
# ============================================================================

# Redirect all output to build_log with timestamps
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_LOG="$SCRIPT_DIR/build_log"
if command -v ts >/dev/null 2>&1; then
    exec > >(ts '%Y-%m-%d %H:%M:%S' | tee "$BUILD_LOG") 2>&1
else
    exec > >(awk '{ print strftime("%Y-%m-%d %H:%M:%S"), $0; fflush(); }' | tee "$BUILD_LOG") 2>&1
fi

# Auto-detect repository root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR" && git rev-parse --show-toplevel 2>/dev/null)"

if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/platformio.ini" ]; then
    echo "ERROR: Could not detect repository root or not in a Marlin repository"
    echo "This script must be run from within the CR6Community-Marlin repository"
    exit 1
fi

echo "Repository root detected: $REPO_ROOT"
cd "$REPO_ROOT"
export REPO_ROOT="$(realpath "$REPO_ROOT")"

RELEASE_NAME="${1:-test-build}"
SINGLE_BUILD="${2:-}"
DRY_RUN="${3:-}"
TOUCHSCREEN_REPO_PATH="${4:-../CR-6-Touchscreen}"

OUTPUT_DIR="$REPO_ROOT/.pio/build-output"
TIMESTAMP=$(date +%Y-%m-%d-%H-%M)

echo "=== CR6 Community Firmware Build Script ==="
echo "Release Name: $RELEASE_NAME"
echo "Timestamp: $TIMESTAMP"
echo "Touchscreen Repo: $TOUCHSCREEN_REPO_PATH"
echo ""

# Check for touchscreen DWIN_SET folder
DWIN_SET_PATH="$TOUCHSCREEN_REPO_PATH/src/DWIN/DWIN_SET"
TOUCHSCREEN_AVAILABLE=false

if [ -d "$DWIN_SET_PATH" ]; then
    echo "=== Touchscreen DWIN_SET Found ==="
    echo "DWIN_SET folder located at: $DWIN_SET_PATH"
    TOUCHSCREEN_AVAILABLE=true
else
    echo "=== Touchscreen DWIN_SET Not Found ==="
    echo "DWIN_SET folder not found at: $DWIN_SET_PATH"
    echo "Will create URL shortcut instead"
fi
echo ""

# Clean output directory
if [ -d "$OUTPUT_DIR" ]; then
    echo "Cleaning previous build output..."
    rm -rf "$OUTPUT_DIR"
fi
mkdir -p "$OUTPUT_DIR"

# Get list of available configurations (only those with required files)
echo "Scanning configurations..."
CONFIGS=()
for config_dir in "$REPO_ROOT/config/"*/; do
    config_name=$(basename "$config_dir")
    
    # Skip README.md and other non-config files
    if [ "$config_name" = "README.md" ]; then
        continue
    fi
    
    # Check for required files
    if [ ! -f "$config_dir/Configuration.h" ]; then
        echo "WARNING: Skipping $config_name - missing Configuration.h"
        continue
    fi
    
    if [ ! -f "$config_dir/Configuration_adv.h" ]; then
        echo "WARNING: Skipping $config_name - missing Configuration_adv.h"
        continue
    fi
    
    if [ ! -f "$config_dir/platformio-environment.txt" ]; then
        echo "WARNING: Skipping $config_name - missing platformio-environment.txt"
        continue
    fi
    
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
    local container_config_dir="/code/config/$config_name"
    

    echo "=== Building $config_name ==="

    # Check for no-autobuild flag before any hashing or copying
    if [ -f "$config_dir/no-autobuild.txt" ] && [ "$config_name" != "$SINGLE_BUILD" ]; then
        echo "Skipping $config_name (marked no-autobuild)"
        return 0
    fi

    # Hash before overwriting
    echo "[DEBUG] Hashing base Configuration*.h before overwrite..."
    HASH_BEFORE=$("$SCRIPT_DIR/hash-configs.sh")
    HASH_BEFORE_H=$(echo "$HASH_BEFORE" | grep CONFIG_H_SHA256 | cut -d'=' -f2)
    HASH_BEFORE_ADV=$(echo "$HASH_BEFORE" | grep CONFIG_ADV_H_SHA256 | cut -d'=' -f2)
    
    # Check if configuration exists
    if [ ! -d "$config_dir" ]; then
        echo "ERROR: Configuration directory not found: $config_dir"
        return 1
    fi
    
    # Get platform environment
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

    echo "Platform environment: $platform_env"
    
    # Check for no-autobuild flag
    if [ -f "$config_dir/no-autobuild.txt" ] && [ "$config_name" != "$SINGLE_BUILD" ]; then
        echo "Skipping $config_name (marked no-autobuild)"
        return 0
    fi
    
    # Create build output directory
    local build_output_dir="$OUTPUT_DIR/$RELEASE_NAME-$config_name-$TIMESTAMP"
    local firmware_dir="$build_output_dir/Firmware/Motherboard firmware"
    local display_dir="$build_output_dir/Firmware/Display Firmware"
    local config_copy_dir="$build_output_dir/configs"

    mkdir -p "$firmware_dir"
    mkdir -p "$display_dir"
    mkdir -p "$config_copy_dir"

    # Overwrite Marlin/Configuration*.h with config's files
    cp "$config_dir"/Configuration*.h "$REPO_ROOT/Marlin/"

    # Hash after overwriting
    echo "[DEBUG] Hashing base Configuration*.h after overwrite..."
    HASH_AFTER=$("$SCRIPT_DIR/hash-configs.sh")
    HASH_AFTER_H=$(echo "$HASH_AFTER" | grep CONFIG_H_SHA256 | cut -d'=' -f2)
    HASH_AFTER_ADV=$(echo "$HASH_AFTER" | grep CONFIG_ADV_H_SHA256 | cut -d'=' -f2)

    if [ "$HASH_BEFORE_H" = "$HASH_AFTER_H" ] && [ "$HASH_BEFORE_ADV" = "$HASH_AFTER_ADV" ]; then
        echo "WARNING: Configuration*.h hashes before and after overwrite are identical! The config files may not have been copied."
    fi
    
    # Check for touchscreen support
    local has_touchscreen=true
    if [ -f "$config_dir/no-touchscreen.txt" ]; then
        has_touchscreen=false
        echo "Configuration excludes touchscreen firmware"
    fi
    
    if [ "$DRY_RUN" != "true" ]; then
        echo "[DEBUG] Starting podman build for $config_name (platform_env: $platform_env)"
        BUILD_OUT_FILE="$build_output_dir/platformio-build.log"
        echo "[DEBUG] Invoking podman-compose for $config_name, output will be logged to $BUILD_OUT_FILE"

    # Write the build script to a temp file in $REPO_ROOT for robust execution (always mounted in container)
    BUILD_SCRIPT="$REPO_ROOT/podman-build-script.sh"
    cat > "$BUILD_SCRIPT" <<EOF
set -ex
echo 'DEBUG: Entered container, PWD='" $(pwd)"
cd /code
echo 'DEBUG: Listing files in $container_config_dir'
ls -l "$container_config_dir"
echo 'DEBUG: Listing Marlin/ before copy'
ls -l Marlin/
echo 'DEBUG: Copying $container_config_dir/Configuration*.h to Marlin/'
cp "$container_config_dir"/Configuration*.h Marlin/
echo 'DEBUG: Listing Marlin/ after copy'
ls -l Marlin/
echo "Updating platformio.ini default_envs to: \$PLATFORM_ENV"
sed -i "s/^default_envs = .*/default_envs = \$PLATFORM_ENV/" platformio.ini
echo "Building firmware for platform: \$PLATFORM_ENV"
if [ -z "\$PLATFORM_ENV" ]; then
    echo "ERROR: PLATFORM_ENV is not set. Aborting build."
    exit 2
fi
platformio run -e "\$PLATFORM_ENV" --target clean
platformio run -e "\$PLATFORM_ENV"
echo 'Build completed successfully'
EOF
        chmod +x "$BUILD_SCRIPT"
        sync
        if [ ! -f "$BUILD_SCRIPT" ]; then
            echo "ERROR: Build script $BUILD_SCRIPT was not created!"
            return 1
        fi
    podman-compose -f "$SCRIPT_DIR/podman/podman-compose.yml" run --rm -e PLATFORM_ENV="$platform_env" marlin bash "/code/podman-build-script.sh" &> "$BUILD_OUT_FILE"
        rm -f "$BUILD_SCRIPT"

        BUILD_RESULT=$?
        echo "[DEBUG] podman build finished for $config_name with exit code $BUILD_RESULT"
        cat "$BUILD_OUT_FILE"
        if [ $BUILD_RESULT -ne 0 ]; then
            echo "ERROR: Build failed for $config_name. See $BUILD_OUT_FILE for details."
            return 1
        fi

        # Copy the most recent firmware*.bin file (handles timestamped names)
        local firmware_file=$(ls -1t "$REPO_ROOT/.pio/build/$platform_env"/firmware*.bin 2>/dev/null | head -n1)
        if [ -z "$firmware_file" ]; then
            echo "ERROR: No firmware binary found for $config_name. See $BUILD_OUT_FILE for build output."
            return 1
        fi

        cp "$firmware_file" "$firmware_dir/"
        echo "Firmware copied: $(basename "$firmware_file")"
    else
        echo "DRY RUN: Would build $config_name with platform $platform_env"
    fi

    # Copy configuration files
    cp "$config_dir"/*.h "$config_copy_dir/" 2>/dev/null || true

    if [ "$has_touchscreen" = true ]; then
        if [ "$TOUCHSCREEN_AVAILABLE" = true ] && [ "$DRY_RUN" != "true" ]; then
            echo "Creating DWIN_SET.zip from touchscreen firmware..."
            # Create ZIP file of DWIN_SET folder
            local dwin_zip="$display_dir/DWIN_SET.zip"
            (cd "$(dirname "$DWIN_SET_PATH")" && zip -r "$(basename "$dwin_zip")" "$(basename "$DWIN_SET_PATH")")
            mv "$(dirname "$DWIN_SET_PATH")/DWIN_SET.zip" "$dwin_zip"
            echo "Display firmware packaged: DWIN_SET.zip"
        elif [ "$DRY_RUN" = "true" ]; then
            echo "DRY RUN: Would create DWIN_SET.zip from $DWIN_SET_PATH"
        else
            echo "Creating URL shortcut for touchscreen firmware download..."
            # Create URL shortcut file
            cat > "$display_dir/CR-6-Touchscreen-Download.url" <<EOF
[InternetShortcut]
URL=https://github.com/CR6Community/CR-6-touchscreen
IconFile=https://github.com/favicon.ico
IconIndex=0
EOF
            echo "Created download link: CR-6-Touchscreen-Download.url"
        fi
    else
        # Configuration excludes touchscreen - copy the no-touchscreen.txt file to explain
        if [ -f "$config_dir/no-touchscreen.txt" ] && [ "$DRY_RUN" != "true" ]; then
            cp "$config_dir/no-touchscreen.txt" "$display_dir/"
            echo "Copied no-touchscreen.txt to Display Firmware folder"
        elif [ "$DRY_RUN" = "true" ]; then
            echo "DRY RUN: Would copy no-touchscreen.txt to Display Firmware folder"
        fi
    fi
    
    if [ "$DRY_RUN" != "true" ]; then
        echo "Configuration uses BTT TFT - no CR-6 touchscreen firmware needed"
    fi
    
    # Copy description if available
    if [ -f "$config_dir/description.txt" ]; then
        cp "$config_dir/description.txt" "$build_output_dir/"
    else
        echo "Configuration: $config_name" > "$build_output_dir/description.txt"
        echo "Platform: $platform_env" >> "$build_output_dir/description.txt"
        echo "Built: $TIMESTAMP" >> "$build_output_dir/description.txt"
    fi
    
    if [ "$DRY_RUN" != "true" ]; then
    # Add repository URL shortcut at ZIP root level
    cat > "$build_output_dir/CR6Community-Marlin-Repository.url" << EOF
[InternetShortcut]
URL=https://github.com/Thinkersbluff/CR6Community-Marlin_TB
IconFile=https://github.com/favicon.ico
IconIndex=0
EOF

    # Create ZIP file with all contents of build_output_dir at the root
    local zip_file="$OUTPUT_DIR/$RELEASE_NAME-$config_name-$TIMESTAMP.zip"
    (cd "$build_output_dir" && zip -r "$zip_file" .)

    # Generate SHA256
    local sha256=$(sha256sum "$zip_file" | cut -d' ' -f1)
    echo "$sha256  $(basename "$zip_file")" >> "$OUTPUT_DIR/checksums.txt"

    echo "Created: $(basename "$zip_file")"
    echo "SHA256: $sha256"
    fi
    
    echo "Completed: $config_name"
    echo ""
    echo "Build output available in: $build_output_dir"
}

# Backup user's original Marlin/Configuration*.h files
ORIG_CONFIG_H="$REPO_ROOT/Marlin/Configuration.h"
ORIG_CONFIG_ADV_H="$REPO_ROOT/Marlin/Configuration_adv.h"
ORIG_CONFIG_H_BAK="$REPO_ROOT/Marlin/Configuration.h.userbak"
ORIG_CONFIG_ADV_H_BAK="$REPO_ROOT/Marlin/Configuration_adv.h.userbak"

cp "$ORIG_CONFIG_H" "$ORIG_CONFIG_H_BAK"
cp "$ORIG_CONFIG_ADV_H" "$ORIG_CONFIG_ADV_H_BAK"

# Main build loop
if [ -n "$SINGLE_BUILD" ]; then
    echo "Building single configuration: $SINGLE_BUILD"
    build_config "$SINGLE_BUILD"
else
    echo "Building all configurations..."
    for config in "${CONFIGS[@]}"; do
        build_config "$config"
    done
fi

# Restore user's original Configuration*.h files
echo "Restoring user's original Marlin/Configuration*.h files..."
cp "$ORIG_CONFIG_H_BAK" "$ORIG_CONFIG_H"
cp "$ORIG_CONFIG_ADV_H_BAK" "$ORIG_CONFIG_ADV_H"
rm -f "$ORIG_CONFIG_H_BAK" "$ORIG_CONFIG_ADV_H_BAK"
