#!/bin/bash
# Linux equivalent of Run-ExampleConfigBuilds.ps1
# Builds multiple configuration examples and packages them for release

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
    
    echo "=== Building $config_name ==="
    
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
    
    # Check for touchscreen support
    local has_touchscreen=true
    if [ -f "$config_dir/no-touchscreen.txt" ]; then
        has_touchscreen=false
        echo "Configuration excludes touchscreen firmware"
    fi
    
    if [ "$DRY_RUN" != "true" ]; then
        echo "Building firmware..."
        
        # Use Docker to build with proper environment
        docker-compose run --rm -e PLATFORM_ENV="$platform_env" marlin bash -c "
            set -e
            cd /code
            echo 'Applying configuration: $config_name'
            cp $config_dir/Configuration*.h Marlin/
            
            echo 'Updating platformio.ini default_envs to: '\$PLATFORM_ENV
            sed -i 's/^default_envs = .*/default_envs = '\$PLATFORM_ENV'/' platformio.ini
            
            # For BTT boards, ensure correct motherboard selection
            if [[ \$PLATFORM_ENV == *'btt'* ]]; then
                echo 'Applying BTT board configuration...'
                # Ensure board is set correctly for BTT environment
                sed -i 's/^[[:space:]]*#define[[:space:]]*MOTHERBOARD[[:space:]]*BOARD_CREALITY_V453/#define MOTHERBOARD BOARD_BTT_SKR_CR6/' Marlin/Configuration.h
                sed -i 's/^[[:space:]]*#define[[:space:]]*MOTHERBOARD[[:space:]]*BOARD_CREALITY_V452/#define MOTHERBOARD BOARD_BTT_SKR_CR6/' Marlin/Configuration.h
                sed -i 's/^[[:space:]]*#define[[:space:]]*MOTHERBOARD[[:space:]]*BOARD_CREALITY_V427/#define MOTHERBOARD BOARD_BTT_SKR_CR6/' Marlin/Configuration.h
                echo 'BTT board configuration applied'
            fi
            
            echo 'Building firmware for platform: '\$PLATFORM_ENV
            platformio run -e \$PLATFORM_ENV --target clean
            platformio run -e \$PLATFORM_ENV
            
            echo 'Build completed successfully'
        "
        
        if [ $? -ne 0 ]; then
            echo "ERROR: Build failed for $config_name"
            return 1
        fi
        
        # Copy firmware binary
        local firmware_files=($(find "$REPO_ROOT/.pio/build/$platform_env" -name "firmware*.bin" 2>/dev/null))
        if [ ${#firmware_files[@]} -eq 0 ]; then
            echo "ERROR: No firmware binary found for $config_name"
            return 1
        fi
        
        cp "${firmware_files[0]}" "$firmware_dir/"
        echo "Firmware copied: $(basename "${firmware_files[0]}")"
        
    else
        echo "DRY RUN: Would build $config_name with platform $platform_env"
    fi
    
    # Copy configuration files
    cp "$config_dir"/*.h "$config_copy_dir/" 2>/dev/null || true
    
    # Handle touchscreen/display firmware
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
            cat > "$display_dir/CR-6-Touchscreen-Download.url" << EOF
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
        
        if [ "$DRY_RUN" != "true" ]; then
            echo "Configuration uses BTT TFT - no CR-6 touchscreen firmware needed"
        fi
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
        cat > "$OUTPUT_DIR/CR6Community-Marlin-Repository.url" << EOF
[InternetShortcut]
URL=https://github.com/Thinkersbluff/CR6Community-Marlin_TB
IconFile=https://github.com/favicon.ico
IconIndex=0
EOF
        
        # Create ZIP file including both the build directory and the URL file
        local zip_file="$OUTPUT_DIR/$RELEASE_NAME-$config_name-$TIMESTAMP.zip"
        (cd "$OUTPUT_DIR" && zip -r "$(basename "$zip_file")" "$(basename "$build_output_dir")" "CR6Community-Marlin-Repository.url")
        
        # Generate SHA256
        local sha256=$(sha256sum "$zip_file" | cut -d' ' -f1)
        echo "$sha256  $(basename "$zip_file")" >> "$OUTPUT_DIR/checksums.txt"
        
        echo "Created: $(basename "$zip_file")"
        echo "SHA256: $sha256"
    fi
    
    echo "Completed: $config_name"
    echo ""
}

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

# Restore original configuration
echo "Restoring original configuration..."
docker-compose run --rm marlin bash -c "cd /code && git checkout HEAD -- Marlin/Configuration*.h platformio.ini"

echo ""
echo "=== Build Summary ==="
if [ -f "$OUTPUT_DIR/checksums.txt" ]; then
    echo "Built packages:"
    cat "$OUTPUT_DIR/checksums.txt"
else
    echo "No packages built (dry run or errors occurred)"
fi

echo ""
echo "Build script completed!"
echo "Output directory: $OUTPUT_DIR"
