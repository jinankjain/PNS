import os
import requests
from src.crypto import *
from src.combine_diff import *

API_URL = "http://localhost:5000/"

def get_page_without_version(page_id):
    url = "{}get_page".format(API_URL)
    print(url)
    r = requests.get(url, params = {'page_id' : page_id})
    print(r.text)


def get_page_diff_with_version(page_id, version):
    url = "{}get_page".format(API_URL)
    print(url)
    r = requests.get(url, params={'page_id': page_id, 'version': version})
    print(r.text)


def apply_patch():
    pass


def verify_signature():
    pass

get_page_diff_with_version(0, 1)