import numpy as np
import os
import sys
import time
import yaml

from collections import defaultdict
from datetime import datetime

_TIME_FMT = "%Y-%m-%dT%H:%M:%S"


class Analyzer:
    def __init__(self):
        self.authoritative_nses = {}
        self.changes = defaultdict(int)
        self.start = None
        self.end = None

    def add_file(self, filename):
        timestamp = self._extract_timestamp(filename)
        if not timestamp:
            print("Could not parse %s." % filename)
            return
        else:
            print("Processing %s." % filename)
        if not self.start:
            self.start = timestamp
        self.end = timestamp
        with open(filename) as infile:
            data = yaml.load(infile)
            print("Data contains %d domains." % len(data))
            if not self.authoritative_nses:
                self.authoritative_nses = data
            else:
                self._add_changes(data)

    def compute_statistics(self):
        N = len(self.changes)
        nchanges = np.array([n for _, n in self.changes.items()])
        np.sort(nchanges)
        ndomains = len(self.authoritative_nses)
        print("Statistics about authoritative NS changes between %s and %s "
              "(%s) for %d domains:" % (self.start.strftime(_TIME_FMT),
                                        self.end.strftime(_TIME_FMT),
                                        self.end - self.start,
                                        ndomains))
        print("Domains with no changes: %d" % (ndomains - N))
        print("Domains with at least one change: %d" % N)
        print("Total changes: %d" % np.sum(nchanges))
        print("Min: %d" % np.min(nchanges))
        print("Max: %d" % np.max(nchanges))
        print("Mean: %.2f" % np.mean(nchanges))
        print("Median: %d" % np.median(nchanges))
        print("95th: %d" % np.percentile(nchanges, 95))

    def _extract_timestamp(self, filename):
        assert filename
        parts = filename.split('-', 1)
        ts_string = parts[1].split('.')[0]
        assert ts_string
        time_struct = time.strptime(ts_string, _TIME_FMT)
        timestamp = datetime.fromtimestamp(time.mktime(time_struct))
        return timestamp

    def _add_changes(self, data):
        for domain, nses in data.items():
            if domain not in self.authoritative_nses:
                # First time we see this domain, don't count changes.
                self.authoritative_nses[domain] = nses
            else:
                current_domain_nses = self.authoritative_nses[domain]
                has_changes = False
                for ns_name, ns_ip in nses.items():
                    if (ns_name not in current_domain_nses.keys() or
                            current_domain_nses[ns_name] != ns_ip):
                        current_domain_nses[ns_name] = ns_ip
                        has_changes = True
                if has_changes:
                    self.changes[domain] += int(has_changes)

if __name__ == "__main__":
    analyzer = Analyzer()
    for _, _, files in os.walk('.'):
        sorted_files = sorted(files)
        for file in sorted_files:
            if file.endswith(".yml"):
                analyzer.add_file(file)
    analyzer.compute_statistics()
