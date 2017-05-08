from __future__ import division

#from block_pattern_probabilities import harmonic_approx

_MAX_REPLICATION = 10 ** 5

def replication(k, max_replication=_MAX_REPLICATION, zipf_param=1):
    return max(1, round(max_replication / (k ** zipf_param)))

def num_replicated_domains(max_replication=_MAX_REPLICATION, zipf_param=1):
    # round(k^{-s}R) > 1 iff k^{-s}R >= 1.5 iff R/1.5 >= k^s
    # iff k <= (R/1.5)^(1/s) iff k <= int( (R/1.5)^(1/s) )
    return int((max_replication / 1.5) ** (1 / zipf_param))

def num_replicas(max_replication=_MAX_REPLICATION, zipf_param=1):
    """Number of replicas, without counting the original record"""
    sum_replicas = 0
    k_star = num_replicated_domains(max_replication, zipf_param)
    for i in xrange(1, k_star+1):
        sum_replicas += replication(i, max_replication, zipf_param) - 1
    return sum_replicas
    #k_star = num_replicated_domains(max_replication, zipf_param)
    #return harmonic_approx(k_star, zipf_param) * max_replication - k_star

if __name__ == "__main__":
    assert replication(1) == _MAX_REPLICATION
    assert replication(num_replicated_domains()) == 2
    assert replication(num_replicated_domains() + 1) == 1
    assert replication(num_replicated_domains() + 1000) == 1
    assert replication(num_replicated_domains(zipf_param=0.8), zipf_param=0.8) == 2
    assert replication(num_replicated_domains(zipf_param=0.8) + 1, zipf_param=0.8) == 1

    print "# replicas (zipf_param=1):", num_replicated_domains()
    print "# replicas (zipf_param=0.9):", num_replicated_domains(zipf_param=0.9)
    M = 10 ** 9
    print "Cost (zipf_param=1):", num_replicas() / M
    print "Cost (zipf_param=0.9):", num_replicas(zipf_param=0.9) / M
    print "Replication of top 30 (zipf_param=0.9):"
    for i in range(1, 31):
        repl_i = replication(i, zipf_param=0.9)
        print "{}:\t{}\t(on {:.2f}% of all pages)".format(i, repl_i, repl_i / _MAX_REPLICATION * 100)

