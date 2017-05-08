from __future__ import division
import sys
import operator as op
#import scipy.misc as sm

#def binomialCoeff(n, r):
#    r = min(r, n-r)
#    if r == 0: return 1
#    numer = reduce(op.mul, xrange(n, n-r, -1))
#    denom = reduce(op.mul, xrange(1, r+1))
#    return numer//denom

#def k_permute(n, k):
#    """
#    Compute nPk, i.e., n!/(n-k)!
#    """
#    res = 1
#    for i in xrange(n-k+1, n+1):
#        res *= i
#    return res

def binomialCoeff(n , k):
    """
    Python program for Optimized Dynamic Programming solution to
    Binomail Coefficient. This one uses the concept of pascal
    Triangle and less memory
    """
    # Declaring an empty array
    C = [0 for i in xrange(k+1)]
    C[0] = 1 #since nC0 is 1

    for i in range(1,n+1):

        # Compute next row of pascal triangle using
        # the previous row
        j = min(i ,k)
        while (j>0):
            C[j] = C[j] + C[j-1]
            j -= 1

    return C[k]

def distribute_over_bins_no_empty(k, b):
    """
    This function returns the number of ways that k elements can be distributed
    over b bins such that no bin is empty.
    """
    if k < b: return 0
    if b == 1: return 1
    tot = b ** k
    for i in xrange(1,b):
        tot -= binomialCoeff(b, i) * distribute_over_bins_no_empty(k, i)
    return tot

def probability_page_num_exactly(i, n, k):
    """
    This function computes the probability that distributing k elements
    uniformly at random over n pages exactly i pages are used.
    """
    if i > n: return 0
    return (binomialCoeff(n, i) * distribute_over_bins_no_empty(k, i)) / (n ** k)

def expected_page_num(n, k):
    """
    This function computes the expected number of pages (out of n) unto which
    k records would be distributed, with the records being distributed
    according to a uniform distribution (i.i.d.)
    """
    tot = 0
    for i in xrange(1,k+1):
        tot += i * probability_page_num_exactly(i, n, k)
    return tot

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " n k")
        sys.exit(1)
    else:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
        res = expected_page_num(n,k)
        print(res)
