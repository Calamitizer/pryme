from pryme import *
import operator
import itertools

decomposecomparisons = [
    operator.__lt__,
    operator.__le__,
    operator.__eq__,
    operator.__ne__,
    operator.__ge__,
    operator.__gt__,
]

decomposeunary = [
    operator.__abs__,
]

decomposebinary = [
    operator.__add__,
    operator.__mul__,
    operator.__pow__,
    lambda x,y: operator.__pow__(y,x),
]

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

logging = 1
def getmessage(string):
    if logging:
        return string
    return ''

def testvalues(x, y):
    dx = decompose(x)
    dy = decompose(y)
    for comp in decomposecomparisons:
        message = getmessage('Comparison ' + `comp` + ' failed for ' + `x` + ', ' + `y`)
        cond = comp(x, y) == comp(dx, dy)
        assert cond, message
    for op in decomposebinary:
        message = getmessage('Operation ' + `op` + ' failed for ' + `x` + ', ' + `y`)
        cond = op(x, y) == op(dx, dy)
        assert cond, message

def main():
    tests = itertools.product(xrange(1, 22), xrange(1, 22))
    for (x, y) in tests:
        pass
        testvalues(x, y)
    assert 2==2
    print 'All clear!'
    print 'M-R:'
    i = 0
    while True:
        i += 1
        if i % 1000000 == 0:
            print `i` + ' ' + `mr_prime(i)`
















if __name__ == '__main__':
    main()
