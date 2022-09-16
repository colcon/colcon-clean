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
        main(argv=argv + ['clean', 'packages', '--yes', \
            '--base-select', \
                'build', \
                'install', \
                'log', \
                'test_result', \
            '--packages-select', \
                'test-package-b', \
                'test-package-c'])  # noqa

        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'build', \
            '--clean-match', \
                '*.py'])  # noqa

        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'build', \
                'install', \
                'log', \
                'test_result'])  # noqa

        main(argv=argv + ['clean', 'workspace', '--yes'])  # noqa

        main(argv=argv + ['build'])

        monkeypatch.setattr('builtins.input', lambda _: 'y')
        main(argv=argv + ['clean', 'workspace'])  # noqa

        print('ws_base: ', ws_base)
    finally:
        # the logging subsystem might still have file handles pending
        # therefore only try to delete the temporary directory
        # shutil.rmtree(ws_base, ignore_errors=True)
        pass

    # check files exist
    # shutil.rmtree(ws_base / 'build')
    # shutil.rmtree(ws_base / 'install')
    # # shutil.rmtree(ws_base / 'log')
