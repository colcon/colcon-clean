# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from colcon_clean.base_handler import BaseHandlerExtensionPoint
from colcon_core.plugin_system import satisfies_version

BASE_PATH = 'log'


class LogBaseHandler(BaseHandlerExtensionPoint):
    """Determin how log paths for the workspace should be cleaned."""

    def __init__(self):  # noqa: D107
        super().__init__(BASE_PATH)
        satisfies_version(
            BaseHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--log-base',
            default=self.base_path,
            help='The base path for all log directories '
                 '(default: {self.base_path})'.format_map(locals()))

    def get_workspace_paths(self, *, args):  # noqa: D102
        return [args.log_base]

    def get_package_paths(self, *, pkg):  # noqa: D102
        return []
