from __future__ import print_function
from fractions import Fraction as mpq
import functools
import math
import scipy.integrate
from sympy.functions.combinatorial.numbers import harmonic
import timeit

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            #print("Unable to find cached element", args)
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer

def harmonic_full(n, s=1):
    res = 0.0
    for i in xrange(1, n+1):
        res += 1 / (float(i) ** s)
    return res

def _harmonic4(a, b):
    if b-a == 1:
        return float(1) / a
    m = (a+b)//2
    return _harmonic4(a,m) + _harmonic4(m,b)

def harmonic4(n):
    return _harmonic4(1,n+1)

def approx_harm(n, s=1):
    partial = harmonic_full(min(1000, n), s)
    res = 0
    if n > 1000:
        res, _ = scipy.integrate.quad(lambda x: 1 / (float(x) ** s), 1001, n+1)
    return partial + res

setup_approx="""
import scipy.integrate
def approx_harm(n, s=1):
    res, _ = scipy.integrate.quad(lambda x: 1 / (float(x) ** s), 1, n+1)
    return res
"""

setup_split="""
def _harmonic4(a, b):
    if b-a == 1:
        return float(1) / a
    m = (a+b)//2
    return _harmonic4(a,m) + _harmonic4(m,b)

def harmonic4(n):
    return _harmonic4(1,n+1)
"""

setup_full="""
def harmonic_full(n, s=1):
    res = 0.0
    for i in xrange(1, n+1):
        res += 1 / (float(i) ** s)
    return res
"""

setup_int="""
import scipy.integrate
def harmonic_int(n, s=1):
    return scipy.integrate.quad(lambda x: (1 - x**n) / (float(1) - x), 0, 1)
"""

setup_lib="""
from sympy.functions.combinatorial.numbers import harmonic
"""

if __name__ == "__main__":
    t_full = timeit.timeit('harmonic_full(10000000, 0.9)', setup=setup_full, number=1)
    print("full: {}".format(t_full))
    t_approx = timeit.timeit('approx_harm(10000000, 0.9)', setup=setup_approx, number=1)
    print("approx: {}".format(t_approx))
    #t_int = timeit.timeit('harmonic_int(1000000, 0.9)', setup=setup_int, number=10)
    #print("int: {}".format(t_int))
    #t_split = timeit.timeit('harmonic4(1000000)', setup=setup_split, number=10)
    #print("split: {}".format(t_split))
    max_replication = 1000
    print(harmonic_full(1000000, 0.9 + math.log(max_replication, 1000000)))
    print(approx_harm(1000000, 0.9 + math.log(max_replication, 1000000)))

