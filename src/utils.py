import os
import fileinput

PAGE_STORAGE = "../test/pages"


def get_page_current_version( page_id ):
    page_path = os.path.join(PAGE_STORAGE, page_id)
    result = ""
    try:
        version = open(page_path, 'r').readline().split()
        result = version[1].strip("\n")
    except FileNotFoundError:
        result = "-1"
    return result

def update_version( page_id ):
    page_path = os.path.join(PAGE_STORAGE, page_id)
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
