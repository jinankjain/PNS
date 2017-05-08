import argparse
import logging
import urlparse
import yaml

from alexa_fetcher import get_top_domains
from collections import defaultdict
from proxy2 import ProxyRequestHandler, ThreadingHTTPServer


class RequestCollector:
    """Collects all requests and aggregates them."""
    def __init__(self):
        self.alexa_top_n = None
        self.outfile = None
        self.current_url = ""
        self.current_stats = {}

    def configure(self, n, start_from, outfile):
        self.alexa_top_n = set(get_top_domains(n, start_from))
        self.outfile = outfile

    def add_request(self, url):
        parse_result = urlparse.urlparse(url)
        if not parse_result.netloc:
            return
        # Check whether this request starts a new request chain.
        if (parse_result.path == '/' and parse_result.netloc in self.alexa_top_n
                and parse_result.netloc != self.current_url):
            logging.info("New request chain detected for %s." %
                         parse_result.netloc)
            if self.current_url:
                logging.info("Writing results for %s." % self.current_url)
            # Write previous results to file.
            yaml.dump({self.current_url: dict(self.current_stats)},
                      stream=self.outfile, default_flow_style=False)
            # Reset counters.
            self.current_url = parse_result.netloc
            self.current_stats = defaultdict(int)
        else:
            # Get second level domain from url.
            domain_parts = parse_result.netloc.split('.')
            if len(domain_parts) < 2:
                return
            domain = '.'.join(domain_parts[-2:])
            self.current_stats[domain] += 1
            logging.debug("Registered request to %s for base request %s." %
                           (domain, self.current_url))

    def flush(self):
        if self.current_url and self.current_stats:
            print("Flushing results.")
            yaml.dump({self.current_url: dict(self.current_stats)},
                      stream=self.outfile, default_flow_style=False)

_request_collector = RequestCollector()


class RequestCollectorProxyHandler(ProxyRequestHandler):
    def save_handler(self, req, req_body, res, res_body):
        _request_collector.add_request(req.path)


def run(port=8080, ServerClass=ThreadingHTTPServer, protocol="HTTP/1.1"):
    server_address = ('', port)

    RequestCollectorProxyHandler.protocol_version = protocol
    httpd = ServerClass(server_address, RequestCollectorProxyHandler)

    sa = httpd.socket.getsockname()
    logging.info("Serving HTTP Proxy on %s port %s..." % (sa[0], sa[1]))
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=10000)
    parser.add_argument("--start-from", type=int, default=0)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--out", default="results/dns_lookups.yml")
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level,
                        format="%(asctime)s %(levelname)s: %(message)s")
    with open(args.out, "a") as outfile:
        _request_collector.configure(args.n, args.start_from, outfile)
        try:
            run(port=args.port)
        finally:
            _request_collector.flush()
