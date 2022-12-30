#!/usr/bin/env bash

# Using this shell script we can control the entrypoint for the container.

# Get the updated version of the repo each time
git clone https://github.com/pooyavahidi/examples
cd examples/python/cryptography

if [[ $# > 0 ]]; then
    # If input parameters (container commands) have been passed, run them.
    exec $@
else
    # If no input parameters have been passed, run the default executable
    # which in this example is a kdf calculation.
    python key_derivation_function.py
fi