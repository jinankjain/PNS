WORKING_DATA_URL = "alexa-top-1m-2017-05-01.csv.zip"

def get_10K_domains():
    """
    Random sampling of 10K domains from
    set of 1M domain set.
    """
    
    f = open(WORKING_DATA_URL, 'r')
    
    domains = []
    same_domain = False
    for domain in f:
        domain = domain.strip()
        if not same_domain:
            domains.append(domain.split(' '))
            same_domain = True

        if not domain:
            same_domain = False

    return domains[:10000]
if __name__ == '__main__':
    print(get_10K_domains())
