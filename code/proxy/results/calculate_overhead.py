import argparse
import bisect
import math
import numpy as np
import random
import yaml

from analyze_results import filter_data
from _functools import reduce
from collections import defaultdict, OrderedDict


_ZIPF_PARAM = 0.91
_N_ROUNDS = 1000
_N_PAGE_LOADS = 100

_PAGE_ENTRY_SIZE = 100
_ENTRIES_PER_PAGE = 10**4
_PAGE_SIZE = _ENTRIES_PER_PAGE * _PAGE_ENTRY_SIZE


# Change yaml constructor to construct an OrderedDict instead of dict.
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)


class ZipfGenerator:
    """
    Generates requests according to a Zipf distribution with a given alpha.
    """
    def __init__(self, n, alpha):
        self.n = n
        # Calculate Zeta values from 1 to n:
        tmp = [1. / (math.pow(float(i), alpha)) for i in range(1, n + 1)]
        zeta = reduce(lambda sums, x: sums + [sums[-1] + x], tmp, [0])

        # Store the translation map:
        self.distMap = [x / zeta[-1] for x in zeta]

    def next(self):
        # Take a uniform 0-1 pseudo-random value:
        u = random.random()

        # Translate the Zipf variable:
        return bisect.bisect(self.distMap, u) - 1


def calculate_overhead(page_load_data, debug=False):
    N = len(page_load_data)
    print("Initializing Zipf generator (N=%d, alpha=%.2f)" % (N, _ZIPF_PARAM))
    zipf_gen = ZipfGenerator(N, _ZIPF_PARAM)
    domains = list(page_load_data.keys())

    ndomains_per_round = np.empty(_N_ROUNDS)
    requests_per_sld = defaultdict(int)
    for i in range(_N_ROUNDS):
        page_set = set()
        for _ in range(_N_PAGE_LOADS):
            domain_idx = zipf_gen.next()
            domain = domains[domain_idx]
            # Track how many requests are done for each domain (for debugging).
            requests_per_sld[domain] += 1
            # Add domain to page set, since it might not show up in the
            # SLDs dict for that page load.
            page_set.add(domain)
            # Add all SLDs to the page set.
            page_set.update(page_load_data[domain].keys())
        ndomains_per_round[i] = len(page_set)

    if debug:
        requests_per_sld = sorted([tup for tup in requests_per_sld.items()],
                                  key=lambda item: item[1], reverse=True)
        debug_str = "\n".join("%s: %d" % tup for tup in requests_per_sld)
        print("Request distribution:\n%s" % debug_str)

    np.sort(ndomains_per_round)
    mean = np.mean(ndomains_per_round)
    print("Stats about # of SLDs after %d runs of loading %d pages:" %
          (_N_ROUNDS, _N_PAGE_LOADS))
    print("Min: %d" % np.min(ndomains_per_round))
    print("Max: %d" % np.max(ndomains_per_round))
    print("Mean: %d" % mean)
    print("95th: %d" % np.percentile(ndomains_per_round, 95))
    print("Average cache size: %.2f MB" % (mean * _PAGE_SIZE / 10**6))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    with open(args.i, 'r') as infile:
        page_load_data = yaml.load(infile)
        filtered_data, _, _ = filter_data(page_load_data)
        calculate_overhead(filtered_data, args.debug)
