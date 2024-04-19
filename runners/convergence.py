import os
import numpy as np
from pwpy import pw2py, py2pw, out_schema
from phpy import py2ph
import bash
import shutil

###########################################
# -----------------------------------------
DEBUG = False
CLEAN = True
USPP = False
SOC = True
STARTING_ECUT = 50.0
# -----------------------------------------
###########################################

d = pw2py('pw.in')

d['lspinorb'] = SOC
d['noncolin'] = SOC

def new_calc(prefix_):
    if CLEAN or not os.path.exists(f'{prefix_}.out') or len(bash.grep('!', f'{prefix_}.out')) != 1:
        print(f"srun on {prefix_}.in")
        py2pw(d, f'{prefix_}.in')
        bash.srun(f'{prefix_}.in')
    return float(out_schema(d['prefix'], 'etot').text)

if not os.path.exists('CONV'):
    os.makedirs('CONV')
if not os.path.exists('CONV/k'):
    os.makedirs('CONV/k')
if not os.path.exists('CONV/e'):
    os.makedirs('CONV/e')

if bash.env.PREFIX is not None:
    d['prefix'] = os.getenv('PREFIX')
else:
    d['prefix'] = os.path.basename(os.getcwd())

d['conv_thr'] = 1e-5
d['ecutwfc'] = STARTING_ECUT
if USPP:
    d['ecutrho'] = d['ecutwfc']*8
old_energy = 1e4
new_energy = 1e5
k = [2,2,2,1,1,1]

while abs(old_energy-new_energy) > 0.5e-3:
    print(f"convergenza a k {k}")
    d['K_POINTS']['rows'] = [k]
    filename = f'conv_{k[0]}'
    old_energy = new_energy
    new_energy = new_calc('CONV/k/'+filename)
    print(f"ENERGY: {2*new_energy}")
    k = [x+1 for x in k[:3]] + k[3:] # TODO: does not work if NKX != NKY or NKY != NKZ


d['K_POINTS']['rows'] = [[x-2 for x in k[:3]] + k[3:]]
ecut = 30
old_energy = 1e4
new_energy = 1e5
while abs(old_energy-new_energy) > 0.5e-3:
    print(f"convergenza a ecutwfc {ecut}")
    d['ecutwfc'] = ecut
    if USPP:
        d['ecutrho'] = ecut*8
    filename = f'conv_{ecut}'
    old_energy = new_energy
    new_energy = new_calc('CONV/e/'+filename)
    print(f"ENERGY: {2*new_energy}")
    ecut += 10
d['ecutwfc'] = ecut-20
if USPP:
    d['ecutrho'] = d['ecutwfc']*8







    