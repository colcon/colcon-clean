# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import os

from colcon_clean.base_handler import BaseHandlerExtensionPoint
from colcon_core.plugin_system import satisfies_version
from colcon_core.argument_type import get_root_path_resolver

BASE_PATH = 'install'


class InstallBaseHandler(BaseHandlerExtensionPoint):
    """Determin how install paths for the workspace should be cleaned."""

    def __init__(self):  # noqa: D107
        super().__init__(BASE_PATH)
        satisfies_version(
            BaseHandlerExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        parser.add_argument(
            '--install-base',
            default=self.base_path,
            type=get_root_path_resolver(),
            help='The base path for all install directories '
                 '(default: {self.base_path})'.format_map(locals()))

    def get_workspace_paths(self, *, args):  # noqa: D102
        return [args.install_base]

    def get_package_paths(self, *, args, pkg):  # noqa: D102
        return [os.path.join(args.install_base, pkg.name)]
