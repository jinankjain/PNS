from __future__ import print_function
import functools
import itertools
import math
import scipy.integrate
import sys

TOP_REPLICATION_FACTOR = 0.1
AVG_WEBPAGES_PER_DOMAIN = 150
USE_APPROX = True

def log_replication_function(k, N, m):
    #return math.log(N - k + 1) + 1
    max_replication = max(1.0, m * TOP_REPLICATION_FACTOR)
    return max_replication / (k ** math.log(max_replication, N))

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            #print("Unable to find cached element", args)
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer

@memoize
def harmonic(n, s=1):
    """
    Compute the n-th harmonic number. If s != 1, the generalized harmonic
    number is computed:
    H_{n, s} = Sum_{i=1}^{n} 1/i^s
    """
    res = 0.0
    for i in xrange(1, n+1):
        res += 1 / (float(i) ** s)
    return res

@memoize
def harmonic_approx(n, s=1):
    """
    Compute the n-th harmonic number. If s != 1, the generalized harmonic
    number is computed:
    H_{n, s} = Sum_{i=1}^{n} 1/i^s
    """
    #if s == 1:
    #    return scipy.integrate.quad(lambda x: (1 - x**n) / (float(1) - x), 0, 1)
    partial = harmonic(min(1000, n), s)
    res = 0
    if n > 1000:
        res, _ = scipy.integrate.quad(lambda x: 1 / (float(x) ** s), 1001, n+1)
    return partial + res

@memoize
def _sum_repl_func(repl_func, N, m):
    res_main = 0.0
    for i in xrange(1, N+1):
        res_main += repl_func(i, N, m)
    return res_main

@memoize
def _sum_repl_func_zipf(repl_func, N, m, s=1):
    res_linked = 0.0
    for i in xrange(1, N+1):
        res_linked += repl_func(i, N, m) / (float(i) ** s)
    return res_linked

def average_replication(q, N, m, replication=(lambda k, N, m: 1), s=1):
    """
    Computer the average replication of a domain, i.e., how many fingerprints
    can be associated with that domain
    """
    if USE_APPROX:
        max_replication = max(1.0, m * TOP_REPLICATION_FACTOR)
        main_domain_replication = (max_replication *
                harmonic_approx(N, math.log(max_replication, N)) / N)
        linked_domains_replication = (max_replication *
                harmonic_approx(N, s + math.log(max_replication, N)) /
                harmonic_approx(N, s)) ** (q-1)
    else:
        res_main = _sum_repl_func(replication, N, m)
        res_linked = _sum_repl_func_zipf(replication, N, m, s)
        main_domain_replication = res_main / N
        linked_domains_replication = (res_linked / harmonic(N, s)) ** (q-1)
        assert main_domain_replication >= 1
        assert linked_domains_replication >= 1
    return main_domain_replication * linked_domains_replication

def prob_zipf_distrib(q, t, m, alpha):
    """
    Probability that a block pattern of q + t blocks contains another block
    pattern of q blocks, assuming that all blocks are i.i.d. according to a
    zipf distribution with decay parameter alpha. Parameter m represents the
    total number of blocks.
    """
    #prob_same_block = (harmonic_number(m, 2*alpha)
    #                   / (harmonic_number(m, alpha) ** 2))
    # The following would be the distribution if the distribution were uniform
    # rather than the zipf distribution.
    #prob_same_block = float(1)/m
    prob_same_block = float(1)/m
    prob_single_block_no_match = (1 - prob_same_block) ** (q + t)
    prob_block_pattern_match = (1 - prob_single_block_no_match) ** q
    return prob_block_pattern_match

def average_num_domain_pattern_matches(q, t, m, N, alpha=0.9):
    """
    Compute the average number of domains (out of N) whose block pattern of
    length q matches a reference pattern of q blocks (of a reference domain)
    plus t cover blocks.
    """
    # Compute the average of the binomial distribution, where prob_zipf_distrib
    # gives the probability p of a match, and N is the number of "samples". The
    # binomial distribution has an average of p * N.
    repl_func = log_replication_function
    return (prob_zipf_distrib(q, t, m, alpha) * N * AVG_WEBPAGES_PER_DOMAIN *
            average_replication(q, N, m, repl_func, alpha))

if __name__ == "__main__":
    N = 1000000000 # total number of domains
    q_range = [1, 2, 5, 10] # q is the number of domains queried together (1 website)
    #t_range = [0, 5, 10] # t is the number of cover blocks
    n_range = [50000, 10000, 1000] # n is the number of domains per block
    for q,n in itertools.product(q_range, n_range):
        m = N/n # Total number of blocks
        for t in [0, q]: # t is the number of cover blocks
            res = average_num_domain_pattern_matches(q, t, m, N)
            print("q={0}, t={1}, m={2}, n={3}: \t".format(q, t, m, n), res)

