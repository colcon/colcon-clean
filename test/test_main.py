# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import argparse
import os
from pathlib import Path
import shutil
import sys
from tempfile import mkdtemp

from colcon_core.command import main
import pytest


def test_main(monkeypatch):
    ws_base = Path(mkdtemp(prefix='test_colcon_'))
    resources_base = Path('test', 'resources').absolute()
    shutil.copytree(resources_base / 'test_src', ws_base / 'src')

    os.chdir(ws_base)
    argv = []
    os.environ['COLCON_EXTENSION_BLOCKLIST'] = (
        'colcon_core.event_handler.desktop_notification:' +
        os.environ.get('COLCON_EXTENSION_BLOCKLIST', ''))

    try:
        main(argv=argv + ['build'])

        # Clean all package base paths explicitly
        main(argv=argv + ['clean', 'packages', '--yes', \
            '--base-select', \
                'build', \
                'install', \
                'log', \
                'test_result', \
            '--packages-select', \
                'test-package-b', \
                'test-package-c'])  # noqa

        # Clean workspace build base paths of python files
        # And with duplicate match filters
        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'build', \
            '--clean-match', \
                '*.py', \
                '*.py'])  # noqa

        # Try again but with nothing left to clean
        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'build', \
            '--clean-match', \
                '*.py', \
                '*.py'])  # noqa

        # Clean all workspace base paths explicitly
        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'build', \
                'install', \
                'log', \
                'test_result'])  # noqa

        # Try again but with nothing left to clean
        main(argv=argv + ['clean', 'workspace', '--yes'])  # noqa

        main(argv=argv + ['build'])

        # Don't clean workspace base paths when prompted by user input
        monkeypatch.setattr('builtins.input', lambda: 'n')
        main(argv=argv + ['clean', 'workspace'])  # noqa

        # Ignore one workspace base paths explicitly
        main(argv=argv + ['clean', 'workspace', \
            '--base-ignore', \
                'log'])  # noqa

        # Ignore one workspace base paths explicitly
        main(argv=argv + ['clean', 'packages', \
            '--base-ignore', \
                'log'])  # noqa

        # Clean workspace base paths when prompted by user input
        monkeypatch.setattr('builtins.input', lambda: 'y')
        main(argv=argv + ['clean', 'workspace'])  # noqa

        print('ws_base: ', ws_base)
    finally:
        # the logging subsystem might still have file handles pending
        # therefore only try to delete the temporary directory
        # shutil.rmtree(ws_base, ignore_errors=True)
        pass


class _RaisingArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise sys.exc_info()[1]

    def test_suppress_argument_error(self, monkeypatch):
        ws_base = Path(mkdtemp(prefix='test_colcon_'))
        resources_base = Path('test', 'resources').absolute()
        shutil.copytree(resources_base / 'test_src', ws_base / 'src')

        os.chdir(ws_base)
        argv = []
        os.environ['COLCON_EXTENSION_BLOCKLIST'] = (
            'colcon_core.event_handler.desktop_notification:' +
            os.environ.get('COLCON_EXTENSION_BLOCKLIST', ''))

        main(argv=argv + ['build'])

        # Clean workspace base paths when prompted by user input
        monkeypatch.setattr('builtins.input', lambda: 'y')

        with pytest.raises(argparse.ArgumentError):
            # Try cleaning packages with invalid base handler selection
            main(argv=argv + ['clean', 'packages', '--yes', \
                '--base-select', \
                    'foo'])  # noqa

        with pytest.raises(argparse.ArgumentError):
            # Try cleaning workspace with invalid base handler selection
            main(argv=argv + ['clean', 'workspace', '--yes', \
                '--base-select', \
                    'bar'])  # noqa