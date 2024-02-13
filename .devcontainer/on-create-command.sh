#!/bin/bash

# Immediately catch all errors
set -eo pipefail

# Uncomment for debugging
# set -x
# env

git config --global --add safe.directory "*"

CONSTRAINTS_URL=https://raw.githubusercontent.com/colcon/ci/main/constraints.txt
CONSTRAINTS_FILE=/tmp/constraints.txt

# Download constraints
curl -sSLo $CONSTRAINTS_FILE $CONSTRAINTS_URL
# Remove this package from constraints
sed -i "/^$(python setup.py --name)@/d" $CONSTRAINTS_FILE
# Install dependencies, including any 'test' extras, as well as pytest-cov
pip install -U -e .[test] pytest-cov -c $CONSTRAINTS_FILE
