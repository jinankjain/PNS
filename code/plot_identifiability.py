from __future__ import print_function

import collections
import matplotlib.pyplot as plt
import numpy as np
import os

from identifiability import identifiability, zipf_prob

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

def generate_loglog_and_save(x, y_vect, colors, labels, lines, legend_loc, filename,
                             generate_pdf=False):
    # Generate log-log plot, and save it
    if not isinstance(y_vect[0], collections.Iterable):
        y_vect = [y_vect]
    for y, c, lab, lin in zip(y_vect, colors, labels, lines):
        plt.plot(x, y, c, label=lab, ls=lin, lw=2.0)
    ax = plt.gca()
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim([10**(-5), 1])
    #ax.set_xlim([1, max(x)])
    #ax.set_ylim([0.7, max(y)*2])
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    # See http://stackoverflow.com/a/12998531/6950260 for tick_params
    ax.tick_params(which='both', top='off', right='off', labelsize='large')
    plt.locator_params(axis='x',numticks=4)
    ax.yaxis.grid(True)
    plt.xlabel('Domain rank (log scale)', fontsize='16')
    plt.ylabel('Identifiability', fontsize='16')
    plt.legend(loc=legend_loc, numpoints=1)
    #plt.show()
    filename = get_new_filename(os.path.join(OUTDIR, filename), ".eps")
    plt.savefig(filename)
    if generate_pdf:
        plt.savefig(os.path.splitext(filename)[0] + ".pdf")
    plt.close()

if __name__ == "__main__":
    N = 10**9
    m = 10**5
    s = 0.91
    k_vect = np.logspace(0, 9, num=1000)

    zipf = [zipf_prob(k, N, s) for k in k_vect]

    ident_nor = [identifiability(k, 1, 0, m, N, s, 1) for k in k_vect]
    ident_r5 = [identifiability(k, 1, 0, m, N, s, 10**5) for k in k_vect]
    ident_r4 = [identifiability(k, 1, 0, m, N, s, 10**4) for k in k_vect]

    ident_t1 = [identifiability(k, 1, 1, m, N, s) for k in k_vect]
    ident_t2 = [identifiability(k, 1, 2, m, N, s) for k in k_vect]
    ident_t4 = [identifiability(k, 1, 4, m, N, s) for k in k_vect]

    ident_f2 = [identifiability(k, 2, 0, m, N, s) for k in k_vect]
    ident_f3 = [identifiability(k, 3, 0, m, N, s) for k in k_vect]
    ident_f4 = [identifiability(k, 4, 0, m, N, s) for k in k_vect]

    ident_f2_t1 = [identifiability(k, 2, 1, m, N, s) for k in k_vect]
    ident_f2_t2 = [identifiability(k, 2, 2, m, N, s) for k in k_vect]
    ident_f4_t2 = [identifiability(k, 4, 2, m, N, s) for k in k_vect]
    ident_f4_t4 = [identifiability(k, 4, 4, m, N, s) for k in k_vect]

    y_vect = [ident_nor, ident_r5, ident_r4, zipf]
    labels = ['No replication', 'Replication $\mathregular{R=10^5}$ (max)',
            r'Replication $\mathregular{R=10^4}$', 'Zipf (no observation)']
    colors = ['b','r','g','m']
    lines = ['--', '-', '-.', ':']
    # upper right: 1, upper left: 2, lower left: 3, lower right: 4, right: 5,
    # center left: 6, center right: 7, lower center: 8, upper center: 9, center: 10
    legend_loc = 3
    generate_loglog_and_save(k_vect, y_vect, colors, labels, lines, legend_loc, "ident_replication")

    y_vect = [ident_r5, ident_t1, ident_t2, ident_t4]
    labels = ['$\mathregular{t = 0}$', '$\mathregular{t = 1}$', '$\mathregular{t = 2}$',
              '$\mathregular{t = 4}$']
    colors = ['r','b','g','m']
    lines = ['-', '--', '-.', ':']
    # upper right: 1, upper left: 2, lower left: 3, lower right: 4, right: 5,
    # center left: 6, center right: 7, lower center: 8, upper center: 9, center: 10
    legend_loc = 1
    generate_loglog_and_save(k_vect, y_vect, colors, labels, lines, legend_loc, "ident_cover")

    y_vect = [ident_r5, ident_f2, ident_f2_t1, ident_f2_t2, ident_f4, ident_f4_t2, ident_f4_t4]
    labels = ['$\mathregular{q = 1, t = 0}$', '$\mathregular{q = 2, t = 0}$',
              '$\mathregular{q = 2, t = 1}$', '$\mathregular{q = 2, t = 2}$',
              '$\mathregular{q = 4, t = 0}$', '$\mathregular{q = 4, t = 2}$',
              '$\mathregular{q = 4, t = 4}$']
    colors = ['r','b','b','b', 'm', 'm', 'm']
    lines = ['-', '-', '--', '-.', '-', '--', '-.']
    # upper right: 1, upper left: 2, lower left: 3, lower right: 4, right: 5,
    # center left: 6, center right: 7, lower center: 8, upper center: 9, center: 10
    legend_loc = 8
    generate_loglog_and_save(k_vect, y_vect, colors, labels, lines, legend_loc, "ident_fingerp")

