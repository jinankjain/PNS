import threading
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
            run_test_page_size_5000(self.counter, self.name)
        elif self.function == 1:
            run_test_page_size_7500(self.counter, self.name)
        elif self.function == 2:
            run_test_page_size_10000(self.counter, self.name)


def run_test_page_size_10000(counter, thread_id):
    for i in range(0, counter):
        get_page_without_version("1", thread_id)


def run_test_page_size_7500(counter, thread_id):
    for i in range(0, counter):
        get_page_without_version("2", thread_id)


def run_test_page_size_5000(counter, thread_id):
    for i in range(0, counter):
        get_page_without_version("0", thread_id)


def main():
    total_time_5000 = []
    avg_res_time_5000 = []
    total_time_7500 = []
    avg_res_time_7500 = []
    total_time_10000 = []
    avg_res_time_10000 = []
    x = range(50, 150, 20)
    for i in x:
        thread = []
        start_time = timeit.default_timer()
        for j in range(0, i):
            thread.append(WrapperThread(j, "Thread-"+str(j), 1, 0))
            thread[j].start()
        for j in range(0, i):
            thread[j].join()
        avg_res_time_5000.append((timeit.default_timer() - start_time) / i)
        total_time_5000.append((timeit.default_timer() - start_time))
    for i in x:
        thread = []
        start_time = timeit.default_timer()
        for j in range(0, i):
            thread.append(WrapperThread(j, "Thread-"+str(j), 1, 1))
            thread[j].start()
        for j in range(0, i):
            thread[j].join()
        avg_res_time_7500.append((timeit.default_timer() - start_time) / i)
        total_time_7500.append((timeit.default_timer() - start_time))
    for i in x:
        thread = []
        start_time = timeit.default_timer()
        for j in range(0, i):
            thread.append(WrapperThread(j, "Thread-"+str(j), 1, 2))
            thread[j].start()
        for j in range(0, i):
            thread[j].join()
        avg_res_time_10000.append((timeit.default_timer() - start_time) / i)
        total_time_10000.append((timeit.default_timer() - start_time))
    # print(avg_res_time_10000)
    plot_graph(x, total_time_5000, total_time_7500, total_time_10000, "total_time.pdf")
    plot_graph(x, avg_res_time_5000, avg_res_time_7500, avg_res_time_10000, "avg_time.pdf")

if __name__ == "__main__":
    main()