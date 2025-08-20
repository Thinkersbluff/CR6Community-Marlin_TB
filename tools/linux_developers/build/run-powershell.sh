#!/bin/bash
# PowerShell wrapper script for Linux
# Usage: ./run-powershell.sh script.ps1 [arguments]

if [ $# -eq 0 ]; then
    echo "Usage: $0 <powershell-script.ps1> [arguments...]"
    echo "Example: $0 tools/windows_developers/build/Run-ExampleConfigBuilds.ps1 -ReleaseName test"
    exit 1
fi

SCRIPT_PATH="$1"
shift  # Remove first argument (script path) from $@

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: PowerShell script '$SCRIPT_PATH' not found"
    exit 1
fi

echo "Running PowerShell script: $SCRIPT_PATH"
echo "Arguments: $@"
echo ""

# Run PowerShell script in podman container
podman run --rm \
    -v "$(pwd):/workspace" \
    -w /workspace \
    mcr.microsoft.com/powershell:latest \
    pwsh -ExecutionPolicy Unrestricted -File "$SCRIPT_PATH" "$@"
