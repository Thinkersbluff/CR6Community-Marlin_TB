# Reasons for this project:

1. The build-configs.sh script does not work correctly on docker containers, but an equivalent script designed to run on the local system (build-configs-local.sh) works fine.
This infers that the problem is with the containerized environment, not with the Marlin files or the Platformio or Python tools
By migrating from Docker to Podman, we hope to create a more reliable solution for running compilations in a containerized environment.
