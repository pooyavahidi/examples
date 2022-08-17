#!/bin/sh

function d-hugo-run() {
    local __hugo_workspace
    __hugo_workspace=$1

    [[ -z $1 ]] && __hugo_workspace=$(pwd)

    docker container run --rm -p 1313:1313 \
        -v $__hugo_workspace:/home/dev/workspace \
        pv/hugo-shell:latest \
        hugo -D server -s workspace --bind 0.0.0.0
}

function d-hugo-shell() {
    local __hugo_workspace
    __hugo_workspace=$1

    [[ -z $1 ]] && __hugo_workspace=$(pwd)

    docker container run -it --rm -p 1314:1313 \
        -v $__hugo_workspace:/home/dev/workspace \
        pv/hugo-shell:latest \
        zsh
}

function d-hugo-build {
    local __hugo_workspace
    __hugo_workspace=$1
    [[ -z $1 ]] && __hugo_workspace=$(pwd)

    docker container run --rm \
        -v $__hugo_workspace:/home/dev/workspace \
        pv/hugo-shell:latest \
        hugo -s workspace

}
