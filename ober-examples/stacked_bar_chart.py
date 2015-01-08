#!/usr/bin/env python
#-----------------------------------------------------------------------------------------
# From http://matplotlib.org/examples/pylab_examples/bar_stacked.html
# Forseeing a stacked bar plot of variant frequencies for the imputation paper
#-----------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

colors = ['b', 'g', 'r', 'c', 'm', 'y']  # Colors of stacked groups

num_variants = np.loadtxt('stacked_bar_chart.dat', dtype=int)
N = num_variants.shape[1]
ind = np.arange(N)  # the x locations for the groups
width = 0.5  # the width of the bars: can also be len(x) sequence

p = [plt.bar(ind, num_variants[group, :], width,
             color=colors[group], bottom=sum(num_variants[:group, :])) 
             for group in xrange(num_variants.shape[0])]

plt.xlabel('Minor Allele Frequency', fontsize=18)
plt.ylabel('# Variants', fontsize=18)
plt.xticks(ind + width / 2., ['%.1f-%.1f' % (x - 0.25 / N, x + 0.25 / N) for x in (np.arange(N) + 0.5) / (2 * N)], fontsize=18)
plt.yticks(np.arange(0, 81, 10), fontsize=18)
plt.legend(tuple(x[0] for x in p), ('Non-coding', 'Non-synonymous', 'Missense'))
# plt.xlim([-0.05, 0.55])

plt.show()
