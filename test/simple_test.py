import requests
from src.utils import *
import timeit

API_URL = "http://localhost:5000/"
CACHE_DIR = ".pns_test"
USER_DIR = os.path.expanduser('~')
DIFF_SUFFIX = ".diff"


def get_page_without_version(page_id):
    url = "{}get_page".format(API_URL)
    r = requests.get(url, params={'page_id': page_id})
    save_page(r.text, page_id)
    verify_signature(page_id)


def verify_signature(page_id):
    url = "{}get_signature".format(API_URL)
    r = requests.get(url, params={'page_id': page_id})
    signature = r.text.split('"')[1]
    page_path = os.path.join(USER_DIR, CACHE_DIR)
    result = verify_signature_page(signature, page_path, page_id)
    if result == "Failed":
        # Don't save the file
        os.remove(os.path.join(page_path, page_id))
    # else:
        # continue
        # print("Successfully downloaded the page")


def new_verify_signature(signature, page_id):
    page_path = os.path.join(USER_DIR, CACHE_DIR)
    result = verify_signature_page_test(signature, page_path, page_id)
    if result == "Failed":
        # Don't save the file
        os.remove(os.path.join(page_path, page_id))
    # else:
        # continue
        # print("Successfully downloaded the page")


def save_page(page_data, page_id):
    cache_path = os.path.join(USER_DIR, CACHE_DIR)
    page_path = os.path.join(cache_path, page_id)
    if os.path.exists(cache_path):
        f = open(page_path, 'w+')
        f.write(page_data)
    else:
        os.mkdir(cache_path)
        f = open(page_path, 'w+')
        f.write(page_data)

    return page_path


def new_approach():
    url = "{}test_signature".format(API_URL)
    r = requests.get(url)
    signature = r.text.split('\n')[-1]
    save_page(r.text, "0_part2")
    new_verify_signature(signature, "0_part2")


# cProfile.run('get_page_without_version("0")')
# cProfile.run('new_approach()')

start_time = timeit.default_timer()
for i in range(0, 1):
    new_approach()
print((timeit.default_timer() - start_time)/1)

start_time = timeit.default_timer()
for i in range(0, 1):
    get_page_without_version("0")
print((timeit.default_timer() - start_time)/1)