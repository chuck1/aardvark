__version__ = '0.1'

import copy

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
        a = navigate(a, self.address)
        self.apply2(a)
    
    def apply2(self, a):
        raise NotImplementedError()

class OperationPair(Operation):
    def __init__(self, address, pair):
        super(OperationPair, self).__init__(address)
        self.pair = copy.deepcopy(pair)

    def apply2(self, a):
        raise NotImplementedError()

class OperationRemove(Operation):
    def __init__(self, address):
        super(OperationRemove, self).__init__(address)

    def apply(self, a):
        a = navigate(a, Address(self.address.lines[:-1]))
        del a[self.address.lines[-1].key]

    def to_array(self):
        return {'remove': [self.address.to_array()]}

    def __repr__(self):
        return f'<{self.__class__.__name__} address={self.address}>'

class OperationAdd(Operation):
    def __init__(self, address, value):
        super(OperationAdd, self).__init__(address)
        self.value = value

    def apply(self, a):
        a = navigate(a, Address(self.address.lines[:-1]))
        a[self.address.lines[-1].key] = self.value

    def to_array(self):
        return {'add': [self.address.to_array(), self.value]}

    def __repr__(self):
        return f'<{self.__class__.__name__} address={self.address} value={self.value!r}>'

class OperationReplace(Operation):
    def __init__(self, a, b, address):
        super(OperationReplace, self).__init__(address)
        self.a = copy.deepcopy(a)
        self.b = copy.deepcopy(b)

    def apply(self, a):
        a = navigate(a, Address(self.address.lines[:-1]))
        a[self.address.lines[-1].key] = self.b

    def __repr__(self):
        return f'<{self.__class__.__name__} a={self.a!r} b={self.b!r} address={self.address}>'

    def to_array(self):
        return {'replace': [self.a, self.b, self.address.to_array()]}

class AddressLine:
    def __init__(self, key):
        self.key = key

    def navigate(self, a):
        return a[self.key]

    def __repr__(self):
        return f'<{self.__class__.__name__} key={self.key}>'

    def to_array(self):
        return {'address_line': [self.key]}

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
        return repr(self.lines)


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

    yield OperationReplace(a, b, address)

def apply(a, diff_list):
    a = copy.deepcopy(a)
    for d in diff_list:
        d.apply(a)
    return a

def from_array(d):
    s, args = list(d.items())[0]
    
    functions = {
            'add': OperationAdd,
            'remove': OperationRemove,
            'replace': OperationReplace,
            'address_line': AddressLine,
            }

    f = functions[s]

    return f(*args)

def maybe_dict_func(a):
    if isinstance(a, dict):
        return from_array(a)
    else:
        return a




