class IntersectionError(Exception):
    def __init__(self):
        Exception.__init__(self)

class SetPartitionPartStructureError(Exception):
    def __init__(self, arg):
        Exception.__init__(self, arg)

class SetPartitionPart(tuple):
    def __new__(_cls, arg):
        seen = []
        if len(arg) == 0:
            message = repr(arg) + ' is not a container'
            raise SetPartitionStructureError(message)
        for item in arg:
            if type(item) is not int or item < 1: # make assert_natural
                message = repr(item) + ' cannot be in a SetPartitionPart'
                raise SetPartitionPartStructureError(message)
            if item in seen:
                message = repr(item) + ' degenerate in ' + repr(arg)
                raise SetPartitionPartStructureError(message)
            seen.append(item)
        return tuple.__new__(_cls, sorted(arg))
    def __lt__(self, other):
        self._checkcompat(other)
        return self[0] < other[0]
    def __le__(self, other):
        self._checkcompat(other)
        return self[0] <= other[0]
    def __gt__(self, other):
        self._checkcompat(other)
        return self[0] > other[0]
    def __ge__(self, other):
        self._checkcompat(other)
        return self[0] >= other[0]
    def __eq__(self, other):
        return tuple.__eq__(self, other)
    def __ne__(self, other):
        return tuple.__ne__(self, other)
    def _checkcompat(self, other):
        print 'compare: ' + `self` + `other`
        if set(self) & set(other) != set():
            message = repr(self) + ' and ' + repr(other) + ' not disjoint'
            raise SetPartitionPartStructureError(message)

class SetPartition(tuple):
    def __new__(_cls, arg):
        parts = []
        for item in arg:
            if type(item) == SetPartitionPart:
                parts.append(item)
            else:
                parts.append(SetPartitionPart(item))
        return tuple.__new__(_cls, tuple(sorted(parts)))
    def __init__(self, arg):
        if len(self) >= 2:
            for i, a in enumerate(self[:-1]):
                for b in self[i+1:]:
                    a._checkcompat(b)
        rep = self._flatten()
        self.n = max(rep)
        if rep != range(1, self.n + 1):
            raise TypeError
    def _flatten(self):
        return sorted([i for part in self for i in part])
        #check flatten
        # how to pull a part from it? canonical ordering?

class IntPartition(set):
    def __init__(self, arg):
        pass
        # canonical ordering


x = SetPartitionPart([1, 2, 4])
print 'x: ' + `x`
y = SetPartitionPart([5, 6])
z = SetPartitionPart([3])
P = SetPartition((x, y, z))

x1 = [1,2,4]
y1 = [5,6]
z1 = [3]
P1 = SetPartition((x1, y1, z1))
print P == P1













print P
print P.n
