from pwpy import pw2py, py2pw
import bash


d = pw2py('pw.in')

d['calculation'] = 'relax'
d['conv_thr'] = 1e-9
d['ion_dynamics'] = 'bfgs'
print("RELAX")
py2pw(d, 'relax.pw.in')
bash.srun('relax.pw.in')

bash.run('last_coord.py relax.pw.out')
del d['ion_dynamics']
py2pw(d, 'pw.in')