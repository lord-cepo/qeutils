#!/usr/bin/env python3
from pwpy import pw2py, py2pw
import sys

nkx =  int(sys.argv[1])
nky =  int(sys.argv[2])
nkz =  int(sys.argv[3])
nbnd = int(sys.argv[4])

nkpts = nkx*nky*nkz
d = pw2py('pw.in')
d['K_POINTS']['type'] = 'crystal'
d['K_POINTS']['rows'] = []
rows = [[nkpts]] + [[i/nkx, j/nky, k/nkz, 1/nkpts] for i in range(nkx) for j in range(nky) for k in range(nkz)]
d['K_POINTS']['rows'] = rows
d['nbnd'] = nbnd
d['calculation'] = 'nscf'

py2pw(d, 'nscf-nosym.pw.in')