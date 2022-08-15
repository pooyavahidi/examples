#!/bin/sh

# Use macos keychain to keep the awscli credentials instead of a plain text file.
# Each env variable must be kept in a separate line.
function dsh-awscli-auth-keychain {
    local __access_key_id
    local __secret_access_key
    local __creds
    local __keychain_item_name
    local __image_name
    local __env_file

    # Validations
    __keychain_item_name=$1
    [[ -z $__keychain_item_name ]] && echo "Keychain item name is missing" \
        && return 1

    __image_name=$2
    [[ -z $__image_name ]] && __image_name=pv/awscli-shell

    __env_file=$3
    [[ -z $__env_file ]] && echo "env file is missing" \
        && return 1

    __creds=$(_keychain_get_password ${__keychain_item_name})
    __access_key_id=$(echo $__creds | awk 'FNR==1')
    __secret_access_key=$(echo $__creds | awk 'FNR==2')

    docker run -it --rm \
        --name dsh-awscli-auth-${__keychain_item_name} \
        -v ${WORKSPACE}:/home/dev/workspace \
        --env $__access_key_id \
        --env $__secret_access_key \
        --env AWS_DEFAULT_REGION=us-east-1 \
        --env AWS_DEFAULT_OUTPUT=json \
        --env-file $__env_file \
        --hostname dsh-awscli-auth-${__keychain_item_name} \
        ${__image_name}
}

function dsh-awscli-docker {
    local __name
    local __image_name
    __name="awscli-docker"

    __image_name=$1
    [[ -z $__image_name ]] && __image_name=pv/awscli-shell

    docker run -it --rm --name $__name \
        -v ${WORKSPACE}:/home/dev/workspace \
        -v /var/run/docker.sock:/var/run/docker.sock \
        --hostname $__name \
        ${__image_name}
}
