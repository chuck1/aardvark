import json
import aardvark
import pytest

def _test_serialize(diffs):
    diffs1 = [d.to_array() for d in diffs]

    json.dumps(diffs1)

    diffs2 = [aardvark.from_array(d, aardvark.FUNCTIONS) for d in diffs1]

    return diffs2

def _test(a, b):
    diffs = list(aardvark.diff(a, b))

    print('diffs:')
    for d in diffs:
        print(repr(d))

    c = aardvark.apply(a, diffs)

    assert b == c

    #a1 = aardvark.unapply(b, diffs)
    #assert a1 == a

    diffs2 = _test_serialize(diffs)

    d = aardvark.apply(a, diffs2)
    
    assert b == d

string_short0 = 'a\nb\nc\nd\ne'
string_short1 = 'a\nb\nz\nd\ne'

long_string0 = (
        'hello\n'
        'this is a long multiline\n'
        'string. it has newline characters.\n'
        'it has several lines\n'
        'goodbye\n'
        )
long_string1 = (
        'hello\n'
        'this is a long multiline\n'
        'string. it has newline characters.\n'
        'THIS IS A NEW LINE\n'
        'it has several lines\n'
        'goodbye\n'
        )

@pytest.mark.parametrize("a, b", [
    ({'a': 1}, None),
    ('a', None),
    ('a', 1),
    (None, 'a'),
    (None, 1),
    ({'a': 1},           {'b': 1}),
    ({'c': {'a': 1}},    {'c': {'b': 1}}),
    ({'c': {'a': 1}},    {'c': {'a': 2}}),
    ({'c': 1},           {'c': 2}),
    (long_string0,       long_string1),
    (string_short0,      string_short1),
    ({'a': long_string0},   {'a': long_string1}),
    ({'a': string_short0},  {'a': string_short1}),
    ])
def test_diff(a, b):
    _test(a, b)
    _test(b, a)


