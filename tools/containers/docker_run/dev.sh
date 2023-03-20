#!/bin/sh

function d-dev-shell() {
    # Try to to attach to `dev` container if exists. If not, create one.

    if ! docker::container_attach dev; then
        echo Creating container...
        docker container run -it --name dev \
            -p 5001:5001 \
            -v ${WORKSPACE}:/home/dev/workspace \
            --hostname dev-shell \
            pv/dev-shell:latest \
            zsh
    fi
}
