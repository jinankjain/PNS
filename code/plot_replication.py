from __future__ import print_function

import bisect
import matplotlib.pyplot as plt
import numpy as np
import os

from replication import replication

OUTDIR = "."

def get_new_filename(base, ext="", with_time=False):
    if with_time:
        base = str(base) + "_" + time.strftime("%Y%m%d-%H%M%S")
    current_base = base
    counter = 1
    while os.path.exists(current_base + ext):
        current_base = base + "_" + str(counter)
        counter += 1
    return current_base + ext

def generate_loglog_and_save(x, y, filename, generate_pdf=False):
    # Generate log-log plot, and save it
    filename = get_new_filename(os.path.join(OUTDIR, filename), ".eps")
    fig = plt.plot(x, y, lw=2.0)
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlim([1, max(x)])
    ax.set_ylim([0.7, max(y)*2])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    # See http://stackoverflow.com/a/12998531/6950260 for tick_params
    ax.tick_params(which='both', top='off', right='off', labelsize='large')
    #plt.locator_params(axis='x',numticks=4)
    ax.yaxis.grid(True)
    k_star = next(k for i,k in enumerate(x) if y[i] == 1)
    xexp = list(range(0,10, 3))
    xlabels = ['$\mathregular{10^' + str(exp) + '}$' for exp in xexp]
    xticks = [10**exp for exp in xexp] + [k_star]
    xlabels.append('$\mathregular{\quad k^*}$')
    plt.xticks(xticks, xlabels)
    yexp = list(range(0,6))
    ylabels = ['$\mathregular{10^' + str(exp) + '}$' for exp in yexp]
    ylabels[-1] = 'R = $\mathregular{10^5}$'
    yticks = [10**exp for exp in yexp]
    plt.yticks(yticks, ylabels)
    plt.xlabel('Domain rank (log scale)', fontsize='16')
    plt.ylabel('Replication degree (log scale)', fontsize='16')
    plt.tight_layout()
    #plt.show()
    plt.savefig(filename)
    if generate_pdf:
        plt.savefig(os.path.splitext(filename)[0] + ".pdf")
    plt.close()

if __name__ == "__main__":
    R = 10**5
    s = 0.91
    k_vector = np.logspace(0, 9, num=1000)
    r_vector = [replication(k, R, s) for k in k_vector]
    generate_loglog_and_save(k_vector, r_vector, "replication")

