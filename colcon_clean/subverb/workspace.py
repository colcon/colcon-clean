# Copyright 2016-2018 Dirk Thomas
# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import os
import os.path
from pathlib import Path
import shutil

from colcon_clean.clean.query import query_yes_no
from colcon_clean.subverb import CleanSubverbExtensionPoint
from colcon_core.argument_parser.destination_collector \
    import DestinationCollectorDecorator
from colcon_core.event_handler import add_event_handler_arguments
from colcon_core.plugin_system import satisfies_version
from colcon_core.verb import check_and_mark_build_tool
from colcon_core.verb import logger


class WorkspaceCleanSubverb(CleanSubverbExtensionPoint):
    """Clean current workspace."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            CleanSubverbExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--build-base',
            default='build',
            help='The base path for all build directories (default: build)')
        parser.add_argument(
            '--install-base',
            default='install',
            help='The base path for all install prefixes (default: install)')
        parser.add_argument(
            '--log-base',
            default='log',
            help='The base path for all install prefixes (default: log)')
        parser.add_argument(
            '--test-result-base',
            default='build',
            help='The base path for all test results (default: build)')

        parser.add_argument(
            '--base-select', nargs='*', metavar='BASE_NAME',
            default=['build', 'install', 'log', 'test_result'],
            help='Select base names to clean in workspace '
                 '(default: [build, install, log, test_result])')

        parser.add_argument(
            '-y', '--yes',
            action='store_true',
            help='Automatic yes to prompts')
        add_event_handler_arguments(parser)

        decorated_parser = DestinationCollectorDecorator(parser)
        self.task_argument_destinations = decorated_parser.get_destinations()

    def main(self, *, context):  # noqa: D102
        check_and_mark_build_tool(context.args.build_base)

        self._clean_paths(context.args)

        return 0

    def _clean_paths(self, args):
        base_paths = set()
        for base_name in args.base_select:
            base_arg = base_name + '_base'
            if hasattr(args, base_arg):
                base_path = getattr(args, base_arg)
                base_path = Path(os.path.abspath(base_path))
                base_paths.add(base_path)
            else:
                logger.warning(
                    "No base path knows for selction '{base_name}'"
                    .format_map(locals()))

        if not args.yes:
            print('Base paths:')
            for base_path in sorted(base_paths):
                print('    ', base_path)
            question = 'Clean the above base paths?'
            args.yes = query_yes_no(question)

        if args.yes:
            for base_path in base_paths:
                self._clean_path(base_path)

    def _clean_path(self, path):
        if path.exists():
            logger.info(
                "Cleaning base path: '{path}'".format_map(locals()))
            shutil.rmtree(path)
