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
    def __int__(self):
        return self.n
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
        return self == other or self < other
    def __gt__(self, other):
        self._checkother(other)
        return other < self
    def __ge__(self, other):
        return self == other or self > other
    def __eq__(self, other):
        self._checkother(other)
        return tuple.__eq__(self, other)
    def __ne__(self, other):
        return not self == other
    def __floordiv__(self, other):
        return not self <= other or self > other

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

class IntPartitionPart(int):
    def __new__(_cls, arg):
        #assert_natural
        if type(arg) is not int or arg < 1:
            message = repr(arg) + ' is not a valid IntPartitionPart'
            raise TypeError(message)
        return int.__new__(_cls, arg)

class IntPartition(tuple):
    def __new__(_cls, arg):
        parts = []
        for k in arg:
            # sometimes not container
            if type(k) == IntPartitionPart:
                parts.append(k)
            else:
                parts.append(IntPartitionPart(k))
        return tuple.__new__(_cls, reversed(sorted(parts)))
    def __init__(self, arg):
        self.n = sum(self)
    def __int__(self):
        return self.n
    def _checkother(self, other):
        if type(other) is not IntPartition:
            raise TypeError
    def __lt__(self, other):
        self._checkother(other)
        if len(self) > len(other):
            return False
        for i in len(self):
            if self[i] > other[i]:
                return False
        return True
    def __le__(self, other):
        return self == other or self < other
    def __gt__(self, other):
        self._checkother(other)
        return other < self
    def __ge__(self, other):
        return self == other or self > other
    def __eq__(self, other):
        self._checkother(other)
        return tuple.__eq__(self, other)
    def __ne__(self, other):
        return not self == other
    def young(self, char='*'):
        for part in self:
            print char*part
    def conj(self):
        w = list(self)
        c = []
        while w != []:
            c.append(len(w))
            w = [part - 1 for part in w if part > 1]
        print c
        return IntPartition(c)
    def rank(self):
        if len(self) == 0:
            return 0
        if self[-1] == len(self):
            return len(self)
        for k in xrange(2, len(self) + 1):
            if self[k - 1] < k:
                break
        return k - 1

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

x = IntPartition((2, 6, 2, 1, 1, 1))
x = IntPartition((4, 3, 3))
print x
print len(x)
x.young()
y = x.conj()
print y.rank()
