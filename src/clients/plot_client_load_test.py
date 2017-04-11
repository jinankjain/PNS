import matplotlib.pyplot as plt


def plot_graph(x, avg, total):
    fig, ax = plt.subplots()
    ax.plot(x, avg, label="250")
    ax.plot(x, total, label="2500")
    legend = ax.legend(loc='upper center', shadow=True)
    plt.grid(True)
    ax = plt.gca()
    label_x = ax.set_xlabel('Number of clients', fontsize = 15)
    label_y = ax.set_ylabel('Runtime(in seconds)', fontsize = 15)
    plt.show()