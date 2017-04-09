import requests
from src.utils import *

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


def get_page_without_version(page_id):
    path = os.path.join(USER_DIR, CACHE_DIR)
    page_path = os.path.join(path, page_id)
    if os.path.exists(page_path):
        version = get_page_current_version(path, page_id)
        get_page_diff_with_version(page_id, version)
    else:
        url = "{}get_page".format(API_URL)
        r = requests.get(url, params={'page_id': page_id})
        save_page(r.text, page_id)
        verify_signature(page_id)


def get_page_diff_with_version(page_id, version):
    url = "{}get_page".format(API_URL)
    r = requests.get(url, params={'page_id': page_id, 'version': version})
    if r.text == '"Updated"':
        return True
    else:
        diff_path = save_diff(r.text, page_id, version)
        old_version_path = os.path.join(USER_DIR, CACHE_DIR, page_id)
        apply_patch(diff_path, old_version_path)


def apply_patch(diff_path, old_version_path):
    command = "patch {} {}".format(old_version_path, diff_path)
    os.system(command)


def verify_signature(page_id):
    url = "{}get_signature".format(API_URL)
    r = requests.get(url, params={'page_id': page_id})
    signature = r.text.split('"')[1]
    print(signature)
    page_path = os.path.join(USER_DIR, CACHE_DIR)
    result = verify_signature_page(signature, page_path, page_id)
    if result == "Failed":
        # Don't save the file
        os.remove(os.path.join(page_path, page_id))
    else:
        print("Successfully downloaded the page")


def diff_verify_signature(diff_content, signature):
    result = verify_signature_diff(signature, diff_content)


get_page_without_version("0")