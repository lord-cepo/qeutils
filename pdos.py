#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
data = {}
for file in os.listdir():
    if ".pdos_atm#" in file:
        atom = file.split("#")[1].split("(")[1].split(")")[0]
        orbital = file.split("#")[2].split("(")[1].split(")")[0].split("_")[0]
        if atom+orbital not in data:
            data[atom+orbital] = np.loadtxt(file)[:, :2]
        else:
            data[atom+orbital][:, 1] += np.loadtxt(file)[:, 1]
# make moving average of data
for key in data:
    data[key][:, 1] = np.convolve(data[key][:, 1], np.ones(10)/10, mode='same')
# for line in lines:
#     plt.axvline(x=line, color='black', linestyle='--')
for key in data:
    plt.plot(data[key][:, 0], data[key][:, 1], label=key)
    # print(data[key][:, 0][-1])

plt.xlim(-15,15)
plt.ylim(0,0.02)
plt.legend()
# plt.show()
plt.savefig("pdos.png", dpi=500)