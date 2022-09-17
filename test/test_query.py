# Copyright 2021 Ruffin White
# Licensed under the Apache License, Version 2.0

from colcon_clean.clean.query import query_yes_no
import pytest


def test_query_interface(monkeypatch):
    question = 'Clean the above paths?'

    monkeypatch.setattr('builtins.input', lambda: '')
    assert query_yes_no(question, default='yes') is True
    assert query_yes_no(question, default='no') is False
    with pytest.raises(ValueError):
        query_yes_no(question, default='foo')

    input_iter = iter(['', 'y'])
    monkeypatch.setattr('builtins.input', lambda x=input_iter: next(x))
    assert query_yes_no(question, default=None) is True

    input_iter = iter(['', 'n'])
    monkeypatch.setattr('builtins.input', lambda x=input_iter: next(x))
    assert query_yes_no(question, default=None) is False
