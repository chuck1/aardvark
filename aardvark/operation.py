
import copy
import difflib
import json

from .address import *

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
    def __init__(self, address): #, value):
        super(OperationRemove, self).__init__(address)
        #self.value = value

    def apply(self, a0):
        a1 = copy.deepcopy(a0)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        del a2[self.address.lines[-1].key]
        return a1

    def unapply(self, a0):
        a1 = copy.deepcopy(a0)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        a2[self.address.lines[-1].key] = self.value
        return a1

    def to_array(self):
        #return {'remove': [self.address.to_array(), value]}
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

    def unapply(self, a):
        if not self.address.lines:
            return copy.deepcopy(self.a)

        a1 = copy.deepcopy(a)
        a2 = navigate(a1, Address(self.address.lines[:-1]))
        a2[self.address.lines[-1].key] = self.a
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

    def unapply(self, a):
        if not self.address.lines:
            return ''.join(difflib.restore(self.diffs, 1))

        a1 = copy.deepcopy(a)
        a2 = navigate(a1, Address(self.address.lines[:-1]))

        a2[self.address.lines[-1].key] = ''.join(difflib.restore(self.diffs, 1))

        return a1

    def to_array(self):
        return {'difflib': {
                'address': self.address.to_array(),
                'diffs': self.diffs,
                }}

    def __repr__(self):
        return f'<{self.__class__.__name__} address={self.address!r} diffs={self.diffs!r}>'











