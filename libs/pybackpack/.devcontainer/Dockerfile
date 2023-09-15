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
    && sudo apt-get install -y redis \
    && redis-cli --version

# Install mongosh using official instructions:
# https://www.mongodb.com/docs/mongodb-shell/install/
RUN wget -qO- https://www.mongodb.org/static/pgp/server-7.0.asc | sudo tee /etc/apt/trusted.gpg.d/server-7.0.asc \
    && echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list \
    && sudo apt-get update \
    && sudo apt-get install -y mongodb-mongosh \
    && mongosh --version

# Upgrade pip.
RUN pip install -U pip

# Install development packages.
RUN pip install --upgrade \
    pytest \
    pycodestyle

# Install requirements.
COPY ../requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt