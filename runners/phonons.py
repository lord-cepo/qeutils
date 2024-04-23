from pwpy import pw2py, py2pw
from phpy import py2ph
import os
import bash
import sys

###########################################
# -----------------------------------------
NKX = 1
NKY = 1
NKZ = 1
SCF = True
# -----------------------------------------
###########################################
def phonons(nkx=NKX, nky=NKY, nkz=NKZ, scf=SCF):
    d = pw2py('pw.in')
    if scf:
        d['calculation'] = 'scf'
        d['conv_thr'] = 1e-12
        py2pw(d, 'pw.in')
        bash.srun('pw.in')

    # scf_seconds = round(float(out_schema(old_prefix, 'total').find('./wall').text))
    # num_iter = bash.grep("convergence has been achieved in", 'pw.out')[0].split()[5]

    dph = {
        'prefix': d['prefix'],
        'fildyn': f"MATDYN/{d['prefix']}.dyn",
        'tr2_ph': 1e-17,
        'ldisp': True,
        'nq1': nkx,
        'nq2': nky,
        'nq3': nkz,
        'nmix_ph': 20,
    }

    if nkx == nky == nkz == 1:
        ph_prefix = 'gamma'
    else:
        ph_prefix = 'grid'
    py2ph(dph, ph_prefix+'.ph.in')
    if not os.path.exists('MATDYN'):
        os.makedirs('MATDYN')
    bash.srun('gamma.ph.in', exe='ph')
# ph_time = bash.grep("PHONON       :", "gamma.ph.out")[-1].split()[2]

# with open('../results.txt', 'a') as f:
#     scf_time = str(scf_seconds//60)+'m'+str(scf_seconds%60)+'s'
#     freq_text = bash.grepA('**************************************************************************', 'gamma.ph.out', 15)
#     freqs = [float(s.split()[7]) for s in freq_text]
#     EXPERIMENTAL = np.array([34., 34., 50., 50., 62., 94., 94., 95., 102., 102., 120., 134.])
#     norm = np.linalg.norm(EXPERIMENTAL - np.array(freqs[3:]))
#     line = [scf_time, num_iter, ph_time, str(norm)[:5]]
#     f.write(" ".join(line)+'\n')

if __name__ == '__main__':
    phonons()