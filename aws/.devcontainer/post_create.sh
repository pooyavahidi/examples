#!/bin/bash

# postCreateCommand to run inside the container for the first time it's created.
pip install --upgrade boto3
pip install --upgrade cryptography