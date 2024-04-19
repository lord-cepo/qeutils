import os
import numpy as np
from pwpy import pw2py, py2pw, out_schema
from phpy import py2ph
import bash
import shutil

DEBUG = False
CLEAN = True
USPP = False
SOC = True
# NTASKS = os.getenv('SLURM_NTASKS')
# ESPRESSO_BIN = os.getenv('ESPRESSO_BIN')
# SCRATCH = os.getenv('SCRATCH')
# if not os.path.exists('pw.in'):
#     shutil.copy('../pw.in', '.')
d = pw2py('../pw.in')
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

d['prefix'] = os.path.basename(os.getcwd())
d['conv_thr'] = 1e-5
d['ecutwfc'] = 50 ##################################################################################
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
    k = [x+1 for x in k[:3]] + k[3:] ###############################################################


d['K_POINTS']['rows'] = [[x-2 for x in k[:3]] + k[3:]]
ecut = 20
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

d['calculation'] = 'relax'
d['conv_thr'] = 1e-9
d['ion_dynamics'] = 'bfgs'
print("RELAX")
py2pw(d, 'relax.pw.in')
bash.srun('relax.pw.in')

bash.run('last_coord.py relax.pw.out')
d = pw2py('relax.pw.in')
d['calculation'] = 'scf'
d['conv_thr'] = 1e-12
# py2pw(d, 'pw.in')
# bash.srun('pw.in')
# scf_seconds = round(float(out_schema(old_prefix, 'total').find('./wall').text))

# num_iter = bash.grep("convergence has been achieved in", 'pw.out')[0].split()[5]

print("Benchmark delle forze: ")
f = pw2py('../force.pw.in')
d['ATOMIC_POSITIONS']['rows'] = f['ATOMIC_POSITIONS']['rows']
d['tprnfor'] = True
d['tstress'] = True
py2pw(d, 'force.pw.in')
bash.srun('force.pw.in')


# dph = {
#     'prefix': old_prefix,
#     'fildyn': f'MATDYN/{old_prefix}.dyn',
#     'tr2_ph': 1e-17,
#     'ldisp': True,
#     'nq1': 1,
#     'nq2': 1,
#     'nq3': 1,
#     'nmix_ph': 20,
# }

# py2ph(dph, 'gamma.ph.in')
# if not os.path.exists('MATDYN'):
#     os.makedirs('MATDYN')
# bash.srun('gamma.ph.in', exe='ph')
# ph_time = bash.grep("PHONON       :", "gamma.ph.out")[-1].split()[2]

# with open('../results.txt', 'a') as f:
#     scf_time = str(scf_seconds//60)+'m'+str(scf_seconds%60)+'s'
#     freq_text = bash.grepA('**************************************************************************', 'gamma.ph.out', 15)
#     freqs = [float(s.split()[7]) for s in freq_text]
#     EXPERIMENTAL = np.array([34., 34., 50., 50., 62., 94., 94., 95., 102., 102., 120., 134.])
#     norm = np.linalg.norm(EXPERIMENTAL - np.array(freqs[3:]))
#     line = [scf_time, num_iter, ph_time, str(norm)[:5]]
#     f.write(" ".join(line)+'\n')






    