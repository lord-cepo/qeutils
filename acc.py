#!/usr/bin/env python
import matplotlib.pyplot as plt
import os
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()
    grep = []
    for line in lines:
        if "estimated scf accuracy" in line:
            grep.append(float(line.split()[4]))

plt.plot(range(len(grep)), grep)
plt.yscale('log')
plt.tight_layout()
plt.savefig('/gpfsssd/scratch/rech/yhk/unr46rr/acc.png')