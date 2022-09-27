# Copyright 2016-2018 Dirk Thomas
# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from colcon_core.plugin_system import instantiate_extensions
from colcon_core.plugin_system import order_extensions_by_name


class BaseHandlerExtensionPoint:
    """
    The interface for base handler extensions.

    A base handler extension determines how a base
    should cleaned for subset of packages to be processed.

    For each instance the attribute `BASE_HANDLER_NAME` is being set to
    the basename of the entry point registering the extension.
    """

    """The version of the package selection extension interface."""
    EXTENSION_POINT_VERSION = '1.0'

    def __init__(self, base_path):  # noqa: D107
        self.base_path = base_path

    def add_arguments(self, *, parser):
        """
        Add command line arguments specific to the workspace base.

        This method must be overridden in a subclass.

        :param parser: The argument parser
        """
        raise NotImplementedError()

    def get_workspace_paths(self, *, args):
        """
        Get paths for a workspace.

        This method must be overridden in a subclass.

        :param args: The parsed command line arguments

        :rtype: list
        """
        raise NotImplementedError()

    def get_package_paths(self, *, args, pkg):
        """
        Get paths for a package.

        This method must be overridden in a subclass.

        :param args: The parsed command line arguments
        :param pkg: The package descriptor

        :rtype: list
        """
        raise NotImplementedError()


def add_base_handler_arguments(parser):
    """
    Add the command line arguments for the base handler extensions.

    :param parser: The argument parser
    """
    group = parser.add_argument_group(title='Base handler arguments')
    extensions = get_base_handler_extensions()

    default_base_select = sorted(extensions.keys())
    group.add_argument(
        '--base-select', nargs='*', metavar='BASE_NAME',
        default=default_base_select,
        help='Select base names to clean in workspace '
             '(default: {default_base_select})'.format_map(locals()))

    for key in sorted(extensions.keys()):
        extension = extensions[key]
        extension.add_arguments(parser=group)


def get_base_handler_extensions():
    """
    Get the available base handler extensions.

    The extensions are ordered by their entry point name.

    :rtype: OrderedDict
    """
    extensions = instantiate_extensions(__name__)
    for name, extension in extensions.items():
        extension.BASE_HANDLER_NAME = name
    return order_extensions_by_name(extensions)
