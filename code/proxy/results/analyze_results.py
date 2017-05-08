import numpy as np
import sys
import yaml

from collections import defaultdict


def is_valid_entry(domain, nrequests):
    parts = domain.split('.')
    # Remove requests to raw IPs since they need no name lookup.
    # Note: This assumes IPv4 addresses.
    if parts[0].isdigit() and parts[1].isdigit() or nrequests == 0:
        return False
    return True


def is_valid_base_entry(base_domain, requests):
    total_requests = 0
    for _, nrequests in requests.items():
        total_requests += nrequests

    return base_domain and requests and total_requests > 1


def filter_data(raw_data):
    sub_requests_before = 0
    sub_requests_after = 0
    for base_domain, requests in raw_data.items():
        sub_requests_before += len(requests)
        raw_data[base_domain] = {k: v for k, v in requests.items() if
                                 is_valid_entry(k, v)}
        sub_requests_after += len(raw_data[base_domain])

    # Remove empty request chains.
    page_loads_before = len(raw_data)
    filtered_data = {k: v for k, v in raw_data.items() if
                     is_valid_base_entry(k, v)}
    return (filtered_data, page_loads_before - len(filtered_data),
            sub_requests_before - sub_requests_after)

def compute_statistics(raw_data, P=100):
    """Computes some interesting statistics on the raw data.

    Args:
        raw_data: A dict from domain to a dict containing all SLDs requested
            and how many times they where requested.
    """
    filtered_data, n_page_loads_filtered, n_sub_requests_filtered = \
        filter_data(raw_data)
    N = len(filtered_data)
    finger_prints = np.empty(N)
    finger_prints_alt = np.zeros(N)
    sld_counts = defaultdict(int)
    unique_slds = set()
    idx = 0
    for base_domain, requests in filtered_data.items():
        finger_prints[idx] = len(requests)
        unique_slds.add(base_domain)
        for sld, _ in requests.items():
            sld_counts[sld] += 1
            unique_slds.add(sld)
        idx += 1

    sorted_sld_counts = sorted(sld_counts.items(),
                               key=lambda item: item[1],
                               reverse=True)
    top_p_slds = set([sld[0] for sld in sorted_sld_counts[:P]])
    idx = 0
    for base_domain, requests in filtered_data.items():
        for sld, _ in requests.items():
            if sld not in top_p_slds:
                finger_prints_alt[idx] += 1
        finger_prints_alt[idx] = max(finger_prints_alt[idx], 1)
        idx += 1
    # print("\n".join("%s: %d" % tup for tup in sorted_sld_counts[:P]))

    np.sort(finger_prints)
    np.sort(finger_prints_alt)
    print("%d page loads analyzed." % N)
    print("%d page loads filtered out." % n_page_loads_filtered)
    print("%d sub requests filtered." % n_sub_requests_filtered)
    print("Total number of unique SLDs seen: %d" % len(unique_slds))
    print("Fingerprints:\nMin: %d | Max: %d | Mean: %.2f | Median: %d | 95th: "
          "%d" % (np.min(finger_prints), np.max(finger_prints),
                  np.mean(finger_prints), np.median(finger_prints),
                  np.percentile(finger_prints, 95)))
    print("Fingerprints without top %d SLDs:\nMin: %d | Max: %d | Mean: %.2f | "
          "Median: %d | 95th: %d" %
          (P, np.min(finger_prints_alt), np.max(finger_prints_alt),
           np.mean(finger_prints_alt), np.median(finger_prints_alt),
           np.percentile(finger_prints_alt, 95)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide raw input file.")
        sys.exit(1)
    with open(sys.argv[1], "r") as infile:
        raw_data = yaml.load(infile)
        P = 100
        if len(sys.argv) == 3:
            P = int(sys.argv[2])
        compute_statistics(raw_data, P)
