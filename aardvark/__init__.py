__version__ = '0.1'

import copy
import difflib
import json

def breakpoint():
    import pdb; pdb.set_trace();

def navigate(a, address):

    if not isinstance(address, Address):
        breakpoint()

    for line in address.lines:
        a = line.navigate(a)
    return a

class Operation:
    def __init__(self, address):
        self.address = Address(address)

    def apply(self, a):
        raise NotImplementedError()

class OperationPair(Operation):
    def __init__(self, address, pair):
        super(OperationPair, self).__init__(address)
        self.pair = copy.deepcopy(pair)

class OperationRemove(Operation):
    def __init__(self, address):
        super(OperationRemove, self).__init__(address)

    def apply(self, a0):
        a1 = copy.deepcopy(a0)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        del a2[self.address.lines[-1].key]
        return a1

    def to_array(self):
        return {'remove': [self.address.to_array()]}

    def __repr__(self):
        return f'<{self.__class__.__name__} address={self.address}>'

class OperationAdd(Operation):
    def __init__(self, address, value):
        super(OperationAdd, self).__init__(address)
        self.value = value

    def apply(self, a0):
        a1 = copy.deepcopy(a0)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        a2[self.address.lines[-1].key] = self.value
        return a1

    def to_array(self):
        return {'add': [self.address.to_array(), self.value]}

    def __repr__(self):
        return f'<{self.__class__.__name__} address={self.address} value={self.value!r}>'

class OperationReplace(Operation):
    def __init__(self, a, b, address):
        # TODO if you want to reorder the argument to put address first
        # be aware that it will break existing elephant databases!
        super(OperationReplace, self).__init__(address)
        self.a = copy.deepcopy(a)
        self.b = copy.deepcopy(b)

    def apply(self, a):
        if not self.address.lines:
            return copy.deepcopy(self.b)

        a1 = copy.deepcopy(a)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        a2[self.address.lines[-1].key] = self.b
        return a1

    def __repr__(self):
        return f'<{self.__class__.__name__} a={self.a!r} b={self.b!r} address={self.address}>'

    def to_array(self):
        # TODO if you want to reorder the argument to put address first
        # be aware that it will break existing elephant databases!
        return {'replace': [self.a, self.b, self.address.to_array()]}

class OperationDiffLib(Operation):
    def __init__(self, address, diffs):
        super(OperationDiffLib, self).__init__(address)
        self.diffs = diffs

    def apply(self, a):
        if not self.address.lines:
            return ''.join(difflib.restore(self.diffs, 2))

        a1 = copy.deepcopy(a)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        
        # do stuff to a2
        a2[self.address.lines[-1].key] = ''.join(difflib.restore(self.diffs, 2))

        return a1

    def to_array(self):
        return {'difflib': {
                'address': self.address.to_array(),
                'diffs': self.diffs,
                }}

class Address:
    def __init__(self, list_or_address=[]):
        if isinstance(list_or_address, list):
            lines = list_or_address
        elif isinstance(list_or_address, Address):
            lines = list_or_address.lines
        else:
            raise TypeError('must be list or Address')

        lines = copy.deepcopy(lines)

        self.lines = [maybe_dict_func(l) for l in lines]

    def __add__(self, lines):
        return Address(self.lines + lines)

    def to_array(self):
        return [l.to_array() for l in self.lines]

    def __repr__(self):
        return f'<{self.__class__.__name__} lines={self.lines!r}'

    def string(self):
        return ''.join(line.string() for line in self.lines)

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
            import pprint
            pprint.pprint(d)

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

def from_array(d):

    print('from_array', d, list(d.items())[0])

    s, args = list(d.items())[0]
    
    functions = {
            'add': OperationAdd,
            'remove': OperationRemove,
            'replace': OperationReplace,
            'address_line': AddressLine,
            'difflib': lambda d: OperationDiffLib(d['address'], d['diffs']),
            }

    f = functions[s]

    if isinstance(args, list):
        return f(*args)
    else:
        return f(args)

def maybe_dict_func(a):
    if isinstance(a, dict):
        return from_array(a)
    else:
        return a




