#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# os.chdir('/linkhome/rech/genimp01/unr46rr/work/bi2te3/thirdorder')

kpath = 'KPATH'
pre_kpath = './'
max_depth = 5
counter = 0
while kpath not in os.listdir(pre_kpath):
    pre_kpath += '../'
    counter += 1
    if counter == 5:
        raise("I did not find KPATH")
    
kpath = pre_kpath + kpath
with open(kpath) as f:
    lines = f.readlines()

POINT_LABELS = [line.split('!')[1].strip() for line in lines if len(line.split('!')) == 2]
for gpfile, color in zip([file for file in os.listdir() if file.endswith('.gp')], matplotlib.rcParams['axes.prop_cycle']):
    data = np.loadtxt(gpfile)
    X = data[:,0]
    l = gpfile.replace('.gp', '')
    for Y in data.T[1:,:]:
        plt.plot(X,Y, color=color['color'], label=l)
        l = None

ticks = [X[i] for i in range(0,data.shape[0], data.shape[0]//(len(POINT_LABELS)-1))]
for x in ticks:
    plt.axvline(x, linestyle='--', color='grey')
plt.xticks(ticks, POINT_LABELS)

plt.legend()
plt.ylabel('energy [cm-1]')
plt.tight_layout()
plt.savefig('gp.png', dpi=500)