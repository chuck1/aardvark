__version__ = '0.1'

import copy
import difflib
import json

from .operation import *

def breakpoint():
    import pdb; pdb.set_trace();

def diff_dicts(a, b, address):
    
    keys_a = set(a.keys())
    keys_b = set(b.keys())
    just_a = keys_a - keys_b
    just_b = keys_b - keys_a
    a_and_b = keys_a & keys_b

    for k in just_a:
        yield OperationRemove(address + [AddressLine(k)])

    for k in just_b:
        yield OperationAdd(address + [AddressLine(k)], b[k])

    for k in a_and_b:
        yield from diff(a[k], b[k], address + [AddressLine(k)])
    
def diff(a, b, address=Address()):
    
    if a == b: return
    
    if isinstance(a, dict) and isinstance(b, dict):
        yield from diff_dicts(a, b, address)
        return

    if isinstance(a, str) and isinstance(b, str):
        a_lines = a.splitlines(keepends=True)
        b_lines = b.splitlines(keepends=True)
        if (len(a_lines) > 1) or (len(a_lines) > 2):
            d = difflib.ndiff(a_lines, b_lines)
            d = list(d)

            o = OperationDiffLib(address, d)

            #print(f'operation difflib: {json.dumps(o.to_array())}')
            #print(f'operation difflib bytes: {len(json.dumps(o.to_array()))}')
             
            yield o
            return

    o = OperationReplace(a, b, address)

    #print(f'operation replace: {json.dumps(o.to_array())}')
    #print(f'operation replace bytes: {len(json.dumps(o.to_array()))}')

    yield o

def apply(a, diff_list):
    a = copy.deepcopy(a)
    for d in diff_list:
        a = d.apply(a)
    return a

def unapply(a, diff_list):
    a = copy.deepcopy(a)
    for d in diff_list:
        a = d.unapply(a)
    return a

FUNCTIONS = {
            'add': OperationAdd,
            'remove': OperationRemove,
            'replace': OperationReplace,
            'address_line': AddressLine,
            'difflib': lambda d: OperationDiffLib(d['address'], d['diffs']),
            }

def blame(history, address, line):
    assert isinstance(history, list)

    for h in reversed(history):

        assert isinstance(h, list)

        for d in h:
            assert isinstance(d, Operation)
    
            if d.address.lines != address: continue

            if not isinstance(d, OperationDiffLib): continue

            s = '+ ' + line

            if s in d.diffs:
                return d

def parse_diffs(D):
    return [aardvark.util.from_array(d, FUNCTIONS) for d in D]





