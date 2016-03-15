import math
import numbers
import fractions
import operator
import pickle

from .decorators import *

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
            self.n = 1
            candidates = primes(int(math.floor(math.sqrt(arg))))
            r = arg
            for p in candidates:
                if r == 1:
                    return
                while r % p == 0:
                    self[p] += 1
                    r //= p
        elif isinstance(arg, dict):
            for key in arg:
                self[key] = arg[key]
            self.n = product([p ** self[p] for p in self])
    def __getitem__(self, p):
        assert_prime(p)
        return dict.__getitem__(self, p)
    def __missing__(self, p):
        return 0
    def __setitem__(self, p, e):
        assert_prime(p)
        assert_natural(e, 0)
        if e == 0:
            if p in self:
                dict.__delitem__(self, p)
            return
        if e >= self[p]:
            self.n *= p ** (e - self[p])
        else:
            self.n //= p ** (self[p] - e)
        dict.__setitem__(self, p, e)
    def __delitem__(self, p):
        self.n //= p ** self[p]
        dict.__delitem__(self, p)
    def __repr__(self):
        return type(self).__name__ + '(' + str(self.n) + ')'
    def __add__(self, rhs):
        if type(rhs) is int:
            return self + decompose(rhs)
        if type(rhs) is type(self):                                             
            return decompose(self.n + rhs.n)
    def __radd__(self, lhs):
        return self + rhs
    def __mul__(self, rhs):
        if type(rhs) is int:
            # should be self * decompose(rhs)?
            return decompose(self.n * rhs)
        if type(rhs) is type(self):
            factors = set(self.keys()) | set(rhs.keys())
            return Decomposition({p: self[p] + rhs[p] for p in factors})
    def __rmul__(self, lhs):
        return self * lhs
    def _print(self):
        for p in self:
            print 'items:'
            print `p` + ': ' + `self[p]`

def assert_prime(n):
    message = str(n) + ' is not a prime (of type int).'
    assert is_prime(n), message

#put somewhere, decorate?
def product(container):
    return reduce(operator.mul, container, 1)

@natural_input
def primes(n):
    """
    Return a list of primes no greater than n.
    """
    return [2, 3, 5, 7, 11, 13, 17, 19, 23]

@natural_input
def is_prime(n):
    """
    Return whether n is prime.
    """
    return n in primes(n)

def mobius_transform(f):
    """
    Return the mobius transform of the input function f.
    """
    @natural_input
    def mf(n):
        return sum([mobius(n//d) * f(d) for d in divisors(n)])
    return mf

@needs_decomp
def divisors(decomp):
    print 2
    """
    Return a set of all divisors of the argument.
    """
    combine = lambda acc, p: set(a * (p ** e) for a in acc for e in xrange(decomp[p] + 1))
    return reduce(combine, decomp, {1})

@natural_input
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

@natural_input
def constant(n):
    """
    Return 1.
    
    Needs to accept a Decomposition.
    """
    return 1

@natural_input
def identity(n):
    """
    Return n.
    
    Needs to accept a Decomposition.
    """
    return n

@natural_input(0)
def power_gen(k):
    """
    Return a function yielding the k-th power of its argument.
    """
    if k == 0:
        return constant
    if k == 1:
        return identity
    @natural_input
    def power_k(n):
        return n ** k
    return power_k

@natural_input
def unit(n):
    return int(n == 1)

@needs_decomp
def totient(decomp):
    factors = [1 - fractions.Fraction(1, d) for d in decomp]
    return int(decomp.n * product(factors))

@needs_decomp
def mobius(decomp):
    """
    Return the mobius function evaluated at the argument.
    
    Accepts an int or a Decomposition.
    Called lowercase-mu in number theory.
    mobius(n) = (-1)^support(n) if n is square-free, 0 otherwise.
    """
    return 0 if any([p >= 2 for _, p in decomp]) else -1 ** (breadth(decomp) % 2)

@needs_decomp
def num_divisors(decomp):
    return product([decomp[p] + 1 for p in decomp])

@needs_decomp
def sum_divisors(decomp):
    a = [(p ** (decomp[p] + 1)) - 1 for p in decomp]
    b = [p - 1 for p in decomp]
    factors = [fractions.Fraction(x, y) for x, y in zip(a, b)]
    return int(product(factors))

@natural_input(0)
def sigma_gen(k):
    if k == 0:
        return num_divisors
    if k == 1:
        return sum_divisors
    @needs_decomp
    def sigma_k(decomp):
        a = [(p ** ((decomp[p] + 1) * k)) - 1 for p in decomp]
        b = [p ** k - 1 for p in decomp]
        # rewrite this line, jeez
        factors = [fractions.Fraction(x, y) for x, y in zip(a, b)]
        return int(product(factors))
    return sigma_k

@needs_decomp
def num_abel(decomp):
    """
    Return the number of isodistinct Abelian groups of the given order.
    """
    return product([partitions(decomp[p]) for p in decomp])

@natural_input
def liouville(n):
    return -1 ** breadth(n)

@natural_input
def gamma(n):
    return -1 ** breadth(n)

@natural_input
def ramanujan(n):
    return 1

@needs_decomp
def support(decomp):
    """
    Return the number of distinct prime factors of the argument.
    
    Accepts an int or a Decomposition.
    Called lowercase-omega in number theory.
    """
    return len(decomp)

@needs_decomp
def breadth(decomp):
    """
    Return the sum of the exponents in the decomposition of the argument.
    
    Accepts an int or a Decomposition.
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















