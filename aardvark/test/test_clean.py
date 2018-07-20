
import aardvark.util

import pytest

@pytest.mark.parametrize("a, b", [
    ({'a': 1}, {'a': 1}),
    ({'a': 1, '_b': 2}, {'a': 1}),
    ({'a': {'b': 2, '_b': 2}}, {'a': {'b': 2}}),
    ])
def test_0(a, b):
    assert aardvark.util.clean(a) == b

