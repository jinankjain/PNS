
import cStringIO
from urllib import urlopen

IANA_DATA_URL = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'


def tld_iterator():
    """
    Generator that:
        Downloads the list of TLDs from the iana website,
        and returns them one at a time.
    """

    f = urlopen(IANA_DATA_URL)
    buf = cStringIO.StringIO(f.read())
    next(buf)
    for line in buf:
        yield line.rstrip()
    #buf = cStringIO.StringIO(f.read())
    #zfile = zipfile.ZipFile(buf)
    #buf = cStringIO.StringIO(zfile.read('top-1m.csv'))
    #for line in buf:
    #    (rank, domain) = line.split(',')
    #    yield (int(rank), domain.strip())

if __name__ == "__main__":
    for domain in tld_iterator():
        print domain
