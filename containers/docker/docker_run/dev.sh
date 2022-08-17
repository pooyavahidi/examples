#!/bin/sh

function d-dev-shell() {
    docker container run -it --name dev \
        -p 5000:5000 \
        -v ${WORKSPACE}:/home/dev/workspace \
        --hostname dev-shell \
        pv/dev-shell:latest \
        zsh
}
