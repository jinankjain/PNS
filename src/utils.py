from src.combine_diff import *
from src.crypto import *
import operator
import csv
import netaddr
import time

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
    path_p = os.path.join(UTIL_ABS_PATH, "pages")

    for p in page_id:
        path = os.path.join(path_p, p+"_tmp")
        if os.path.exists(path):
            result = update_version(path_p, p+"_tmp")
            diff = Diff()
            new_version = get_page_current_version(path_p, p+"_tmp")
            diff.generate_diffs(new_version, p, path_p)

    generate_new_sig_files()


def sort_all_the_pages():
    page_id = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    path_p = "pages"

    for p in page_id:
        abs_path = os.path.join(UTIL_ABS_PATH, path_p, p)
        sample = open(abs_path)
        csv1 = csv.reader(sample, delimiter=' ')
        sort = sorted(csv1, key=operator.itemgetter(0))
        sample.close()
        f = open(abs_path, 'w')
        for eachline in sort:
            ans = [eachline[0]]
            for word in eachline[1:]:
                try:
                    ip = str(int(netaddr.IPAddress(word)))
                    ans.append(ip)
                except netaddr.core.AddrFormatError:
                    ans.append(str(int(time.time())))
                    break
            f.write(' '.join(ans) + '\n')
        f.close()


# sort_all_the_pages()

