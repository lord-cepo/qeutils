import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
# filenames
PREFIXES = ["bi2te3-pbe-nc-sr-exp", "valence"]
COLORS = ['r', 'g', 'b', 'c', 'm', 'y']
# SHIFTS = [8-17.3+0.15, 8-17.3, -9.3, -9.3+0.019, -8.116-0.370, -8.9+0.054]
SHIFTS = [0, 1.34]
xvlines = [0, 30, 60, 90, 120]
labels = ['$\\Gamma$', 'Z', 'F', '$\\Gamma$', 'L']
NPOINTS = 121


for prefix, color, shift in zip(PREFIXES, COLORS, SHIFTS):
    print_prefix = prefix
    filename = prefix + '.bands.gnu'
    data = np.loadtxt(filename)
    data = data.reshape(-1, NPOINTS, 2)
    # val = make_interp_spline(data[-NPOINTS*6:-NPOINTS*5, 0], data[-NPOINTS*6:-NPOINTS*5, 1])
    # cond = make_interp_spline(data[-NPOINTS*5:-NPOINTS*4, 0], data[-NPOINTS*5:-NPOINTS*4, 1])
    # x = np.linspace(data[-NPOINTS*6,0], data[-NPOINTS*5-1,0], 1000)
    for i in range(data.shape[0]):
        plt.plot(data[i, :, 0], data[i, :, 1]+shift, color=color, label=print_prefix)
        print_prefix = None
# data_GW = np.loadtxt('GW.bands.gnu')
# val = make_interp_spline(data_GW[:117, 0], data_GW[:117, 1]+0.086)
# cond = make_interp_spline(data_GW[117:, 0], data_GW[117:, 1]+0.086)
# x = np.linspace(0, 4.701, 1000)
# plt.plot(x, val(x), label='GW', color='orange')
# plt.plot(x, cond(x), color='orange')

data_exp = np.loadtxt('bi2te3-lda-nc-sr-exp.bands.gnu')
for xv in xvlines:
    plt.axvline(x=data_exp[xv,0], color="black")
plt.xticks([data_exp[xv,0] for xv in xvlines], labels)
plt.legend(loc='upper left')
plt.tight_layout()
# plt.savefig('sr-bands.png', dpi=500)
plt.show()
