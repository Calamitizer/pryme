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
            message = 'Sub-tuples do not span 1-' + str(self.n)
            raise TypeError(message)
    def _flatten(self):
        return sorted([i for part in self for i in part])
    def _checkother(self, other):
        if type(other) is not SetPartition:
            message = 'A SetPartition cannot be compared with a(n)' + type(other).__name__
            raise TypeError(message)
        if self.n != other.n:
            message = 'Partitions are not of the same set'
            raise TypeError(message)
    def __lt__(self, other):
        self._checkother(other)
        for a in self:
            if not any([set(self).issubset(b) for b in other]):
                return False
        return True
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    def __gt__(self, other):
        self._checkother(other)
        return other.__lt__(self)
    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)
    def __eq__(self, other):
        self._checkother(other)
        return tuple.__eq__(self, other)
    def __ne__(self, other):
        return not self == other
    def __floordiv__(self, other):
        return not self.__le__(other) or self.__gt__(other)

class IntPartition(set):
    def __init__(self, arg):
        pass
        # canonical ordering

def get_setpartitions(n):
    # assert_natural(0)
    if n == 0:
        return [tuple(tuple())]
    places = [1 for _ in xrange(n)]
    partitions = [range(1, n + 1)]
    maxes = [0 for _ in xrange(n)]
    while places != range(1, n + 1):
        for i in xrange(1, n):
            maxes[i] = max(places[i - 1], maxes[i - 1])
        partition = []
        j = list(reversed([places[i] <= maxes[i] for i in xrange(n)])).index(True)
        places[n - 1 - j] += 1
        for i in xrange(n - j, n):
            places[i] = 1
        for i in xrange(n):
            if places[i] <= len(partition):
                partition[places[i] - 1].append(i + 1)
            else:
                partition.append([i + 1])
        partitions.append(SetPartition(partition))
    return partitions

"""
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
"""
for i in xrange(0, 7):
    print len(get_setpartitions(i))
