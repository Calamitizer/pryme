import functools

def assert_natural(n, m = 1):
    """
    Assert that n is of type int and is greater than m.
    """
    message = str(n) + ' is not a natural number (of type int).'
    assert (type(n) is int) and (n >= m), message

def optional_arguments(d):
    """
    Decorate the input decorator d to accept optional arguments.
    """
    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return d(args[0])
        else:
            def real_decorator(decoratee):
                return d(decoratee, *args)
            return real_decorator
    return wrapped_decorator

@optional_arguments
def natural_input(f, m = 1):
    """
    Decorate the input function f to only take ints above m.
    """
    @functools.wraps(f)
    def final(n):
        assert_natural(n, m)
        return f(n)
    return final

def needs_int(f):
    """
    Decorator for typing arguments as int from Decomposition.
    """
    @functools.wraps(f)
    def wrapper(arg):
        if type(arg) is int:
            assert_natural(arg)
            return f(arg)
        return f(decompose(arg))
    return wrapper

def needs_decomp(f):
    """
    Decorator for typing arguments as Decomposition.
    
    If the argument  not already a Decomposition, this makes one out of it.
    """
    @functools.wraps(f)
    def wrapper(arg):
        if type(arg) is Decomposition:
            return f(arg)
        assert_natural(arg)
        return f(decompose(arg))
    return wrapper

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

def with_logging(f): # works
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        print '! ' + f.__name__ + ' called'
        return f(*args, **kwds)
    return wrapper
