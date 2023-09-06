ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN sudo apt-get update \
    && sudo apt-get install -y \
    curl \
    gpg \
    lsb-release

# Add the root directory to git safe directories.
RUN git config --global --add safe.directory '/workspace'

# Install Redis using official instructions:
# https://redis.io/docs/getting-started/installation/install-redis-on-linux/
RUN curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list \
    && sudo apt-get update \
    && sudo apt-get install -y redis

RUN pip install -U pip

# Install pythong packages.
RUN pip install --upgrade \
    pytest \
    pydantic \
    redis
