# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from colcon_clean.base_handler import BaseHandlerExtensionPoint
from colcon_core.plugin_system import satisfies_version

BASE_PATH = 'build'


class BuildBaseHandler(BaseHandlerExtensionPoint):
    """Determin how build paths for the workspace should be cleaned."""

    def __init__(self):  # noqa: D107
        super().__init__(BASE_PATH)
        satisfies_version(
            BaseHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--build-base',
            default=self.base_path,
            help='The base path for all build directories '
                 '(default: {self.base_path})'.format_map(locals()))
