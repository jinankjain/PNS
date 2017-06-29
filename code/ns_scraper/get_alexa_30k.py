import zipfile
import io
import random

# Random seed for generating the results in a repetetive way
random.seed(1119)

# Random sampling to get 30K domains from 1M domain set
domain_ids = random.sample(range(1, 1000001), 30000)
assert(len(domain_ids) == 30000)
domain_ids.sort()

ALEXA_DATA_URL = "alexa-top-1m-2017-05-01.csv.zip"

def get_30K_domains():
    """
    Random sampling of 30K domains from
    set of 1M domain set.
    """

    zfile = zipfile.ZipFile(ALEXA_DATA_URL)

    buf = io.BytesIO(zfile.read('top-1m.csv'))
    result = []
    i = 0
    for line in buf:
        line = line.decode('utf-8')
        (rank, domain) = line.split(',')
        if i<30000 and int(rank) == domain_ids[i]:
            result.append((int(rank), domain.strip()))
            i += 1
    return result

if __name__ == '__main__':
    print(get_30K_domains())