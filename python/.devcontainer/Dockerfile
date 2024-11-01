ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN sudo apt-get update \
    && sudo apt-get install -y \
    build-essential \
    curl \
    gpg \
    lsb-release

RUN conda init zsh

RUN python -m pip install --upgrade pip

RUN pip install --upgrade \
    boto3 \
    pydantic
