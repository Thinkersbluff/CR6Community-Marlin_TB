FROM python:3.9-bullseye

# Create a user that matches the host user
RUN groupadd -g 1000 user && \
    useradd -u 1000 -g 1000 -m -s /bin/bash user && \
    mkdir -p /home/user/.platformio && \
    chown -R user:user /home/user




RUN python3 -m pip install --upgrade pip

RUN pip install platformio==6.1.18
# Do not auto-update PlatformIO; keep version fixed for reproducibility
# To get the test platforms
RUN pip install PyYaml

# Make sure the user can run platformio
RUN chown -R user:user /usr/local/lib/python3.9/site-packages/platformio*
RUN chown -R user:user /usr/local/bin/platformio /usr/local/bin/pio

# Switch to the user
USER user
WORKDIR /home/user
