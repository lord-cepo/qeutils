#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from pwpy import pw2py, out_schema
# from scipy.interpolate import make_interp_spline
from re import sub
import os

fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1]) 
HARTREE_EV = 27.2114
PREFIX = pw2py("../pw.in")['prefix']
HOMO = float(out_schema(PREFIX, "highestOccupiedLevel").text)*HARTREE_EV
LUMO = float(out_schema(PREFIX, "lowestUnoccupiedLevel").text)*HARTREE_EV
W90_PREFIX = [file.split('.')[0] for file in os.listdir() if file.endswith('.win')][0]
FILENAME_W90 = W90_PREFIX+"_band.dat"
FILENAME_DFT = "dft.gnu"

with open(W90_PREFIX+"_band.gnu") as f:
    lines = f.readlines()
    XVLINES = []
    XVLABELS = []
    for line in lines:
        if line.startswith("set xtics"):
            points = line.split("\"")[1:]
            for index,point in enumerate(points):
                if index%2:
                    XVLINES.append(float(sub('[^0-9.]', '', point)))
                else:
                    XVLABELS.append(point)
            break

with open(W90_PREFIX+"_band.kpt") as f:
    lines = f.readlines()
    NPOINTS = int(lines[0].strip())
    
with open(W90_PREFIX+".win") as f:
    lines = f.readlines()
    for line in lines:
        if line.strip().startswith("exclude_bands"):
            start_band = int(line.split("=")[1].strip().split("-")[1])


# f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
ax1 = plt.subplot(gs[0])
data_W90 = np.loadtxt(FILENAME_W90)
data_W90 = np.reshape(data_W90, (-1, NPOINTS, 2))
label = "W90"
truex = data_W90[0,:NPOINTS,0]
for i in range(data_W90.shape[0]):
    ax1.plot(truex, data_W90[i, :, 1], color="red", label=label)
    label = None

valence = 0
norm_valence = 1e10
conduction = 0
norm_conduction = 1e10
data_DFT = np.loadtxt(FILENAME_DFT)
data_DFT = np.reshape(data_DFT, (-1, NPOINTS, 2))
label = "DFT"
for i in range(start_band, data_DFT.shape[0]):
    ax1.plot(truex, data_DFT[i, :, 1], color="blue", label=label)
    energies_fermi = data_DFT[i,:,1]-(HOMO+LUMO)/2
    new_norm = np.linalg.norm(energies_fermi)
    if new_norm < norm_valence and np.all(energies_fermi < 0):
        valence = i
        norm_valence = new_norm
    if new_norm < norm_conduction and np.all(energies_fermi > 0):
        conduction = i
        norm_conduction = new_norm
    label = None

print(valence, conduction)
ax2 = plt.subplot(gs[1], sharex = ax1)
ax2.plot(truex, (data_DFT[valence,:,1]-data_W90[valence-start_band,:,1])*1000, label="valence")
ax2.plot(truex, (data_DFT[conduction,:,1]-data_W90[conduction-start_band,:,1])*1000, label="conduction")


# data_GW = np.loadtxt('GW.bands.gnu')
# val = make_interp_spline(data_GW[:117, 0], data_GW[:117, 1]+0.086)
# cond = make_interp_spline(data_GW[117:, 0], data_GW[117:, 1]+0.086)
# x = np.linspace(0, 4.701, 1000)
# plt.plot(x, val(x), label='GW', color='orange')
# plt.plot(x, cond(x), color='orange')


for xv in XVLINES:
    ax2.axvline(x=xv, color="grey", linestyle="--")
    ax1.axvline(x=xv, color="grey", linestyle="--")
    
    
# ax1.set_xticks(XVLINES, XVLABELS)
plt.setp(ax1.get_xticklabels(), visible=False)
# yticks = ax2.yaxis.get_major_ticks()
# yticks[-1].label2.set_visible(False)
ax2.set_xticks(XVLINES, XVLABELS)

ax2.set_ylabel("diff (meV)")
ax1.legend(loc='upper left')
ax2.legend()
plt.tight_layout()
plt.subplots_adjust(hspace=.0)
plt.savefig('wannier_dft_bands.png', dpi=500)


