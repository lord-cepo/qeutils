#!/usr/bin/env python
import numpy as np
import sys
with open('pw.out') as f:
    lines = f.readlines()

at = []
for line in lines:
    for i in range(1,4):
        if f"a({i}) =" in line:
            at.append(list(map(float,line.split()[3:6])))

at = np.array(at).T
bg = np.linalg.inv(at).T

v = np.array(list(map(float, [sys.argv[i] for i in range(1,4)])))
print(np.einsum('ij,j->i', np.linalg.inv(bg), v))
