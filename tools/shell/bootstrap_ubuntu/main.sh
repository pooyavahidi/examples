#!/bin/bash
#
# This script installs basic packages and tools which are required for development.

#######################################
# Install prerequisite tools and packages
#######################################
function install_prerequisites() {
  sudo apt update; \
  sudo apt install -y \
        dirmngr \
        curl \
        git \
        gnupg \
        python3 \
        python3-venv \
        python3-pip \
        rsync \
        tree \
        tmux \
        unzip \
        vim \
        wget \
        zsh \
        xz-utils; \
    pip3 install -U \
        pylint \
        pycodestyle \
        black \
        git-remote-codecommit; \
    \
    # Create workspace directories and clone git repos.
    mkdir -p $HOME/workspace/temp; \
    cd $HOME/workspace; \
    git clone https://github.com/pooyavahidi/dotfiles; \
    git clone https://github.com/pooyavahidi/docker-library; \
    \
    # bootstrap the dotfile.
    cd $HOME/workspace/dotfiles; \
    ./bootstrap.sh; \
    cd $HOME; \
    \
    # Change shell to zsh
    sudo chsh $USER -s $(which zsh);
}

#######################################
# Install awscli v2
#######################################
function install_awscli() {
    cd $HOME/workspace/temp; \
    dpkgArch=$(dpkg --print-architecture); \
    case "${dpkgArch##-}" in \
        "amd64") \
            url="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"; \
            ;; \
        "arm64") \
            url="https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"; \
            ;; \
        *) echo "error: unsupported architecture ${dpkgArch}"; exit 1 ;; \
    esac; \
    wget -O awscliv2.zip "${url}" --progress=dot:giga; \
    wget -O awscliv2.zip.sig "${url}.sig" --progress=dot:giga; \
    \
    # Verify the signature of downloaded packages
    gpg --import $HOME/workspace/docker-library/awscli/debian/awscli_public_key; \
    gpg --verify awscliv2.zip.sig awscliv2.zip; \
    unzip -oq awscliv2.zip; \
    sudo ./aws/install --update; \
    rm awscliv2.zip awscliv2.zip.sig awscli_public_key; \
    rm -rf aws; \
    aws --version;
}

#######################################
# Install golang
#######################################
function install_golang() {
    export GOLANG_VERSION=1.19.1; \
    dpkgArch=$(dpkg --print-architecture); \
    case "${dpkgArch##-}" in \
        "amd64") \
            url="https://dl.google.com/go/go${GOLANG_VERSION}.linux-amd64.tar.gz"; \
            sha256="acc512fbab4f716a8f97a8b3fbaa9ddd39606a28be6c2515ef7c6c6311acffde"; \
            ;; \
        "arm64") \
            url="https://dl.google.com/go/go${GOLANG_VERSION}.linux-arm64.tar.gz"; \
            sha256="49960821948b9c6b14041430890eccee58c76b52e2dbaafce971c3c38d43df9f"; \
            ;; \
        *) echo "error: unsupported architecture ${dpkgArch}"; exit 1 ;; \
    esac; \
    wget -O go.tgz.asc "${url}.asc" --progress=dot:giga; \
    wget -O go.tgz "${url}" --progress=dot:giga; \
    echo "$sha256 *go.tgz" | sha256sum --strict --check -; \
    \
    export GNUPGHOME="$(mktemp -d)"; \
    # Verify the signature of downloaded packages
    # https://www.google.com/linuxrepositories/
    gpg --batch --keyserver keyserver.ubuntu.com --recv-keys 'EB4C 1BFD 4F04 2F6D DDCC EC91 7721 F63B D38B 4796'; \
    gpg --batch --verify go.tgz.asc go.tgz; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" go.tgz.asc; \
    \
    sudo tar -C /usr/local -xzf go.tgz; \
    rm go.tgz; \
    \
    # Verify installation and set the environment variables.
    /usr/local/go/bin/go version; \
    echo 'export GOPATH="$HOME/go"' >> ${HOME}/.extra; \
    echo 'export PATH="/usr/local/go/bin:$GOPATH/bin:$PATH"' >> ${HOME}/.extra
}

