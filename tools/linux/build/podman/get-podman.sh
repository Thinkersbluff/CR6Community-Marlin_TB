#!/bin/sh
set -e
# Podman and podman-compose installation script for Linux
#
# This script attempts to install Podman and podman-compose using the system package manager.
# It supports Debian/Ubuntu, Fedora, CentOS, RHEL, and openSUSE.
#
# Usage:
#   curl -fsSL <URL_TO_THIS_SCRIPT> -o get-podman.sh
#   sudo sh get-podman.sh
#
# For more details, see:
#   https://podman.io/getting-started/installation
#   https://github.com/containers/podman-compose

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if command_exists podman && command_exists podman-compose; then
    echo "Podman and podman-compose are already installed."
    exit 0
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    VERSION_ID=$VERSION_ID
else
    echo "Cannot detect OS. Please install podman and podman-compose manually."
    exit 1
fi

install_podman_debian() {
    sudo apt-get update
    sudo apt-get install -y podman
    # podman-compose may not be in all repos, so use pip as fallback
    if apt-cache show podman-compose >/dev/null 2>&1; then
        sudo apt-get install -y podman-compose
    else
        sudo apt-get install -y python3-pip
        sudo pip3 install --upgrade pip
        sudo pip3 install podman-compose
    fi
}

install_podman_fedora() {
    sudo dnf -y install podman podman-compose
}

install_podman_centos() {
    sudo yum -y install podman
    # podman-compose may not be in repos, so use pip
    sudo yum -y install python3-pip
    sudo pip3 install --upgrade pip
    sudo pip3 install podman-compose
}

install_podman_opensuse() {
    sudo zypper --non-interactive install podman podman-compose
}

case "$OS" in
    ubuntu|debian)
        install_podman_debian
        ;;
    fedora)
        install_podman_fedora
        ;;
    centos|rhel)
        install_podman_centos
        ;;
    opensuse*|suse)
        install_podman_opensuse
        ;;
    *)
        echo "Unsupported OS: $OS. Please install podman and podman-compose manually."
        exit 1
        ;;
esac

echo "Podman and podman-compose installation complete."
