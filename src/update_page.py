import os
import time

def update_page(page_id, fqdn_sha256, ns_record, page_path):
    page_path = os.path.join(page_path, page_id)
    file = open(page_path, 'r')
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
    command = "sed -i '' '{}s/.*/{}/' ".format(line_no, data) + page_path
    os.system(command)