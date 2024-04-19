import numpy as np
import matplotlib.pyplot as plt

LOTO_000 = np.array([0, 0, 0, 37.64, 37.64, 52.95, 52.95, 61.32, 93.74, 93.74, 99.55, 100.09, 100.09, 119.2, 132.94])
LOTO_100 = np.array([0, 0, 0, 37.64, 37.64, 52.95, 61.3, 74.1, 93.7, 94.5, 99.6, 100.1, 100.1, 119.2, 132.9])
LOTO_111 = np.array([0, 0, 0, 37.64, 37.64, 52.95, 61.32, 72.59, 93.74, 94.3, 100.09, 100.09, 100.16, 119.29, 132.94])
spacing = 100
prefixes = ["epw-new", "old"]
vlines = ["$\\Gamma$", "Z", "F", "$\\Gamma$", "L"]
colors = ["green", "blue", "blue", "black"]
# vlines = ['$\\Gamma$', 'T', 'H2|H0', 'L', '$\\Gamma$', 'S0|S2', 'F', '$\\Gamma$']
xvlines = [ i*spacing for i in range(len(vlines)) ]
# for i, lab in enumerate(vlines):
#     if "|" in lab
#         for j in range(i, len(vlines)):
#             xvticks[j] += 1
#         xvlines = xvlines[:i] + [xvlines[i]] + xvlines[i:]
#         for j in range(i+1, len(xvlines)):
#             xvlines[j] += 1

for prefix, color in zip(prefixes, colors):
    data = np.loadtxt(prefix + '.gp')
    to_remove = []
    for i in range(data.shape[0]-1):
        if data[i+1, 0] - data[i, 0] > 0.1:
            to_remove.append(i)
    data = np.delete(data, to_remove, axis=0)
    xrange = np.linspace(0, 1, data.shape[0])
    for i in range(1, data.shape[1]):
        plt.plot(xrange, data[:, i], color=color, label=prefix if i == 1 else None)
    # for i in range(15):
    #     plt.plot(xrange[xvlines[3]], LOTO_100[i], 'o', color="black", label='100' if i == 1 else None)
    #     plt.plot(xrange[xvlines[0]], LOTO_111[i], 'o', color="blue", label='111' if i == 1 else None)


# data = np.loadtxt('epw.gp1')
# for i in range(5, 22):
#     plt.plot(data[:,0], data[:, i], '.', color="black")
for xv in xvlines:
    plt.axvline(x=xrange[xv], color="black")

plt.xticks([xrange[xv] for xv in xvlines], vlines)
plt.legend()
plt.tight_layout()
# plt.savefig('bi2te3-soc.png', dpi=500)
plt.show()