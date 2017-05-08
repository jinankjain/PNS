from __future__ import print_function
import dns.flags
import dns.resolver
import dns.rdatatype
import dns.rdataclass
import sys

DEFAULT = dns.resolver.get_default_resolver()

def get_authoritative_ns(domain, log=lambda msg: None):
    """
    Return the DNS response containing the NS of the given domain, if it can be
    found, or the response containing an error message if the lookup fails.
    """
    n = dns.name.from_text(domain)

    #nameserver = DEFAULT.nameservers[0]
    nameserver = '198.41.0.4' #dig a.root-servers.net

    last = False
    depth = 2 # Depth 1 is '.', the root
    while not last:
        s = n.split(depth)

        last = s[0].to_unicode() == u'@'
        sub = s[1]

        log('Looking up %s on %s' % (sub, nameserver))
        query = dns.message.make_query(sub, dns.rdatatype.NS, want_dnssec=True)
        response = dns.query.udp(query, nameserver, timeout=5)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            # Let the caller handle the error
            return response
            #if rcode == dns.rcode.NXDOMAIN:
            #    raise Exception('%s does not exist.' % sub)
            #else:
            #    raise Exception('Error %s' % dns.rcode.to_text(rcode))

        rrset = None
        if len(response.authority) > 0:
            rrset = response.authority[0]
        else:
            rrset = response.answer[0]

        rr = rrset[0]
        if rr.rdtype == dns.rdatatype.SOA:
            log('Same server is authoritative for %s' % sub)
        else:
            authority = rr.target
            log('%s is authoritative for %s' % (authority, sub))
            # Sometimes the following will raise a dns.resolver.NXDOMAIN
            # exception: this should not happen, since if we get this far it
            # means that we already got the authority by doing an iterative
            # query starting at the root. However for some reason (configuration
            # error?) sometimes this happens.
            nameserver = DEFAULT.query(authority).rrset[0].to_text()
            ns_response = response

        depth += 1

    return ns_response, nameserver

def get_dnskey_response(domain, nameserver=DEFAULT.nameservers[0], log=lambda msg: None):
    log('Looking up DNSKEY for %s on %s' % (domain, nameserver))
    query = dns.message.make_query(domain, dns.rdatatype.DNSKEY, want_dnssec=True)
    return dns.query.udp(query, nameserver, timeout=5)

def log (msg):
    """Simple logging function, writes to stderr."""
    sys.stderr.write(msg + u'\n')

def lookup_and_get_ttls(domain, output_files_by_rdtype):
    """
    Looks up the given domain, finds its nameserver, and prints the TTL
    information for the records it finds to the files specified in the
    output_files_by_rdtype dictionary. This dictionary should contain a number
    of rdatatypes as keys with associated open files to which the TTLs of the
    rrset are written.
    """
    ns_failed = False
    dnskey_failed = False
    try:
        ns_response, nameserver = get_authoritative_ns(domain, log)
    except Exception as e:
        ns_failed = True
        log('Lookup failed unexpectedly' + str(e))
#    else:
#        try:
#            # Instead of using the original domain, e.g., www.inf.ethz.ch, we
#            # use the highest level domain for which the nameserver
#            # authoritative for www.inf.ethz.ch is authoritative, e.g., ethz.ch.
#            last_domain = ns_response.question[0].name
#            dnskey_response = get_dnskey_response(last_domain, nameserver, log)
#        except Exception as e:
#            dnskey_failed = True
#            log('Lookup of DNSKEY failed' + str(e))
    for rdtype, outfile in output_files_by_rdtype.iteritems():
        print(domain, end=' ', file=outfile)
        is_dnskey = rdtype == dns.rdatatype.DNSKEY
        if ns_failed or (is_dnskey and dnskey_failed):
            print('FAILED', file=outfile)
            continue
        response = dnskey_response if is_dnskey else ns_response
        if response.rcode() != dns.rcode.NOERROR:
            print('FAILED' + ' ' + dns.rcode.to_text(response.rcode()),
                  file=outfile)
            continue
        for rrset in (response.authority + response.answer +
                response.additional):
            if rrset.rdtype == rdtype:
                print(rrset.ttl, end=' ', file=outfile)
        print('', file=outfile) # Terminate current record with newline

if __name__ == "__main__":
    output_files_by_rdtype = {}
    #output_files_by_rdtype[dns.rdatatype.A] = open('a_output.txt', 'w+')
    output_files_by_rdtype[dns.rdatatype.NS] = open('ns_output.txt', 'w+')
    #output_files_by_rdtype[dns.rdatatype.DS] = open('ds_output.txt', 'w+')
    #output_files_by_rdtype[dns.rdatatype.RRSIG] = open('rrsig_output.txt', 'w+')
    #output_files_by_rdtype[dns.rdatatype.DNSKEY] = open('dnskey_output.txt', 'w+')
    try:
        if len(sys.argv) < 2:
            #print("reading from stdin..")
            data_file = sys.stdin
        else:
            try:
                data_file = open(sys.argv[1], 'r')
            except IOError as e:
                print("Unable to open file", file=sys.stderr)
                print(str(e), file=sys.stderr)
                sys.exit(1)
        #lookup_and_get_ttl("com")
        for line in data_file:
            lookup_and_get_ttls(line.rstrip(), output_files_by_rdtype)
    finally:
        for outfile in output_files_by_rdtype.values():
            outfile.close()

