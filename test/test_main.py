# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import os
from pathlib import Path
import shutil
from tempfile import mkdtemp

from colcon_core.command import main


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

        # Clean workspace base paths when prompted by user input
        monkeypatch.setattr('builtins.input', lambda _: 'y')
        main(argv=argv + ['clean', 'workspace'])  # noqa

        # Try cleaning packages with invalid base handler selection
        main(argv=argv + ['clean', 'packages', '--yes', \
            '--base-select', \
                'foo'])  # noqa

        # Try cleaning workspace with invalid base handler selection
        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'foo'])  # noqa

        print('ws_base: ', ws_base)
    finally:
        # the logging subsystem might still have file handles pending
        # therefore only try to delete the temporary directory
        # shutil.rmtree(ws_base, ignore_errors=True)
        pass
