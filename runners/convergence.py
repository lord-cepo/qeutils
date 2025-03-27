import os
from pwpy import pw2py, py2pw, out_schema
import bash
# from phpy import py2ph
# import numpy as np
# import shutil

###########################################
# -----------------------------------------
DEBUG = False
CLEAN = False
USPP = False
SOC = True
STARTING_ECUT = 40.0
# -----------------------------------------
###########################################

def convergence(debug=DEBUG, clean=CLEAN, uspp=USPP, soc=SOC, starting_ecut=STARTING_ECUT):
    d = pw2py('pw.in')

    d['lspinorb'] = soc
    d['noncolin'] = soc

    def new_calc(prefix_):
        if clean or not os.path.exists(f'{prefix_}.out') or len(bash.grep('!', f'{prefix_}.out')) != 1:
            print(f"srun on {prefix_}.in")
            py2pw(d, f'{prefix_}.in')
            bash.srun(f'{prefix_}.in')
        
        return float(bash.grep('!', f'{prefix_}.out')[0].split()[4])


    if not os.path.exists('CONV'):
        os.makedirs('CONV')
    if not os.path.exists('CONV/k'):
        os.makedirs('CONV/k')
    if not os.path.exists('CONV/e'):
        os.makedirs('CONV/e')

    if os.getenv('PREFIX') != os.path.basename(os.getcwd()):
        print(f"WARNING: prefix = {os.getenv('PREFIX')} is different than parent folder {os.path.basename(os.getcwd())}")
    if d['prefix'] is None:
        d['prefix'] = os.getenv('PREFIX')
    previous_prefix = d['prefix']

    previous_conv_thr = d['conv_thr']
    d['conv_thr'] = 1e-5
    d['ecutwfc'] = starting_ecut
    if uspp:
        d['ecutrho'] = d['ecutwfc']*8
    old_energy = 1e4
    new_energy = 1e5
    k = [2,2,2,1,1,1]
    print('\n-----------------------------------------------------\n')
    while abs(old_energy-new_energy) > 1e-3:
        print(f"convergenza a k {k}")
        d['K_POINTS']['rows'] = [k]
        filename = f'conv_{k[0]}'
        d['prefix'] = filename
        old_energy = new_energy
        new_energy = new_calc('CONV/k/'+filename)
        print(f"ENERGY: {new_energy}")
        k = [x+1 for x in k[:3]] + k[3:] # TODO: does not work if NKX != NKY or NKY != NKZ


    d['K_POINTS']['rows'] = [[x-2 for x in k[:3]] + k[3:]]
    
    # ----------------------------------------------------------------------------------------------
    ecut = 20
    step = 10
    # ----------------------------------------------------------------------------------------------
    old_energy = 1e4
    new_energy = 1e5
    print('\n-----------------------------------------------------\n')
    while abs(old_energy-new_energy) > 1e-3:
        print(f"convergenza a ecutwfc {ecut}")
        d['ecutwfc'] = ecut
        if uspp:
            d['ecutrho'] = ecut*8
        filename = f'conv_{ecut}'
        d['prefix'] = filename
        old_energy = new_energy
        new_energy = new_calc('CONV/e/'+filename)
        print(f"ENERGY: {2*new_energy}")
        ecut += step
    d['ecutwfc'] = ecut-2*step
    if uspp:
        d['ecutrho'] = d['ecutwfc']*8

    d['prefix'] = previous_prefix
    d['conv_thr'] = previous_conv_thr
    py2pw(d, 'pw.in')
    print('\n-----------------------------------------------------\n')
    

if __name__ == '__main__':
    convergence()





    
