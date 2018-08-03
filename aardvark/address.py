
import copy
import difflib
import json

from .util import *

class AddressLine:
    def __init__(self, key):
        self.key = key

    def navigate(self, a):
        try: 
            a[self.key]
        except:
            #breakpoint()
            pass

        return a[self.key]

    def __repr__(self):
        return f'<{self.__class__.__name__} key={self.key}>'

    def string(self):
        return f'[{self.key!r}]'

    def to_array(self):
        return {"address_line": [self.key]}


FUNCTIONS = {'address_line': AddressLine}

def breakpoint():
    import pdb; pdb.set_trace();

class Address:
    def __init__(self, list_or_address=[]):
        if isinstance(list_or_address, list):
            lines = list_or_address
        elif isinstance(list_or_address, Address):
            lines = list_or_address.lines
        else:
            raise TypeError('must be list or Address')

        lines = copy.deepcopy(lines)

        self.lines = [maybe_dict_func(l, FUNCTIONS) for l in lines]

    def __add__(self, lines):
        return Address(self.lines + lines)

    def to_array(self):
        return [l.to_array() for l in self.lines]

    def __repr__(self):
        return f'<{self.__class__.__name__} lines={self.lines!r}'

    def string(self):
        return ''.join(line.string() for line in self.lines)


