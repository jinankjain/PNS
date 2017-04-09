import threading
import timeit
from src.clients.client import *


class WrapperThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter # Number of time you want to repeat a same test case

    def run(self):
        run_test(self.counter, self.name)


def run_test(counter, thread_id):
    for i in range(0, counter):
        get_page_without_version("0", thread_id)


def main():
    total_time = []
    avg_res_time = []
    for i in range(100, 500, 50):
        thread = []
        start_time = timeit.default_timer()
        for j in range(0, i):
            thread.append(WrapperThread(j, "Thread-"+str(j), 1))
            thread[j].start()
        for j in range(0, i):
            thread[j].join()
        avg_res_time.append((timeit.default_timer() - start_time) / i)
        total_time.append((timeit.default_timer() - start_time))
    print(total_time)
    print(avg_res_time)

if __name__ == "__main__":
    main()