from __future__ import print_function
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import sys

def file_len(fname):
    with open(fname) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def ttl_generator(file_names):
    try:
        for file_name in file_names:
            with open(file_name, 'r') as data_file:
                for line in data_file:
                    fields = line.strip().split()
                    if len(fields) < 2 or not fields[1].isdigit():
                        continue
                    yield int(fields[1])
    except IOError as e:
        print("Unable to open file", file=sys.stderr)
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("This script requires one file as input", file=sys.stderr)
        sys.exit(1)
    ttls_list = list(ttl_generator(sys.argv[1:]))
    ttls_array = np.array(ttls_list)
    counts = Counter(ttls_array)
    min_frequency = int(max(counts.values()) / 10000)
    for ttl in counts.keys():
        if counts[ttl] < min_frequency:
            del counts[ttl]

    bins = [x - 0.5 for x in counts.keys()] + [x + 0.5 for x in counts.keys()]
    bins.append(max(counts)+11000)
    bins.sort()
    plt.hist(ttls_array, bins, cumulative=True, histtype='step', normed=True)
    ax = plt.gca()
    #Set maximum to 1 for normed y-axis (cumulative distrib)
    ax.set_ylim([ax.get_ylim()[0], 1.0])
    ax.set_xlim([ax.get_xlim()[0], max(counts)+10000])
    ax.yaxis.grid(True)
    lowest_count_shown = counts.most_common(4)[-1][1]
    plt.xticks([k for k in counts.keys() if counts[k] >= lowest_count_shown])
    plt.yticks(np.arange(0, 1.04, 0.05))
    plt.show()
    plt.close()
    # Plot counter
    #plt.bar(counts.keys(), counts.values(), width=5000)
    #plt.show()

