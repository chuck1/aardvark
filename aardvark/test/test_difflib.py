import functools
import json
import operator

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

    return diffs

def _test_0(l):
    a = l[0]
    for b in l[1:]:
        yield _test(a, b)
        a = b

def _test_1(l, s):
    print()

    diffs = list(_test_0(l))

    assert aardvark.apply(l[0], functools.reduce(operator.add, diffs)) == l[-1]

    b = aardvark.blame(diffs, [], s)

    assert b

def test_0():
    l = [
            'a\nb\nc\nd\ne\n',
            'a\nb\nf\nd\ne\n',
            'a\nb\nf\ng\nh\n',
            'a\nb\ng\nh\n',
            ]

    s = 'f\n'

    _test_1(l, s)
    _test_1(list(reversed(l)), s)



