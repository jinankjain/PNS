import get_name_server
import hashlib
import os
import time

INPUT_FILE_NAME = "top_1m.txt"
PAGE_INDEX = 1
PAGE_STORAGE = "pages"

def generate_page( ):
    f = open(INPUT_FILE_NAME, 'r')
    f_iter = iter(f)

    for line in f_iter:
        temp = line.split()
        temp = temp[2][1:-1]
        fqdn_hash = hashlib.sha256(str(temp).encode('utf-8')).hexdigest()
        ns_ipv4 = get_name_server.find_nameserver(temp)
        fs = open(os.path.join(PAGE_STORAGE, fqdn_hash[0:PAGE_INDEX]), 'a')
        print(fqdn_hash + " " + ns_ipv4 + " " + time.strftime("%c"))
        fs.write(fqdn_hash + " " + ns_ipv4 + " " + time.strftime("%c") + "\n")
        fs.close()
    f.close()


def main( ):
    generate_page()


if __name__ == "__main__":
    main()
