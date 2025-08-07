FROM python:3.9.0-buster

# Create a user that matches the host user
RUN groupadd -g 1000 user && \
    useradd -u 1000 -g 1000 -m -s /bin/bash user && \
    mkdir -p /home/user/.platformio && \
    chown -R user:user /home/user

RUN pip install -U https://github.com/platformio/platformio-core/archive/develop.zip
RUN platformio update
# To get the test platforms
RUN pip install PyYaml

# Make sure the user can run platformio
RUN chown -R user:user /usr/local/lib/python3.9/site-packages/platformio*
RUN chown -R user:user /usr/local/bin/platformio /usr/local/bin/pio

# Switch to the user
USER user
WORKDIR /home/user
