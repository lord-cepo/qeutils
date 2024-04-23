from shutil import copytree
import os
from pwpy import pw2py, py2pw
from runners.relax import relax
import bash

###########################################
# -----------------------------------------
EXEC_PATH = "/linkhome/rech/genimp01/unr46rr/common/thirdorder/thirdorder_espresso.py"
GRID = [2,2,2]
MAX_NEIGHBOUR = 3
INPUT_FILE = 'pw.in'
TEMPLATE_FILE = 'template.in'
RESTART = False
# -----------------------------------------
###########################################

def thirdorder_init(exec_path=EXEC_PATH, grid=GRID, max_neighbour=MAX_NEIGHBOUR, input_file=INPUT_FILE, template_file=TEMPLATE_FILE):
    command = f'{exec_path} {input_file} sow {" ".join(map(str,grid))} -{max_neighbour} {template_file}'

    d = pw2py('pw.in')
    d['tprnfor'] = True
    d['tstress'] = True
    d['outdir'] = f"{os.getenv('SCRATCH')}/{d['prefix']}/##NUMBER##"
    d['nat'] = '##NATOMS##'
    d['ibrav'] = 0
    d['startingwfc'] = 'file'
    d['startingpot'] = 'file'
    if d['K_POINTS']['type'].lower() == 'automatic':
        new_kpts = [round(int(x)/y) for x, y in zip(d['K_POINTS']['rows'][0][:3],GRID)]
        new_kpts = [x if x != 0 else 1 for x in new_kpts]
        if new_kpts == [1,1,1] and ('noncolin' not in d or d['noncolin'] == False):
            d['K_POINTS']['type'] = 'gamma'
            d['K_POINTS']['rows'] = []
        else:
            d['K_POINTS']['rows'] = [new_kpts+d['K_POINTS']['rows'][0][3:]]

    py2pw(d, template_file, ignore_tags=['nat'])
    with open(template_file, 'a') as f:
        f.writelines(['\n', '##CELL##\n', '\n', '##COORDINATES##\n', '\n'])

    os.system(command)

if __name__ == '__main__':
    thirdorder_init()
    d = pw2py('BASE.template.in')
    del d['startingwfc']
    del d['startingpot']
    py2pw(d, 'BASE.template.in')
    relax(input_file='BASE.template.in')
    disp_files = [f for f in os.listdir() if f.startswith('DISP.template.in.')]
    # bash.env.NTASKS //= len(disp_files)
    # if bash.env.NTASKS == 0:
    #     raise ValueError(f'More PW input files ({len(disp_files)}) than processors')
    for file in disp_files:
        copytree(f"{os.getenv('SCRATCH')}/{d['prefix']}/0", 
                 f"{os.getenv('SCRATCH')}/{d['prefix']}/{int(file.split('.')[-1])}")
        # bash.srun(file, _output='DISP.template.out.'+file.split('.')[-1])
