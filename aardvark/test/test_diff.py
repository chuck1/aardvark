import json
import aardvark
import pytest

def _test(a, b):
    diffs = list(aardvark.diff(a, b))

    print('diffs:')
    for d in diffs:
        print(repr(d))

    c = aardvark.apply(a, diffs)

    assert b == c

    diffs1 = [d.to_array() for d in diffs]

    json.dumps(diffs1)

    diffs2 = [aardvark.from_array(d) for d in diffs1]

    d = aardvark.apply(a, diffs2)
    
    assert b == d

@pytest.mark.parametrize("a, b", [
    ({'a': 1}, None),
    ('a', None),
    ('a', 1),
    (None, 'a'),
    (None, 1),
    ({'a': 1}, {'b': 1}),
    ({'c': {'a': 1}}, {'c': {'b': 1}}),
    ({'c': 1}, {'c': 2}),
    ])
def test_diff(a, b):
    _test(a, b)
    _test(b, a)


