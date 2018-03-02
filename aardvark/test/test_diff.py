from pprint import pprint
from aardvark import *

def test0():

    a = {'a': 1}
    b = {'b': 1}

    print()
    pprint(list(diff(a, b)))

def test1():

    a = {'c': {'a': 1}}
    b = {'c': {'b': 1}}

    print()
    pprint(list(diff(a, b)))

def test2():

    a = {'c': 1}
    b = {'c': 2}

    print()
    pprint(list(diff(a, b)))


