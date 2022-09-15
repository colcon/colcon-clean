FROM python:3

WORKDIR /usr/src/app

COPY setup.cfg setup.py ./
COPY colcon_clean/__init__.py ./colcon_clean/__init__.py
RUN pip install -e .[test]

COPY . .
RUN pip install -e .[test]

RUN colcon build \
        --symlink-install

RUN colcon test && \
    colcon test-result --verbose
