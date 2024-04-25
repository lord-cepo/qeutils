from pwpy import pw2py, py2pw
import bash
import os
###########################################
# -----------------------------------------
INPUT_FILE = 'pw.in'
# -----------------------------------------
###########################################

def relax(input_file=INPUT_FILE):
    d = pw2py(input_file)
    
    d['calculation'] = 'relax'
    # d['conv_thr'] = 1e-9
    d['ion_dynamics'] = 'bfgs'
    if 'forc_conv_thr' not in d: 
        d['forc_conv_thr'] = 1e-4
    if 'etot_conv_thr' not in d:
        d['etot_conv_thr'] = 1e-5
    print("RELAX")
    py2pw(d, 'relax.pw.in')
    bash.srun('relax.pw.in')

    bash.run('last_coord.py relax.pw.out') #TODO: import this script directly
    d['ATOMIC_POSITIONS'] = pw2py('relax.pw.in')['ATOMIC_POSITIONS']
    os.remove('relax.pw.in')
    del d['ion_dynamics']
    
    py2pw(d, input_file)

if __name__ == '__main__':
    relax()
    