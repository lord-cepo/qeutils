#!/usr/bin/env python
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import os
import re
from dataclasses import dataclass
import matplotlib.pyplot as plt
# plt.rcParams['figure.facecolor'] = 'none'
# plt.rcParams['axes.facecolor'] = 'none'

T = 300
SIGMA = 10
V0 = 226.1779

CMM1_RY = 9.11264856497897e-06
RY_SECONDS = 4.83776865301e-17
RY_METERS = 5.2917721092e-11
RY_JOULES = 2.17987236110355e-18
KB_RY = 6.333630685659031e-06
HBAR = 1.054571817e-34
RY_WMK = RY_JOULES / RY_SECONDS / RY_METERS

# RY_TO_SI = 851510213.4899045
KB_T = KB_RY*T

# CELL = np.array([
#     [ 2.388574, -1.379044,  0.343519],
#     [ 0.000000,  2.758088,  0.343519],
#     [-2.388574, -1.379044,  0.343519]
# ]) # in 2pi/alat

CELL = np.array([
    [1.000000,  0.577350,  0.000000],
    [0.000000,  1.154701,  0.000000],
    [0.000000,  0.000000,  0.375375],
]) # in 2pi/alat

r = range(-3,4)
Gs = np.array([[x,y,z] for x in r for y in r for z in r])
Gs = Gs @ CELL

# WEIRD_UNITS_TO_W_MK = 0.9922956656872*T
CELL_m1 = np.linalg.inv(CELL)

def cart2cryst(vec):
    return np.dot(vec, CELL_m1)

def cryst2cart(vec):
    return np.dot(vec, CELL)

def refold(vec):
    for G in Gs:
        vec = np.where(
            (np.linalg.norm(vec+G, axis=-1) < np.linalg.norm(vec, axis=-1))[:,np.newaxis], 
            vec+G, 
            vec)
    return vec
  

@dataclass
class Sma:
    q: np.array     # 2pi/alat
    w: np.array     # cm-1
    v: np.array     # Ry
    lw: np.array    # cm-1
    lw_n: np.array
    lw_u: np.array

# os.chdir('/gpfsdswork/projects/rech/yhk/unr46rr/bi2te3/TK/graphite')
files = os.listdir()

def find_file(folder, regex):
    f = [file for file in folder if re.match(regex, file)][0]
    return f

regs = [r"^q\..*$", r"^freq\..*$", r"^vel\..*$", rf"^lw\..*T{T}_s{SIGMA}\.out$", \
    rf"^lw_N.*T{T}_s{SIGMA}\.out$", rf"^lw_U.*T{T}_s{SIGMA}\.out$"]

sma = Sma(*[np.loadtxt(find_file(files, r), dtype=np.float128)[1:,:] for r in regs])

sma.v = sma.v[:, ::3]
sma.q = sma.q[:, :-1]
sma.w *= CMM1_RY
sma.lw *= 2*CMM1_RY
sma.lw_n *= 2*CMM1_RY
sma.lw_u *= 2*CMM1_RY
PREFIX = 1/(V0*T**2*KB_RY*sma.q.shape[0])*RY_WMK

n =  1 / (np.exp(sma.w/KB_T) - 1)
n_np1 = n*(n+1)



# sma.q = cart2cryst(sma.q)
# sma.q = np.where(sma.q <-0.5, sma.q+1, sma.q)
# sma.q = np.where(sma.q > 0.5, sma.q-1, sma.q)  
# sma.q = cryst2cart(sma.q)
sma.q = refold(sma.q)

q_parallel = sma.q[:,0][:, np.newaxis]
k_qs = sma.v**2 * sma.w**2 * n_np1 / sma.lw 
# ha senso prendere il valore assoluto? 
k_qs_num = (n_np1 * sma.w * sma.v * q_parallel / sma.lw * sma.lw_n)
k_qs_den = (n_np1 * q_parallel**2 / sma.lw * sma.lw_n * sma.lw_u) 
k_callaway = k_qs_num.sum(axis=(0,1))**2 / k_qs_den.sum(axis=(0,1)) * PREFIX

k_q = np.sum(k_qs, axis=-1)
k_s = np.sum(k_qs, axis=0)
k = np.sum(k_s) * PREFIX

# sma.q = cart2cryst(sma.q)
# distances = np.linalg.norm(sma.q, axis=-1)
# BIN = np.linspace(0.05,0.85,9)
# k_qs_bin = np.zeros((len(BIN), 15))
# for i,bin in enumerate(BIN):
#     for mode in range(15):
#         k_qs_bin[i, mode] = np.sum(np.where(np.abs(distances - bin) < 0.05, k_qs[:,mode], 0))

# fig, ax = plt.subplots()
# ax.matshow(k_qs_bin, cmap=plt.cm.Blues)
# ax.set_ylabel('dist from $\Gamma$')
# ax.set_yticks(range(len(BIN)), [f"{bin:.2f}" for bin in BIN])
# ax.set_xlabel('mode')
# ax.set_xticks(range(15), range(1,16))
# fig.savefig('colormap.png', dpi=500)
# for s in range(k_qs.shape[1]):
#     plt.plot(sma.w[:,s], k_qs[:,s], '.', label=f"{0 if s+1 < 10 else ''}{s+1}: {k_s[s]:.1e}")

# with open('tk.in') as f:
#     lines = f.readlines()
#     for line in lines:
#         if 'file_mat2' in line:
#             mat2 = line.split('MATDYN/')[1].replace('\'', '').replace('\"', '').strip()
#         if 'file_mat3' in line:
#             mat3 = line.split('FILD3DYN/')[1].replace('\'', '').replace('\"', '').strip()
            
# plt.title(f"{mat2} -- {mat3} -- k {k:.2f}")
# plt.legend()
# plt.tight_layout()
# plt.savefig(f'../s{os.path.basename(os.getcwd())}.png', dpi=500)
# plt.close()

# plt.plot(distances, k_q, '.')
# plt.title(f"{mat2} -- {mat3} -- k {k:.2f}")
# plt.tight_layout()
# plt.savefig(f'../q{os.path.basename(os.getcwd())}.png', dpi=500)


print(f"{k:.3f}")
print(f"Callaway: {k_callaway:.3f}")
