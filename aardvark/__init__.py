__version__ = '0.1'

import copy

def navigate(a, address):
    for line in address:
        a = line.navigate(a)
    return a

class Operation:
    def __init__(self, address):
        self.address = copy.deepcopy(address)

    def apply(self, a):
        a = navigate(a, self.address)
        self.apply2(a)
    
    def apply2(self, a):
        raise NotImplementedError()

class OperationPair(Operation):
    def __init__(self, address, pair):
        super(OperationPair, self).__init__(address)
        self.pair = copy.deepcopy(pair)

    def __repr__(self):
        return f'<{self.__class__.__name__} address={self.address} pair={self.pair}>'

class OperationPairRemove(OperationPair): pass

class OperationPairAdd(OperationPair):

    def apply2(self, a):
        a[self.pair[0]] = self.pair[1]

class OperationReplace(Operation):
    def __init__(self, a, b, address):
        super(OperationReplace, self).__init__(address)
        self.a = copy.deepcopy(a)
        self.b = copy.deepcopy(b)
    def __repr__(self):
        return f'<{self.__class__.__name__} a={self.a} b={self.b} address={self.address}>'

class Address:
    def __init__(self, lines=[]):
        self.lines = lines

    def __add__(self, lines):
        return Address(self.lines + lines)

    def __repr__(self):
        return f'<{self.__class__.__name__} lines={self.lines!r}'

    def string(self):
        return ''.join(line.string() for line in self.lines)

class AddressLine: pass

class AddressLineKey:
    def __init__(self, key):
        self.key = key

    def navigate(self, a):
        return a[self.key]

    def __repr__(self):
        return f'<{self.__class__.__name__} key={self.key}>'

    def string(self):
        return f'[{self.key!r}]'

class AddressLineIndex:
    def __init__(self, index):
        self.index = index

    def navigate(self, a):
        return a[self.index]

    def __repr__(self):
        return f'<{self.__class__.__name__} index={self.index}>'

    def string(self):
        return f'[{self.index!r}]'

def diff_dicts(a, b, address):
    
    keys_a = set(a.keys())
    keys_b = set(b.keys())
    just_a = keys_a - keys_b
    just_b = keys_b - keys_a
    a_and_b = keys_a & keys_b

    for k in just_a:
        yield OperationPairRemove(address, (k, a[k]))

    for k in just_b:
        yield OperationPairAdd(address, (k, b[k]))

    for k in a_and_b:
        yield from diff(a[k], b[k], address + [AddressLineKey(k)])
    

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




