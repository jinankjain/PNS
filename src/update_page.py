import time
from src.combine_diff import *


def update_page(page_id, fqdn_sha256, ns_record, page_path):
    version = get_page_current_version(page_path, page_id)
    version = str(int(version) + 1)
    copy_page(page_path, page_id, version)
    new_page_path = os.path.join(page_path, page_id+"_"+version)
    update_version(page_path, page_id+"_"+version)
    file = open(new_page_path, 'r')
    iterf = iter(file)
    line_no = 0
    data = []
    for line in iterf:
        data = line.split()
        if data[0] == fqdn_sha256:
            line_no += 1
            break
        line_no += 1
    data = ' '.join([data[0], ns_record, time.strftime("%c")])
    print(data)
    command = "sed -i '' '{}s/.*/{}/' ".format(line_no, data) + new_page_path
    os.system(command)
    diff = Diff()
    diff.generate_diffs(version, page_id, page_path)


def copy_page(page_path, page_id, version):
    old_page_path = os.path.join(page_path, page_id)
    new_page_path = os.path.join(page_path, page_id+"_"+version)
    print(page_path)
    command = "cp {} {}".format(old_page_path, new_page_path)
    os.system(command)
