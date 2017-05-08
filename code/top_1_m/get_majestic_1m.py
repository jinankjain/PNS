
#Adapted from https://github.com/davedash/Alexa-Top-Sites/blob/master/alexa/__init__.py
"""
This script downloads the Majestic Million top 1M sites, unzips it, and reads
the CSV and returns a list of the top N sites.
"""

import zipfile
import cStringIO
from urllib import urlopen

MAJ_DATA_URL = 'http://downloads.majestic.com/majestic_million.csv'


def majestic_etl():
    """
    Generator that:
        Extracts by downloading the csv.zip, unzipping.
        Transforms the data into python via CSV lib
        Loads it to the end user as a python list
    """

    f = urlopen(MAJ_DATA_URL)
    buf = cStringIO.StringIO(f.read())
    next(buf) # Ignore the header
    for line in buf:
        splitted = line.split(',')
        rank = splitted[0]
        domain = splitted[2]
        yield (int(rank), domain.strip())


def top_list(num=100):
    a = majestic_etl()
    return [a.next() for x in xrange(num)]


if __name__ == "__main__":
    for _, domain in majestic_etl():
        print domain
