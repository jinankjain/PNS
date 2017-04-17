import requests
from src.utils import *
import timeit

API_URL = "http://localhost:5000/"
CACHE_DIR = ".pns"
USER_DIR = os.path.expanduser('~')
DIFF_SUFFIX = ".diff"


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


def save_diff(diff_content, page_id, version):
    # TODO: Check if the page is present on which we are trying to apply patch

    file_name = "{}_{}{}".format(page_id, version, DIFF_SUFFIX)
    diff_path = os.path.join(USER_DIR, CACHE_DIR, file_name)
    f = open(diff_path, 'w+')
    f.write(diff_content)
    return diff_path


def get_page_without_version(page_id, thread_id=""):
    path = os.path.join(USER_DIR, CACHE_DIR)
    page_path = os.path.join(path, page_id)
    if os.path.exists(page_path):
        version = get_page_current_version(path, page_id)
        get_page_diff_with_version(page_id, version)
    else:
        url = "{}get_page".format(API_URL)
        req = "page_id: {} ".format(page_id)
        start_time_net = timeit.default_timer()
        r = requests.get(url, params={'page_id': page_id})
        save_page(r.text, page_id+thread_id)
        ans = timeit.default_timer() - start_time_net
        req += "net_lat: {} ".format(ans)
        start_time_ver = timeit.default_timer()
        verify_signature(page_id, thread_id)
        ans = timeit.default_timer() - start_time_ver
        req += "ver_time: {}".format(ans)
        print(req)


def get_page_diff_with_version(page_id, version):
    url = "{}get_page".format(API_URL)
    r = requests.get(url, params={'page_id': page_id, 'version': version})
    if r.text == '"Updated"':
        return True
    else:
        diff_path = save_diff(r.text, page_id, version)
        old_version_path = os.path.join(USER_DIR, CACHE_DIR, page_id)
        diff_content, signature = extract_signature(diff_path)
        result = diff_verify_signature(diff_content, signature)
        if result == "Failed":
            print("Unsuccessful")
            os.remove(diff_path)
        apply_patch(diff_path, old_version_path)


def apply_patch(diff_path, old_version_path):
    command = "patch {} {}".format(old_version_path, diff_path)
    os.system(command)


def extract_signature(diff_path):
    f = open(diff_path, 'r')
    start = f.readline()
    start += f.readline()
    diff_content = []
    for c in f:
        diff_content.append(c)
    signature = diff_content[-1]
    diff_content = diff_content[0:-1]
    diff_content = ''.join(diff_content)
    # print(diff_content)
    start += diff_content
    f.close()
    # print(signature)
    f = open(diff_path, 'w+')
    f.write(start)
    return diff_content, signature


def verify_signature(page_id, thread_id=""):
    url = "{}get_signature".format(API_URL)
    r = requests.get(url, params={'page_id': page_id})
    signature = r.text
    # print(signature)
    page_path = os.path.join(USER_DIR, CACHE_DIR)
    result = verify_signature_page(signature, page_path, page_id+thread_id)
    if result == "Failed":
        # Don't save the file
        print("Unsuccessful")
        os.remove(os.path.join(page_path, page_id))


def diff_verify_signature(diff_content, signature):
    result = verify_signature_diff(signature, diff_content)
    return result


# get_page_without_version("1")