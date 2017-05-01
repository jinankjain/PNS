from src.crypto import *

UTIL_ABS_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


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


def create_tmp_page(page_id):
    path_p = "pages"
    abs_path = os.path.join(UTIL_ABS_PATH, path_p, page_id)
    tmp_path = os.path.join(UTIL_ABS_PATH, path_p, page_id + "_tmp")
    if os.path.exists(tmp_path): return
    else:
        command = "cp {} {}".format(abs_path, tmp_path)
        os.system(command)


def replace_page_with_new_page():
    page_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    path_p = "pages"

    for p in page_id:
        abs_path = os.path.join(UTIL_ABS_PATH, path_p, p)
        tmp_path = os.path.join(UTIL_ABS_PATH, path_p, p+"_tmp")

        command = "cp {} {}".format(tmp_path, abs_path)
        os.system(command)


