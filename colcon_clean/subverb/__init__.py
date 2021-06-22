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

    filter_options = parser.add_argument_group(
        title='Filtering options',
        description='Specify what files and directories to include. All '
        'files and directories (including symbolic links) are included '
        'by default. The --dirhash-match/--dirhash-ignore arguments '
        'allows for selection using glob/wildcard (".gitignore style") '
        'path matching. Paths relative to the root `directory` (i.e. '
        'excluding the name of the root directory itself) are matched '
        'against the provided patterns. For example, to only include '
        'python source files, use: `dirhash path/to/dir -m "*.py"` or to '
        'exclude hidden files and directories use: '
        '`dirhash path/to.dir -i ".*" ".*/"` which is short for '
        '`dirhash path/to.dir -m "*" "!.*" "!.*/"`. By adding the '
        '--dirhash-list argument, all included paths, for the given '
        'filtering arguments, are returned instead of the hash value. '
        'For further details see '
        'https://github.com/andhus/dirhash/README.md#filtering'
    )
    # FIXME: Find out how colcon help could display group description
    filter_options = parser

    filter_options.add_argument(
        '--dirhash-match',
        nargs='+',
        default=['*'],
        help='One or several patterns for paths to include. NOTE: '
        'patterns with an asterisk must be in quotes ("*") or the '
        'asterisk preceded by an escape character (\\*).',
        metavar=''
    )
    filter_options.add_argument(
        '--dirhash-ignore',
        nargs='+',
        default=['.*'],
        help='One or several patterns for paths to exclude. NOTE: '
        'patterns with an asterisk must be in quotes ("*") or the '
        'asterisk preceded by an escape character (\\*).',
        metavar=''
    )
    filter_options.add_argument(
        '--dirhash-empty-dirs',
        action='store_true',
        default=False,
        help='Include empty directories (containing no files that meet '
        'the matching criteria and no non-empty sub directories).'
    )
    filter_options.add_argument(
        '--dirhash-no-linked-dirs',
        dest='dirhash_linked_dirs',
        action='store_false',
        default=True,
        help='Do not include symbolic links to other directories.'
    )
    filter_options.add_argument(
        '--dirhash-no-linked-files',
        dest='dirhash_linked_files',
        action='store_false',
        default=True,
        help='Do not include symbolic links to files.'
    )


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
