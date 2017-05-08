
#Adapted from https://github.com/davedash/Alexa-Top-Sites/blob/master/alexa/__init__.py
"""
This script downloads the Cisco Umbrella top 1M sites, unzips it, and reads the
CSV and returns a list of the top N sites.
"""

import zipfile
import cStringIO
from urllib import urlopen

CISCO_DATA_URL = 'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip'


def cisco_etl():
    """
    Generator that:
        Extracts by downloading the csv.zip, unzipping.
        Transforms the data into python via CSV lib
        Loads it to the end user as a python list
    """

    f = urlopen(CISCO_DATA_URL)
    buf = cStringIO.StringIO(f.read())
    zfile = zipfile.ZipFile(buf)
    buf = cStringIO.StringIO(zfile.read('top-1m.csv'))
    for line in buf:
        (rank, domain) = line.split(',')
        yield (int(rank), domain.strip())


def top_list(num=100):
    a = cisco_etl()
    return [a.next() for x in xrange(num)]


if __name__ == "__main__":
    for _, domain in cisco_etl():
        print domain
