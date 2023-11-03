#!/bin/bash

# Immediately catch all errors
set -eo pipefail

# Uncomment for debugging
# set -x
# env

# Download constraints
curl -sSLo constraints.txt https://raw.githubusercontent.com/colcon/ci/main/constraints.txt
# Remove this package from constraints
sed -i "/^$(python setup.py --name)@/d" constraints.txt
# Install dependencies, including any 'test' extras, as well as pytest-cov
python -m pip install -U -e .[test] pytest-cov -c constraints.txt
