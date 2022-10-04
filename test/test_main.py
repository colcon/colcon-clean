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


def _raising_error(self, message):
    raise sys.exc_info()[1]


argparse.ArgumentParser.error = _raising_error


def test_main(monkeypatch):
    """System test for colcon clean CLI."""
    ws_base = Path(mkdtemp(prefix='test_colcon_'))
    resources_base = Path('test', 'resources').absolute()
    shutil.copytree(resources_base / 'test_src', ws_base / 'src')

    os.chdir(ws_base)
    argv = []
    os.environ['COLCON_EXTENSION_BLOCKLIST'] = (
        'colcon_core.event_handler.desktop_notification:' +
        os.environ.get('COLCON_EXTENSION_BLOCKLIST', ''))
    os.environ['COLCON_DEFAULTS_FILE'] = \
        (resources_base / 'defaults.yaml').as_posix()

    try:
        main(argv=argv + ['build'])
        main(argv=argv + ['test'])

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

        # Assert unselected packages are skipped
        assert (ws_base / 'build' / 'test-package-a').exists()
        assert (ws_base / 'install' / 'test-package-a').exists()
        assert (ws_base / 'test_results' / 'test-package-a').exists()

        # Assert selected packages are cleaned
        assert not (ws_base / 'build' / 'test-package-b').exists()
        assert not (ws_base / 'build' / 'test-package-c').exists()
        assert not (ws_base / 'install' / 'test-package-b').exists()
        assert not (ws_base / 'install' / 'test-package-c').exists()
        assert not (ws_base / 'test_results' / 'test-package-b').exists()
        assert not (ws_base / 'test_results' / 'test-package-c').exists()

        # Assert inapplicable base paths are skipped
        assert (ws_base / 'log').exists()

        # Clean workspace build base paths of python files
        # And with duplicate match filters
        main(argv=argv + ['clean', 'workspace', '--yes', \
            '--base-select', \
                'build', \
            '--clean-match', \
                '*.py', \
                '*.py'])  # noqa

        # Assert workspace matches are cleaned
        assert not (ws_base / 'build' / 'test-package-a' / 'build' / 'lib' /
                    'test_package_a ' / '__init__.py').exists()

        # Assert workspace misses are not cleaned
        assert (ws_base / 'build' / 'test-package-a' /
                'colcon_build.rc').exists()

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

        # Assert workspace base paths are cleaned
        assert not (ws_base / 'build').exists()
        assert not (ws_base / 'install').exists()
        assert not (ws_base / 'test_results').exists()
        # Exception for log, as clean verb generates its own
        # assert not (ws_base / 'log').exists()

        # Try again implicitly but with nothing left to clean
        main(argv=argv + ['clean', 'workspace', '--yes'])  # noqa

        main(argv=argv + ['build'])
        main(argv=argv + ['test'])

        # Don't clean workspace base paths when prompted by user input
        monkeypatch.setattr('builtins.input', lambda: 'n')
        main(argv=argv + ['clean', 'workspace'])  # noqa

        # Ignore one workspace base paths explicitly
        main(argv=argv + ['clean', 'workspace', \
            '--base-ignore', \
                'log'])  # noqa

        # Assert no workspace base paths are cleaned
        assert (ws_base / 'build').exists()
        assert (ws_base / 'install').exists()
        assert (ws_base / 'test_results').exists()
        assert (ws_base / 'log').exists()

        # Ignore one package base paths explicitly
        main(argv=argv + ['clean', 'packages', \
            '--base-ignore', \
                'log'])  # noqa

        # Assert no package base paths are cleaned
        assert (ws_base / 'build' / 'test-package-a').exists()
        assert (ws_base / 'build' / 'test-package-b').exists()
        assert (ws_base / 'build' / 'test-package-c').exists()
        assert (ws_base / 'install' / 'test-package-a').exists()
        assert (ws_base / 'install' / 'test-package-b').exists()
        assert (ws_base / 'install' / 'test-package-c').exists()
        assert (ws_base / 'test_results' / 'test-package-a').exists()
        assert (ws_base / 'test_results' / 'test-package-b').exists()
        assert (ws_base / 'test_results' / 'test-package-c').exists()
        assert (ws_base / 'log').exists()

        # Clean workspace base paths when prompted by user input
        monkeypatch.setattr('builtins.input', lambda: 'y')

        # Ignore one package explicitly
        main(argv=argv + ['clean', 'packages', \
            '--packages-skip', \
                'test-package-a'])  # noqa

        # Assert unselected packages are skipped
        assert (ws_base / 'build' / 'test-package-a').exists()
        assert (ws_base / 'install' / 'test-package-a').exists()
        assert (ws_base / 'test_results' / 'test-package-a').exists()

        # Assert selected packages are cleaned
        assert not (ws_base / 'build' / 'test-package-b').exists()
        assert not (ws_base / 'build' / 'test-package-c').exists()
        assert not (ws_base / 'install' / 'test-package-b').exists()
        assert not (ws_base / 'install' / 'test-package-c').exists()
        assert not (ws_base / 'test_results' / 'test-package-b').exists()
        assert not (ws_base / 'test_results' / 'test-package-c').exists()

        # Ignore one workspace base paths explicitly
        main(argv=argv + ['clean', 'workspace', \
            '--base-ignore', \
                'log'])  # noqa

        # Assert no workspace base paths are cleaned
        assert not (ws_base / 'build').exists()
        assert not (ws_base / 'install').exists()
        assert not (ws_base / 'test_results').exists()
        assert (ws_base / 'log').exists()

        main(argv=argv + ['clean', 'workspace'])  # noqa

        with pytest.raises(argparse.ArgumentError):
            # Try cleaning packages with invalid base handler selection
            main(argv=argv + ['clean', 'packages', \
                '--base-select', \
                    'foo'])  # noqa

        with pytest.raises(argparse.ArgumentError):
            # Try cleaning workspace with invalid base handler selection
            main(argv=argv + ['clean', 'workspace', \
                '--base-select', \
                    'bar'])  # noqa

        print('ws_base: ', ws_base)
    finally:
        # the logging subsystem might still have file handles pending
        # therefore only try to delete the temporary directory
        # shutil.rmtree(ws_base, ignore_errors=True)
        pass
