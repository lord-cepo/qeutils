#!/usr/bin/env python
'''
Plotta dopo aver fatto q2r e matdyn. Tutti i file .gp nella cwd finiscono plottati
'''
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib

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


if len(sys.argv) == 1:
    files = [file for file in os.listdir() if file.endswith('.gp')]
else:
    files = sys.argv[1:]

POINT_LABELS = [line.split('!')[1].strip() for line in lines if len(line.split('!')) == 2]
KPATH_POINTS = [line.split()[3].strip() for line in lines[1:]]
for gpfile, color in zip(files, matplotlib.rcParams['axes.prop_cycle']):
    data = np.loadtxt(gpfile)
    X = data[:,0]
    l = gpfile.replace('.gp', '')
    for Y in data.T[1:,:]:
        plt.plot(X,Y, color=color['color'], label=l)
        l = None
__k = (data.shape[0]-KPATH_POINTS.count('0'))//KPATH_POINTS.count('__k')
KPATH_POINTS = [__k if el == '__k' else int(el) for el in KPATH_POINTS]
indices = []
for i in range(len(KPATH_POINTS)):
    indices.append(sum(KPATH_POINTS[:i]))
ticks = [X[i] for i in indices]
for x in ticks:
    plt.axvline(x, linestyle='--', color='grey')
plt.xticks(ticks, POINT_LABELS)

plt.legend()
plt.ylabel('energy [cm-1]')
plt.tight_layout()
plt.savefig('gp.png', dpi=500)