#######################################
# Install Docker
#######################################
function install_docker() {
    sudo apt-get update; \
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release; \
    mkdir -p /etc/apt/keyrings; \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null; \

    sudo apt-get update; \
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin; \
    \
    # Setup docker user and group
    sudo usermod -aG docker $USER; \
    docker --version; \
    docker compose version;
}

#######################################
# Install nodejs
#######################################
function install_nodejs() {
    # Using official script at https://github.com/nodejs/docker-node/blob/main/16/bullseye/Dockerfile
    export NODE_VERSION=16.17.1 \
    && ARCH= && dpkgArch="$(dpkg --print-architecture)" \
    && case "${dpkgArch##*-}" in \
      amd64) ARCH='x64';; \
      ppc64el) ARCH='ppc64le';; \
      s390x) ARCH='s390x';; \
      arm64) ARCH='arm64';; \
      armhf) ARCH='armv7l';; \
      i386) ARCH='x86';; \
      *) echo "unsupported architecture"; exit 1 ;; \
    esac \
    && for key in \
      4ED778F539E3634C779C87C6D7062848A1AB005C \
      141F07595B7B3FFE74309A937405533BE57C7D57 \
      94AE36675C464D64BAFA68DD7434390BDBE9B9C5 \
      74F12602B6F1C4E913FAA37AD3A89613643B6201 \
      71DCFD284A79C3B38668286BC97EC7A07EDE3FC1 \
      61FC681DFB92A079F1685E77973F295594EC4689 \
      8FCCA13FEF1D0C2E91008E09770F7A9A5AE15600 \
      C4F0DFFF4E8C1A8236409D08E73BC641CC11F4C8 \
      890C08DB8579162FEE0DF9DB8BEAB4DFCF555EF4 \
      C82FA3AE1CBEDC6BE46B9360C43CEC45C17AB93C \
      DD8F2338BAE7501E3DD5AC78C273792F7D83545D \
      A48C2BEE680E841632CD4E44F07496B3EB3C1762 \
      108F52B48DB57BB0CC439B2997B01419BD92F80A \
      B9E2F5981AA6E0CD28160D9FF13993A75599653C \
    ; do \
        gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$key" || \
        gpg --batch --keyserver keyserver.ubuntu.com --recv-keys "$key" ; \
    done \
    && cd ${HOME}/workspace/temp \
    && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION-linux-$ARCH.tar.xz" \
    && curl -fsSLO --compressed "https://nodejs.org/dist/v$NODE_VERSION/SHASUMS256.txt.asc" \
    && gpg --batch --decrypt --output SHASUMS256.txt SHASUMS256.txt.asc \
    && grep " node-v$NODE_VERSION-linux-$ARCH.tar.xz\$" SHASUMS256.txt | sha256sum -c - \
    && sudo tar -xJf "node-v$NODE_VERSION-linux-$ARCH.tar.xz" -C /usr/local --strip-components=1 --no-same-owner \
    && rm "node-v$NODE_VERSION-linux-$ARCH.tar.xz" SHASUMS256.txt.asc SHASUMS256.txt \
    && sudo ln -s /usr/local/bin/node /usr/local/bin/nodejs \
    && node --version \
    && npm --version

}

#######################################
# Install awscdk
########################################
function install_awscdk() {
    sudo npm -g install typescript; \
    sudo npm -g install aws-cdk; \
    cdk --version;
}

#########################################
# Run the functions in order
# Arguments:
#   command line
########################################
function main() {
    export DEBIAN_FRONTEND=noninteractive

    # Keep track of starting directory to get back to it after the installations.
    __starting_dir=$(pwd)

    set -eux
    install_prerequisites
    install_awscli
    install_golang
    install_nodejs
    install_awscdk
    install_docker

    # Final update and upgrade
    sudo apt update && sudo apt upgrade -y

    # Summary of all installations.
    python3 --version
    pip3 --version
    aws --version
    go version
    nodejs --version
    npm --version
    tsc --verison
    cdk --version
    docker --version
    docker compose version

    set +x
    # Go back to the starting directory
    cd $__starting_dir

    echo --------------------------
    echo Reboot before using
}

main "${@}"

