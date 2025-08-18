
FROM python:3.9.0-buster

# Allow dynamic UID/GID via build args
ARG USER_ID=1000
ARG GROUP_ID=1000

# Create a user that matches the host user
RUN groupadd -g ${GROUP_ID} user && \
    useradd -u ${USER_ID} -g ${GROUP_ID} -m -s /bin/bash user && \
    mkdir -p /home/user/.platformio && \
    chown -R user:user /home/user


RUN pip install -U https://github.com/platformio/platformio-core/archive/develop.zip
# To get the test platforms
RUN pip install PyYaml
# Pre-install PlatformIO platform and framework for STM32
USER user
RUN platformio pkg install -g --platform ststm32
USER root

# Make sure the user can run platformio
RUN chown -R user:user /usr/local/lib/python3.9/site-packages/platformio*
RUN chown -R user:user /usr/local/bin/platformio /usr/local/bin/pio

# Add user to root group for group write access
RUN usermod -aG root user

# Switch to the user
USER user
WORKDIR /home/user