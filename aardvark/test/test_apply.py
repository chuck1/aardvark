from pprint import pprint
from aardvark import *

def test0():
    a = {}
    diff_list = [
            OperationAdd([AddressLine('a')], 1),
            ]
    b = apply(a, diff_list)

    pprint(b)

    assert b == {'a': 1}

