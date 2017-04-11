import threading
import timeit
from src.clients.client import *
from src.clients.plot_client_load_test import *


class WrapperThread(threading.Thread):
    def __init__(self, thread_id, name, counter, func):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter # Number of time you want to repeat a same test case
        self.function = func

    def run(self):
        if self.function == 0:
            run_test_page_size_2500(self.counter, self.name)
        elif self.function == 1:
            run_test_page_size_250(self.counter, self.name)


def run_test_page_size_2500(counter, thread_id):
    for i in range(0, counter):
        get_page_without_version("0", thread_id)


def run_test_page_size_250(counter, thread_id):
    for i in range(0, counter):
        get_page_without_version("1", thread_id)


def main():
    total_time_2500 = []
    avg_res_time_2500 = []
    total_time_250 = []
    avg_res_time_250 = []
    x = range(100, 500, 50)
    for i in x:
        thread = []
        start_time = timeit.default_timer()
        for j in range(0, i):
            thread.append(WrapperThread(j, "Thread-"+str(j), 1, 0))
            thread[j].start()
        for j in range(0, i):
            thread[j].join()
        avg_res_time_2500.append((timeit.default_timer() - start_time) / i)
        total_time_2500.append((timeit.default_timer() - start_time))
    for i in x:
        thread = []
        start_time = timeit.default_timer()
        for j in range(0, i):
            thread.append(WrapperThread(j, "Thread-"+str(j), 1, 1))
            thread[j].start()
        for j in range(0, i):
            thread[j].join()
        avg_res_time_250.append((timeit.default_timer() - start_time) / i)
        total_time_250.append((timeit.default_timer() - start_time))
    plot_graph(x, total_time_250, total_time_2500)
    plot_graph(x, avg_res_time_250, avg_res_time_2500)

if __name__ == "__main__":
    main()