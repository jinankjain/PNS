import matplotlib.pyplot as plt
import statistics
import numpy as np

def plot_graph(x, avg, mid, total, fname):
    fig, ax = plt.subplots()
    ax.plot(x, avg, label="5000")
    ax.plot(x, mid, label="7500")
    ax.plot(x, total, label="10000")
    legend = ax.legend(loc='upper center', shadow=True)
    plt.grid(True)
    ax = plt.gca()
    label_x = ax.set_xlabel('Number of clients', fontsize = 15)
    label_y = ax.set_ylabel('Runtime(in seconds)', fontsize = 15)
    plt.savefig(fname, dpi=250,  bbox_inches='tight')


def plot_breakdown():
    fig, ax = plt.subplots()
    f = open("data.txt", 'r')
    net_lat = [[], [], []]
    ver_time = [[], [], []]
    for line in f:
        line = line.split(" ")
        page_id = int(line[1])
        net_lat_t = float(line[3])
        ver_lat_t = float(line[5])
        net_lat[page_id].append(net_lat_t)
        ver_time[page_id].append(ver_lat_t)

    N = 2
    # print(N)
    net_means = []
    net_std = []
    for i in range(0, N):
        net_means.append(statistics.mean(net_lat[i]))
        net_std.append(statistics.stdev(net_lat[i]))

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, net_means, width, color='r', yerr=net_std)

    ver_means = []
    ver_std = []
    for i in range(0, N):
        ver_means.append(statistics.mean(ver_time[i]))
        ver_std.append(statistics.stdev(ver_time[i]))
    rects2 = ax.bar(ind + width, ver_means, width, color='y', yerr=ver_std)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Time (in seconds)')
    ax.set_title('Time Breakdown')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('5000', '10000', '7500'))

    ax.legend((rects1[0], rects2[0]), ('Network Latency', 'Verification Time'))

    def autolabel( rects ):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.savefig("breakdown_new.pdf", dpi=250, bbox_inches='tight')

# plot_breakdown()