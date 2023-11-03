#!/bin/bash

# Immediately catch all errors
set -eo pipefail

# Uncomment for debugging
# set -x
# env

git config --global --add safe.directory "*"

# VENV=./
# python -m venv $VENV
# if [ -f $VENV/Scripts/activate ]; then
#     . $VENV/Scripts/activate
# else
#     . $VENV/bin/activate
# fi
python -m pip install -U pip setuptools

# .devcontainer/update-content-command.sh
