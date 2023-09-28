
function d-conda() {
    # if container exists, attach, if not create one.
    if ! docker::container_attach conda 2> /dev/null; then
        echo "Container doesn't exist, creating one..."

        docker run -it --name conda \
            -p 8888:8888 \
            -v ${WORKSPACE}:/home/dev/workspace \
            --hostname anaconda \
            ${DOCKER_LOCAL_REGISTRY}/anaconda \
            /bin/zsh -c "conda init zsh 1> /dev/null && zsh"
    fi
}

function d-jupyter() {
    local __port

    [[ -z "${__port:=$1}" ]] && __port=8888

    docker run -it --rm \
        -p ${__port}:${__port} \
        -v $(pwd):/home/dev/workspace \
        ${DOCKER_LOCAL_REGISTRY}/anaconda \
        jupyter notebook \
            --notebook-dir=/home/dev/workspace --ip='*' \
            --port=${__port} --no-browser
}
