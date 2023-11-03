#!/bin/bash

# Immediately catch all errors
set -eo pipefail

# Uncomment for debugging
# set -x
# env

# Enable autocomplete for user
cp /etc/skel/.bashrc ~/

python -m pytest --cov --cov-branch --cov-report xml:coverage.xml --cov-config setup.cfg
