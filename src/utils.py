import os
from src.crypto import *

def get_page_current_version( page_path, page_id ):
    page_path = os.path.join(page_path, page_id)
    result = ""
    try:
        version = open(page_path, 'r').readline().split()
        result = version[1].strip("\n")
    except FileNotFoundError:
        result = "-1"
    return result


def update_version( page_path, page_id ):
    page_path = os.path.join(page_path, page_id)
    result = "Error"
    try:
        version = open(page_path, 'r').readline().split()
        version[1] = str((int(version[1]) + 1))
        version = ' '.join(version)
        command = "sed -i '' '1s/.*/{}/' ".format(version) + page_path
        os.system(command)
        result = "Success"
    except FileNotFoundError:
        result = "Error"
    return result


def append_signature_diff(diff_path):
    f = open(diff_path, 'r+')

    # Skip first two lines
    f.readline()
    f.readline()
    diff_content = ""
    for c in f:
        diff_content += c
    signature = compute_signature_diff(diff_content)
    f.write(signature.decode("utf-8"))
