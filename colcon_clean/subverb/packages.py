# Copyright 2016-2018 Dirk Thomas
# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from pathlib import Path

from colcon_clean.base_handler \
    import add_base_handler_arguments, get_base_handler_extensions
from colcon_clean.subverb import (
    add_clean_subverb_arguments,
    clean_paths,
    CleanSubverbExtensionPoint,
    get_recursion_filter,
    scan_directory,
)
from colcon_core.event_handler import add_event_handler_arguments
from colcon_core.package_selection import add_arguments \
    as add_packages_arguments
from colcon_core.package_selection import get_packages
from colcon_core.plugin_system import satisfies_version
from colcon_core.verb import check_and_mark_build_tool
from colcon_core.verb import logger


class PackagesCleanSubverb(CleanSubverbExtensionPoint):
    """Clean packages in workspace."""

    def __init__(self):  # noqa: D107
        super().__init__()
        satisfies_version(
            CleanSubverbExtensionPoint.EXTENSION_POINT_VERSION, '^1.0')

    def add_arguments(self, *, parser):  # noqa: D102
        add_clean_subverb_arguments(parser)
        add_base_handler_arguments(parser)
        add_event_handler_arguments(parser)
        add_packages_arguments(parser)

    def main(self, *, context):  # noqa: D102
        check_and_mark_build_tool(context.args.build_base)

        base_handler_extensions = get_base_handler_extensions()
        base_paths = set()

        args = context.args
        decorators = get_packages(args)
        recursion_filter = get_recursion_filter(args)

        for base_name in args.base_select:
            if base_name in args.base_ignore:
                logger.info(
                    "Ignoring base handler for selection '{base_name}'"
                    .format_map(locals()))
                continue
            base_handler_extension = base_handler_extensions[base_name]
            for decorator in decorators:
                if not decorator.selected:
                    continue
                pkg = decorator.descriptor
                package_paths = \
                    base_handler_extension.get_package_paths(
                        args=args, pkg=pkg)
                for package_path in package_paths:
                    package_path = Path(package_path).absolute()
                    base_paths.update(
                        scan_directory(package_path, recursion_filter))

        clean_paths(
            paths=base_paths,
            confirmed=args.yes)

        return 0
