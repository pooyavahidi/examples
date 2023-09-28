#!/bin/sh

# functions to run, build and develop websites using gohugo
function d-hugo-server() {
    local __hugo_workspace
    __hugo_workspace=$1

    [[ -z $1 ]] && __hugo_workspace=$(pwd)

    docker container run --rm -p 1313:1313 \
        -v $__hugo_workspace:/home/dev/workspace \
        ${DOCKER_LOCAL_REGISTRY}/hugo:latest \
        hugo -D server -s workspace --bind 0.0.0.0
}

function d-hugo() {
    local __hugo_workspace
    __hugo_workspace=$1

    [[ -z $1 ]] && __hugo_workspace=$(pwd)

    docker container run -it --rm -p 1314:1313 \
        -v $__hugo_workspace:/home/dev/workspace \
        ${DOCKER_LOCAL_REGISTRY}/hugo:latest
}

function d-hugo-build {
    local __hugo_workspace
    __hugo_workspace=$1
    [[ -z $1 ]] && __hugo_workspace=$(pwd)

    docker container run --rm \
        -v $__hugo_workspace:/home/dev/workspace \
        ${DOCKER_LOCAL_REGISTRY}/hugo:latest \
        hugo -s workspace

}
