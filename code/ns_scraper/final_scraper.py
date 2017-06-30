import dns.query
import dns.resolver
import dns.message
import dns.name
import dns.query
import dns.rcode
import dns.rdatatype
import dns.resolver
from dns.exception import DNSException
from get_alexa_10k import get_10K_domains
import argparse
import logging
import time
import datetime
import os
import yaml

_error_logger = logging.getLogger('ErrorLogger')
_console_logger = logging.getLogger('ConsoleLogger')

_RESULTS_DIR = "results/"
_ERROR_DIR = "errors/"

def _config_error_logger(_ERROR_LOG):
    file_handler = logging.FileHandler(_ERROR_LOG, mode="w")
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    _error_logger.setLevel(logging.ERROR)
    _error_logger.addHandler(file_handler)


def _config_console_logger(log_level):
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    stream_handler.setFormatter(formatter)
    _console_logger.setLevel(log_level)
    _console_logger.addHandler(stream_handler)


def _log_error(error: str, domain: str):
    _error_logger.error("An error occurred when looking up the authoritative NS"
                        " for %s:\n%s" % (domain, error))

def query_authoritative_ns (domain, outfile, log=lambda msg: None):

    default = dns.resolver.get_default_resolver()
    ns = default.nameservers[0]

    n = domain.split('.')
    ns_all = []
    ns_name = []
    ttl = []
    for i in range(0, len(n)):
        sub = '.'.join(n[i-1:])

        # log('Looking up %s on %s' % (sub, ns))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        try:
            response = dns.query.udp(query, ns, timeout=10)

            rcode = response.rcode()
            if rcode != dns.rcode.NOERROR:
                _log_error("Received rcode %d" % response.rcode(),
                           domain)
                return [],[]

            if len(response.authority) > 0:
                rrsets = response.authority
            elif len(response.additional) > 0:
                rrsets = [response.additional]
            else:
                rrsets = response.answer

            # Handle all RRsets, not just the first one
            i = 0
            j = 0
            for rrset in rrsets:
                j = 0
                for rr in rrset:               
                    if rr.rdtype == dns.rdatatype.SOA:
                        pass
                        # log('Same server is authoritative for %s' % (sub))
                    elif rr.rdtype == dns.rdatatype.A:
                        ns = rr.items[0].address
                        # log('Glue record for %s: %s' % (rr.name, ns))
                    elif rr.rdtype == dns.rdatatype.NS:
                        authority = rr.target
                        ns = default.query(authority).rrset[0].to_text()
                        # log('%s [%s] is authoritative for %s; ttl %i' % 
                        #         (authority, ns, sub, rrset.ttl))
                        if j == 0 and ns != "":
                            ns_all = []
                            ns_name = []
                            ttl = []
                        ns_all.append(ns)
                        ns_name.append(authority)
                        ttl.append(rrset.ttl)
                        result = rrset
                    else:
                        # IPv6 glue records etc
                        #log('Ignoring %s' % (rr))
                        pass
                    j+=1
                i+=1
        except dns.exception.DNSException as error:
            _log_error(str(error), domain)
            return [], []
        except Exception as error:
            _console_logger.error("Captured an exception while handling %s:\n%s" %
                                  (domain, str(error)))
            return [], []

    new = zip(ns_name,ns_all)
    new = list(sorted(new))
    return new, ttl

import sys

def log (msg):
    sys.stderr.write(msg + u'\n')

def scrape(ndomains, outfile):
    report_threshold = max(int(ndomains / 100), 1)
    res = get_10K_domains()
    for i in range(len(res)):
        new1, ttl1 = query_authoritative_ns(res[i][1], outfile, log)
        new2, ttl2 = query_authoritative_ns(res[i][1], outfile, log)
        new3, ttl3 = query_authoritative_ns(res[i][1], outfile, log)

        new = new1
        ttl = ttl1
        temp = len(new2)
        while(i<temp):
            found_match = False
            for j in range(0, len(new)):
                if(new[j][0] == new2[i][0]):
                    found_match = True
            if not found_match:
                new.append(new2[i])
                ttl.append(ttl2[i])
            i = i+1
        temp = len(new3)
        while(i<temp):
            found_match = False
            for j in range(0, len(new)):
                if(new[j][0] == new3[i][0]):
                    found_match = True
            if not found_match:
                new.append(new3[i])
                ttl.append(ttl3[i])
            i = i+1
        print(res[i][1], res[i][0], file=outfile)
        for i in range(0, len(new)):
            print(new[i][0], new[i][1], ttl[i], file=outfile)
        print(file=outfile)
        idx = i
        if (idx + 1) % report_threshold == 0:
            progress_percentage = int((idx + 1) / ndomains * 100)
            _console_logger.info("Progress: %d of %d (%d%%)" %
                                 (idx + 1, ndomains, progress_percentage))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scrape-interval",
                        dest="scrape_interval",
                        help="Interval to scrape domains.",
                        type=int,
                        required=True)
    parser.add_argument("-n", dest="n", help="Top N domains", type=int,
                        default=30000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    _config_console_logger(log_level)
    scrape_interval_counter = 1
    while True:
        _console_logger.info("Starting scrape interval %d" %
                             scrape_interval_counter)
        start_unix_secs = time.time()
        start = datetime.datetime.now()
        fname = "ns_scrape-" + start.strftime("%Y-%m-%dT%H:%M:%S") + ".yml"
        epath = os.path.join(_ERROR_DIR, fname)
        _config_error_logger(epath)
        path = os.path.join(_RESULTS_DIR, fname)
        _console_logger.info("Writing results to: %s" % path)
        # Open new file
        with open(path, "w") as outfile:
            scrape(args.n, outfile)
        end = datetime.datetime.now()
        _console_logger.info("Finished scrape interval %d in %s." %
                             (scrape_interval_counter, end - start))
        scrape_interval_counter += 1
        end_unix_secs = time.time()
        duration = end_unix_secs - start_unix_secs
        if duration > args.scrape_interval:
            _console_logger.warning("Scraping took longer than the scrape "
                                    "interval (%d s vs %d s)" %
                                    (duration, args.scrape_interval))
        else:
            sleep_duration = args.scrape_interval - duration
            _console_logger.info("Sleeping for %d s" % sleep_duration)
            time.sleep(sleep_duration)
