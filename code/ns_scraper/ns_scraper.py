import argparse

import datetime
import ipaddress
import os

import dns.exception
import dns.message
import dns.name
import dns.query
import dns.rcode
import dns.rdatatype
import dns.resolver
import logging
import sys
import time
import yaml

from alexa_fetcher import get_top_domains

_ROOT_NS_ADDRESS = "198.41.0.4"
_RESULTS_DIR = "results/"
_ERROR_LOG = "error.out"

_error_logger = logging.getLogger('ErrorLogger')
_console_logger = logging.getLogger('ConsoleLogger')

default = dns.resolver.get_default_resolver()

def _config_error_logger():
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


def _get_authoritative_ns(qname: dns.name.Name, nameserver: str):
    """Performs a DNS request for domain at a certain depth."""
    # Check that nameserver is wellformed.
    try:
        ipaddress.ip_address(nameserver)
    except ValueError:
        _log_error("Malformed NS IP: %s" % nameserver, qname.to_unicode(True))
        return []
    query = dns.message.make_query(qname, dns.rdatatype.NS)
    try:
        response = dns.query.udp(query, nameserver, timeout=5)
        if response.rcode() != dns.rcode.NOERROR:
            _log_error("Received rcode %d" % response.rcode(),
                       qname.to_text(True))
            return []
        # Check that we have something in the authority section and extract
        # addresses of the authoritative nameservers.
        if len(response.authority) > 0:
            rrsets = response.authority
        elif len(response.additional) > 0:
            rrsets = [response.additional]
        else:
            rrsets = response.answer

        # Handle all RRsets, not just the first one
        for rrset in rrsets:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.SOA:
                    print('Same server is authoritative for')
                elif rr.rdtype == dns.rdatatype.A:
                    ns = rr.items[0].address
                    print('Glue record for %s: %s' % (rr.name, ns))
                elif rr.rdtype == dns.rdatatype.NS:
                    authority = rr.target
                    ns = default.query(authority).rrset[0].to_text()
                    print('%s [] is authoritative for %s; ttl %i' % 
                        (authority, ns, rrset.ttl))
                    result = rrset
                else:
                    # IPv6 glue records etc
                    #log('Ignoring %s' % (rr))
                    pass

        if response.authority and response.additional:
            filtered_additional = [item for item in response.additional
                                   if item.rdtype == dns.rdatatype.A]
            # Sort NS list according to their domain names.
            sorted_additional = sorted(filtered_additional,
                                       key=lambda item: item.name.to_text())
            # Return list of tuples of NS (name, address)
            result = []
            for ns_item in sorted_additional:
                name = ns_item.name.to_unicode(True)
                address = ns_item.items[0].address
                if isinstance(address, bytes):
                    address = address.decode("utf-8")
                result.append((name, address))
            return result
        else:
            return []

    except dns.exception.DNSException as error:
        _log_error(str(error), qname.to_text(True))
        return []
    except Exception as error:
        _console_logger.error("Captured an exception while handling %s:\n%s" %
                              (qname.to_unicode(True), str(error)))
        return []


def scrape(ndomains, outfile):
    report_threshold = max(int(ndomains / 100), 1)
    for (idx, domain) in enumerate(get_top_domains(ndomains)):
        depth = 2
        fqdn = dns.name.from_text("www." + domain)
        nameserver = _ROOT_NS_ADDRESS
        done = False
        while not done:
            prefix, qname = fqdn.split(depth)
            done = prefix.to_unicode() == u'@'

            _console_logger.debug("Looking up %s on %s" % (qname, nameserver))
            nameservers = _get_authoritative_ns(qname, nameserver)
            if nameservers:
                if (qname.to_unicode(True) == domain or
                    qname.to_unicode(True) == "www." + domain):
                    yaml.dump({qname.to_unicode(True): dict(nameservers)},
                              stream=outfile,
                              default_flow_style=False)
                nameserver = nameservers[0][1]
            depth += 1
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
                        default=100000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    _config_error_logger()
    _config_console_logger(log_level)
    scrape_interval_counter = 1
    while True:
        _console_logger.info("Starting scrape interval %d" %
                             scrape_interval_counter)
        start_unix_secs = time.time()
        start = datetime.datetime.now()
        fname = "ns_scrape-" + start.strftime("%Y-%m-%dT%H:%M:%S") + ".yml"
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


