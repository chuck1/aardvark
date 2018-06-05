import pprint
import aardvark

def test0():
    a = {}
    diff_list = [
            aardvark.OperationAdd([aardvark.AddressLine('a')], 1),
            ]
    b = aardvark.apply(a, diff_list)

    print('b:')
    pprint.pprint(b)

    assert b == {'a': 1}

