#!/bin/sh

function d-dev() {
    # Try to to attach to `dev` container if exists. If not, create one.
    if ! docker::container_attach dev 2> /dev/null; then
        echo "Container doesn't exist, creating one..."

        docker container run -it --name dev \
            -p 5001:5001 \
            -v ${WORKSPACE}:/home/dev/workspace \
            --hostname dev-shell \
            ${DOCKER_LOCAL_REGISTRY}/dev-shell:latest
    fi
}
