# all number theoretic functions, breadth, sigma, etc
# power generator
# error: `n` + ' is not a valid input for ' + `f.__name__`
# decorate Decomposition __add__, __mul__
# imp. Decomposition.__div__, __sub__

import math
import operator
import functools
import pickle

class Decomposition(dict):
    """
    Decompose a number and store its prime factorization.
    
    Should be primarily called through decompose(n), to memoize the result.
    
    d = Decomposition(n) creates an object satisfying:
    if p is prime:
        d[p] = e, where e is the exponent of p in the unique prime
        factorization of n. This means e = 0 if p does not divide n.
    if p is not prime:
        Accessing d[p] raises an exception.
    """    
    def __init__(self, arg):
        dict.__init__(self)
        if type(arg) is int:
            self.n = arg
            candidates = primes(math.floor(math.sqrt(self.n)))
            d = self.n
            for c in candidates:
                while d % c == 0:
                    self[c] += 1
                    d /= c
        elif isinstance(arg, dict):
            for d in arg:
                self[d] = arg[d]
            self.n = reduce(operator.mul, [pow(d, self[d]) for d in self], 1)
    def __getitem__(self, d):
        assert_prime(d)
        return dict.__getitem__(self, d)
    def __missing__(self, d):
        return 0
    def __setitem__(self, d, e):
        assert_prime(d)
        assert_natural(e, 0)
        if e == 0:
            return
        dict.__setitem__(self, d, e)
    def __delitem__(self, d):
        self.n /= pow(d, self[d])
        dict.__delitem__(self, d)
    def __add__(self, rhs):
        if type(rhs) is int:
            return self + decompose(rhs)
        if type(rhs) is type(self):                                             
            return decompose(self.n + rhs.n)
    def __radd__(self, lhs):
        return self + rhs
    def __mul__(self, rhs):
        if type(rhs) is int:
            return decompose(self.n * rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            return Decomposition({d: self[d] + rhs[d] for d in factors})
    def __rmul__(self, lhs):
        return self * lhs

def memoize(f): # works!
    """
    Memoization decorator for a function taking a single argument
    """
    class Memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, n):
            return self[n]
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret
    return Memodict(f)

def memoize_with_log(f): # works!
    """
    Goal: make the above print
    """
    print '! Memoizing ' + f.__name__
    class Memodict(dict):
        def __init__(self, f):
            self.__name__ = f.__name__
            self.f = f
        def __call__(self, n):
            return self[n]
        def __missing__(self, key):
            ret = self[key] = self.f(key)
            return ret
    f = Memodict(f)
    @functools.wraps(f)
    def final(n):
        log = '! called ' + f.__name__ + '(' + str(n) + ')'
        print log
        return f(n)
    print '! Memoized ' + final.__name__
    return final

def optional_arguments(f):
    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return f(args[0])
        else:
            def real_decorator(decoratee):
                return f(decoratee, *args)
            return real_decorator
    return wrapped_decorator

@optional_arguments
def natural_input(f, m = 1):
    @functools.wraps(f)
    def final(n):
        assert_natural(n, m)
        return f(n)
    return final

def with_print_name(f): # works
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        print '! ' + f.__name__ + ' called'
        return f(*args, **kwds)
    return wrapper

def primes(n):
    return [2, 3, 5, 7, 11, 13, 17, 19, 23]

def is_prime(n):
    return n in primes(n)

def mt(f):
    def mf(n):
        return [mu(n/d) * f(d) for d in divisors(n)]
    return mf
    
def mu(n):
    return 0 if any([p >= 2 for _, p in decomp]) else -1 ** (len(decomp) % 2)
    
def decompose(n):
    """
    Return a memoized Decomposition of n.
    
    e.g. decompose(12) = {2: 2, 3: 1}
    """
    return Decomposition(n)

@memoize_with_log
def fib(n):
    assert_natural(n, 0)
    if n in xrange(2):
        return n
    return fib(n - 1) + fib(n - 2)

@natural_input
def decompose(n):
    return Decomposition(n)

def assert_natural(n, m = 1):
    """
    Asserts that n is of type int and is greater than m.
    """
    message = str(n) + ' is not a natural number (of type int).'
    assert (type(n) is int) and (n >= m), message

def assert_prime(n):
    message = str(n) + ' is not a prime (of type int).'
    assert is_prime(n), message

def needs_decomp(f):
    """
    Decorator for typing arguments as Decomposition.
    
    If the argument not already a Decomposition, this makes one out of it.
    """
    @functools.wraps(f)
    def wrapper(arg):
        if type(arg) is Decomposition:
            return f(arg)
        assert_natural(arg)
        return f(decompose(arg))
    return wrapper

@needs_decomp
def support(decomp):
    """
    Return the number of distinct prime factors of the argument (int or Decomposition).
    
    Called lowercase-omega in number theory.
    """
    return len(decomp)

@needs_decomp
def breadth(decomp):
    """
    Return the sum of the exponents in the decomposition of the argument.
    
    Called uppercase-Omega in number theory.
    """
    return sum([decomp[d] for d in decomp])

def main():
    x = decompose(20)
    y = decompose(12)
    z1 = x + y
    #print z1
    z2 = x * y

if __name__ == '__main__':
    main()















