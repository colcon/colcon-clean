# Copyright 2016-2018 Dirk Thomas
# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

import shutil

from colcon_clean.clean.query import query_yes_no
from colcon_core.logging import colcon_logger
from colcon_core.plugin_system import instantiate_extensions
from colcon_core.plugin_system import order_extensions_by_name

logger = colcon_logger.getChild(__name__)


class CleanSubverbExtensionPoint:
    """
    The interface for clean subverb extensions.

    A clean subverb extension provides a subverb to the `clean` verb of
    the command line tool.

    For each instance the attribute `SUBVERB_NAME` is being set to the basename
    of the entry point registering the extension.
    """

    """The version of the clean subverb extension interface."""
    EXTENSION_POINT_VERSION = '1.0'

    def add_arguments(self, *, parser):
        """
        Add command line arguments specific to the clean subverb.

        The method is intended to be overridden in a subclass.

        :param parser: The argument parser
        """
        pass

    def main(self, *, context):
        """
        Execute the clean subverb extension logic.

        This method must be overridden in a subclass.

        :param context: The context providing the parsed command line arguments
        :returns: The return code
        """
        raise NotImplementedError()


def add_clean_subverb_arguments(parser):
    """
    Add the command line arguments for the clean subverb extensions.

    :param parser: The argument parser
    """
    group = parser.add_argument_group(title='Clean subverb arguments')

    group.add_argument(
        '-y', '--yes',
        action='store_true',
        help='Automatic yes to prompts')


def get_subverb_extensions():
    """
    Get the available subverb extensions.

    The extensions are ordered by their entry point name.

    :rtype: OrderedDict
    """
    extensions = instantiate_extensions(__name__)
    for name, extension in extensions.items():
        extension.SUBVERB_NAME = name
    return order_extensions_by_name(extensions)


def clean_paths(paths, confirmed=False):
    """
    Clean provided paths with conformation.

    :paths: list
    :confirmed: bool
    """
    if not confirmed:
        print('Paths:')
        for path in sorted(paths):
            print('    ', path)
        question = 'Clean the above paths?'
        confirmed = query_yes_no(question)

    if confirmed:
        for path in paths:
            _clean_path(path)


def _clean_path(path):
    if path.exists():
        logger.info(
            "Cleaning path: '{path}'".format_map(locals()))
        shutil.rmtree(path)
