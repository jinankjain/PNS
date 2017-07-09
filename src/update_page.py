import time
from src.combine_diff import *
import queue
import threading
from apscheduler.scheduler import Scheduler

from src.utils import *

SAFE = True
update_queue = queue.Queue()
sched = Scheduler()
DELAY = 0.5


def update_page(page_id, fqdn_sha256, ns_record, page_path):
    # Check for tmp file exists or not
    tmp_path = os.path.join(page_path, page_id+"_tmp")
    orig_path = os.path.join(page_path, page_id)

    # If not then create one
    if not os.path.exists(tmp_path):
        command = "cp {} {}".format(orig_path, tmp_path)
        os.system(command)

    file = open(tmp_path, 'r')
    iterf = iter(file)
    line_no = 0
    data = []
    for line in iterf:
        data = line.split()
        if data[0] == fqdn_sha256:
            line_no += 1
            break
        line_no += 1
    data = ' '.join([data[0], ns_record, str(int(time.time()))])
    print(data)
    command = "sed -i '' '{}s/.*/{}/' ".format(line_no , data) + tmp_path
    os.system(command)


def copy_page(page_path, page_id, version):
    old_page_path = os.path.join(page_path, page_id)
    new_page_path = os.path.join(page_path, page_id+"_"+version)
    print(page_path)
    command = "cp {} {}".format(old_page_path, new_page_path)
    os.system(command)


def process_request():
    global SAFE
    while True:
        if not update_queue.empty() and SAFE:
            item = update_queue.get()
            # print(*item)
            update_page(*item)
            update_queue.task_done()
        elif not SAFE:
            replace_page_with_new_page()
            SAFE = True


@sched.interval_schedule(minutes=DELAY)
def scheduled_update():
    global SAFE
    SAFE = False


# Register APS Scheduler to  update the pages
sched.configure(misfire_grace_time=30)
sched.start()

t = threading.Thread(target=process_request)
t.daemon = True
t.start()