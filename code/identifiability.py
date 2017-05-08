from __future__ import print_function, division

import functools
import itertools
import math
import scipy.integrate
import sys

from replication import replication

# Maximum replication allowed (even if the number of existing pages is higher).
# For zipf param. 0.9, replication 10**6 has a cost of 3%, 10**5 of 0.2%, while
# a replication of 10**7 would have a cost of 42%.
_MAX_REPLICATION = 10 ** 6

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
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
    Same as harmonic, but much faster for large values of n (n >> 1000)
    """
    partial = harmonic(min(1000, n), s)
    res = 0
    if n > 1000:
        res, _ = scipy.integrate.quad(lambda x: 1 / (float(x) ** s), 1001, n+1)
    return partial + res

@memoize
def factorial(n):
    """Compute n!"""
    assert(n>=0)
    result = 1
    for i in xrange(1,n+1):
        result *= i
    return result

def zipf_prob(k, N, s=1):
    return 1 / ((k ** s) * harmonic_approx(N, s))

# CURRENTLY THIS FUNCTION IS NOT USED (OLD)
def prob_page_pattern_match(q, q1, t, m, s):
    """
    Probability that a page pattern of q + t pages contains another page pattern
    of q1 pages, assuming that all pages are equiprobable. Parameter m
    represents the total number of pages.
    """
    #prob_same_page = (harmonic_approx(m, 2*s)
    #                   / (harmonic_approx(m, s) ** 2))
    prob_same_page = float(1) / m
    prob_single_page_no_match = (1 - prob_same_page) ** (q + t)
    return (1 - prob_single_page_no_match) ** q

def identifiability(k, q_distrib, t, m, N, s=1, max_repl=_MAX_REPLICATION):
    """
    For a given website w (with rank k), compute the probability that an
    adversary seeing the fingerprint F(w) \union T will assign to w being the
    intended website. q_distrib is a dictionary specifying the probability
    distribution of the fingerprint sizes. For example, {2: 0.3, 3: 0.7} would
    indicate that the fingerprint has probability 0.3 of having size 2 and 0.7
    of having size 3 (and probability 0 for other values). t indicates the cover
    query length, and may be a function of the fingerprint size. Parameter m
    represents the total number of pages, N the total number of records.
    """
    if not isinstance(q_distrib, dict):
        if isinstance(q_distrib, int):
            q_distrib = {q_distrib:1}
        else:
            raise TypeError("q_distrib must be a dict or int")
    if not callable(t):
        if isinstance(t, int):
            tmp = t
            t = lambda q: tmp
        else:
            raise TypeError("t must be a function or int")
    zipf_prob_k = zipf_prob(k, N, s)
    repl_k = replication(k, min(max_repl, m), s)
    # We average over the possible values of q
    avg_prob = 0 #temporary
    for q in q_distrib.keys():
        # STEP 1
        # We compute the probability that a randomly chosen fingerprint of w is
        # equal to a specific fingerprint of w. We distinguish two cases for the
        # first page, i.e., the page of the domain that is visited: the first
        # case in which this page is the same in the randomly chosen fingerprint
        # and in the specific fingerprint of w (which happens with probability 1
        # if the domain is not replicated, but has a low probability for higher
        # replications), and second the case where this does not happen, and the
        # first domain just happens by chance to be equal to one of the cover
        # queries of the specific fingerprint, and vice versa. We assume that
        # the rest of the fingerprint is made of non-replicated entries, which
        # are thus the same in the randomly chosen fingerprint and in the
        # specific one.

        # First, we compute the probability that the page of the main domain is
        # not equal to one of the cover pages of the specified fingerprint.
        #prob_page_not_in_cover = 1 #temporary
        #for j in xrange(0, t(q)):
        #    prob_page_not_in_cover *= 1 - 1 / (m - j)
        # Now we compute the probability that the first page matches, whether
        # because it is the same replica, or because it matches one of the cover
        # queries (unlikely).
        #prob_same_repl = (1/repl_k)
        #prob_main_page_match = (prob_same_repl +
        #        (1 - prob_same_repl) * (1 - prob_page_not_in_cover))
        # We compute the probability that the rest matches, i.e., that the
        # randomly chosen cover matches the given cover, or that, in case the
        # replicas for the first page are different, but the first pages matches
        # one of the cover pages in the specified fingerprint, that the randomly
        # chosen cover matches the cover of the specified fingerprint minus the
        # one matched by the first page, plus the first page of the specified
        # fingerprint. The probability of these is actually the same.
        #prob_cover_match = 1 #temporary
        #for i in xrange(0, t(q)):
        #    prob_cover_page_no_match = 1 #temporary
        #    for j in xrange(0, t(q) - i):
        #        prob_cover_page_no_match *= 1 - 1 / (m - q - i - j)
        #    prob_cover_match *= 1 - prob_cover_page_no_match
        # Finally we get the probability that a randomly chosen fingerprint of w
        # is equal to a specific fingerprint of the same w.
        #prob_full_match_same_w = prob_main_page_match * prob_cover_match
        prob_full_match_same_w = 1 / (repl_k**q * m**t(q))
        #prob_full_match_same_w_2 = 1 / (repl_k * m**(t(q)))
        #print(prob_full_match_same_w / prob_full_match_same_w_2)

        # STEP 2
        # Now we compute the probability that a randomly chosen fingerprint of
        # some w' (chosen according to its propularity) is equal to a specific
        # fingerprint of w. We distinguish the cases where w' != w and the case,
        # which we already computed, where w' == w.

        # We note that the probability of a match in the case where w' != w is
        # the same for all such w', independently of their popularity. It
        # depends, however, on the size of the fingerprint, the distribution of
        # which we assume to be independent of the popularity of the page. We
        # therefore compute the weighted average over the different sizes (when
        # the size is different, then the probability of a match is zero).
        avg_prob_full_match_any_w = 0 #temporary
        for q1 in q_distrib.keys():
            if q1 + t(q1) != q + t(q):
                continue
            prob_full_match_different_w = factorial(q1+t(q1))/(m**(q1+t(q1)))
            #prob_full_match_different_w = 1 #temporary
            #for i in xrange(0, q + t(q)):
            #    prob_page_no_match = 1 #temporary
            #    for j in xrange(0, q1 + t(q1) - i):
            #        prob_page_no_match *= 1 - 1 / (m - i - j)
            #    prob_full_match_different_w *= 1 - prob_page_no_match
            #prob_full_match_different_w = prob_page_pattern_match(q + t(q), q1,
            #                                                      t(q), m, s)
            # Now we consider both cases, the one where w' != w, for which we
            # just computed the probability, and the case where w' == w, which
            # we computed before.
            avg_prob_full_match_any_w += q_distrib[q1] * (
                    prob_full_match_different_w * (1 - zipf_prob_k) +
                    prob_full_match_same_w * zipf_prob_k)

        # STEP 3
        # Finally we can compute the probability of of an arbitrary w' being
        # equal to w given that their fingerprints match. We do this using bayes
        # theorem, which tells us that this probability is equal to the
        # probability of the fingerprints being equal given that w' == w, times
        # the probability of w' == w in general (depends on the popularity of
        # w), divided by the general probability of the fingerprints of w' and
        # w' being the same.
        prob_w1_is_w_when_full_match = (prob_full_match_same_w * zipf_prob_k
                                        / avg_prob_full_match_any_w)

        # Finally we update the average over the length of the fingerprint of w
        avg_prob += q_distrib[q] * prob_w1_is_w_when_full_match
    return avg_prob

if __name__ == "__main__":
    N = 10 ** 9 # total number of domains
    q_range = [1, 2] # q is the number of domains queried together (1 website)
    #t_range = [0, 5, 10] # t is the number of cover pages
    n_range = [10000] # n is the number of domains per page
    k_exp_range = [1,2,3,6,9]
    for k_exp,q,n in itertools.product(k_exp_range,q_range, n_range):
        m = N/n # Total number of pages
        for t in [0, q]: # t is the number of cover pages
            res = identifiability(10 ** k_exp, q, t, m, N, 0.91)
            print("k=10^{}, q={}, t={}, m={}, n={}:  \t".format(k_exp, q, t, m, n), res)

