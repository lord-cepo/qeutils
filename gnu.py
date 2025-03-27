#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
plt.rcParams['figure.facecolor'] = 'none'
plt.rcParams['axes.facecolor'] = 'none'
import os
os.chdir('/gpfsdswork/projects/rech/yhk/unr46rr/bi2te3/PP/PW')
# filenames
PREFIXES = ["sd", "d"]
COLORS = ['seagreen', 'mediumvioletred', 'b', 'c', 'm', 'y']
# SHIFTS = [8-17.3+0.15, 8-17.3, -9.3, -9.3+0.019, -8.116-0.370, -8.9+0.054]
SHIFTS = [-9-0.3,-10+0.8]
xvlines = [0, 30, 60, 90, 120]
VALCOND = [[-15,-13], [-6,-5]]
labels = ['$\\Gamma$', 'Z', 'F', '$\\Gamma$', 'L']

plt.subplots(figsize=(3, 7))
for prefix, color, shift, valcond in zip(PREFIXES, COLORS, SHIFTS, VALCOND):
    print_prefix = "SOC" if prefix=='sd' else "w/o"
    filename = prefix + '.gnu'
    data = np.loadtxt(filename)
    # plt.plot(data[:,0], data[:,1]+shift, color=color, label=print_prefix)
    for i in range(1, data.shape[0]):
        if data[i,0]-data[i-1,0] < 0:
            NPOINTS = i
            break
    data = data.reshape(-1, NPOINTS, 2)
    val = make_interp_spline(data[valcond[0],:,0], data[valcond[0],:,1])
    cond = make_interp_spline(data[valcond[1],:,0], data[valcond[1],:, 1])
    x = np.linspace(data[0,0,0], data[0,NPOINTS-1,0], 1000)
    for i in valcond:
        plt.plot(x, val(x)+shift, color=color, label=print_prefix)
        plt.plot(x, cond(x)+shift, color=color)
        print_prefix = None
data_GW = np.loadtxt('GW.gnu')
val = make_interp_spline(data_GW[:117, 0], data_GW[:117, 1]+0.086)
cond = make_interp_spline(data_GW[117:, 0], data_GW[117:, 1]+0.086)
x = np.linspace(0, 4.701, 1000)
plt.plot(x, val(x), label='GW', color='orange')
plt.plot(x, cond(x), color='orange')

# data_exp = np.loadtxt('bi2te3-lda-nc-sr-exp.bands.gnu')
# for xv in xvlines:
plt.axvline(x=3.32, linestyle='--', color="grey")
plt.ylabel('energy (eV)')
plt.xticks([3.32],['$\\Gamma$'])
plt.xlim(2.8,3.8)
plt.ylim(-0.8, 1.6)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('gnu.png', dpi=500)
# plt.show()
