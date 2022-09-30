#!/bin/bash
#
# This script installs basic packages and tools which are required for development.

#######################################
# Install prerequisite tools and packages
#######################################
function install_prerequisites() {
  set -eux; \
  sudo apt update; \
  sudo apt install -y \
        dirmngr \
        curl \
        gnupg \
        git \
        python3 \
        python3-venv \
        python3-pip \
        rsync \
        tree \
        unzip \
        vim \
        wget \
        zsh; \
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
    set -eux; \
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
    aws --version;
}


#######################################
# Install golang
#######################################
function install_golang() {
    set -eux; \
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
# Arguments:
#   None
########################################
function install_docker() {

    set -eux; \
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

#########################################
# Run the functions in order
# Arguments:
#   command line
########################################
function main() {
  export DEBIAN_FRONTEND=noninteractive

  install_prerequisites
  install_awscli
  install_golang
  install_docker

  # Final update and upgrade
  sudo apt update && sudo apt upgrade -y

  echo --------------------------
  echo zsh shell will be active from next login
}

main "${@}"
