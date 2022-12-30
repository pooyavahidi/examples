FROM python:latest

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip3 install cryptography

COPY entrypoint.sh .

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]