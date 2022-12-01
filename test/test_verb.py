# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from unittest.mock import Mock

from colcon_clean.verb.clean import CleanVerb
from colcon_core.command import CommandContext


class Object(object):
    pass


def test_verb_interface():
    interface = CleanVerb()
    interface._subparser = Object()
    interface._subparser.format_usage = Mock(return_value='')

    args = Object()
    context = CommandContext(command_name='clean', args=args)

    context.args.subverb_name = None
    rc = interface.main(context=context)
    assert rc == 'Error: No subverb provided'

    context.args.subverb_name = 'packages'
    rc = interface.main(context=context)
    assert rc is None

    context.args.subverb_name = 'workspace'
    rc = interface.main(context=context)
    assert rc is None
