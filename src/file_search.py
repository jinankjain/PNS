import os
import inspect

SEARCH_ABS_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def search(page_id, key):
    f = os.path.join(SEARCH_ABS_PATH, "pages", page_id)
    command = "./pts_lbsearch -pi {} {}".format(f, key)
    os.system(command)


search('9', '90b1c62c68683be9276d538174e551a41ca3b30811789eb46b85c15afca7dc0d')