ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Add the root directory to git safe directories.
RUN git config --global --add safe.directory '/workspace'

# Upgrade pip
RUN pip install -U pip

# Install python packages
RUN pip install --upgrade \
    pytest \
    pycodestyle
