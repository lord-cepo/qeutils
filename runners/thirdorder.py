"""
Il senso era utilizzare la charge-density e le wfc per avere una speedup nella convergenza,
calcolandole in BASE.{TEMPLATEFILE}.
Problema 1): in alcuni casi forse ti sposti troppo (???) e le wfc non sono più utilizzabili
Problema 2): a quel punto non sono sicuro che usare solo la charge-density possa migliorare molto,
visto che all'iterazione dopo usando atomic wfcs ritorniamo ad una etot_conv_thr altina

Quindi alla fine questo script non fa nulla di che, se non chiamare thirdorder_espresso.py e 
mandare i PW in parallelo, costruendo NWORKERS. 

Bug: nell'ultima run avevo 12 nodi (480 MPI tasks), ma solo 10 stavano realmente runnando in 
sincrono. Ho modificato lo srun command, bisogna riprovare
"""
# from shutil import copytree
import os
from time import sleep
from pwpy import pw2py, py2pw
# from runners.relax import relax
# import subprocess
import bash

###########################################
# -----------------------------------------
EXEC_PATH = "/linkhome/rech/genimp01/unr46rr/common/thirdorder/thirdorder_espresso.py"
GRID = [2,2,2]
MAX_NEIGHBOUR = 3
INPUT_FILE = 'pw.in'
TEMPLATE_FILE = 'template.in'
RESTART = False
NWORKERS = os.getenv('SLURM_NNODES')*2
# -----------------------------------------
###########################################

STRUCTURE_PARAMETERS = [f'celldm({i})' for i in range(1,7)] + ['cosAB', 'cosBC', 'cosAC', 'A', 'B', 'C']

def thirdorder_init(exec_path=EXEC_PATH, 
                    grid=GRID, 
                    max_neighbour=MAX_NEIGHBOUR, 
                    input_file=INPUT_FILE, 
                    template_file=TEMPLATE_FILE):
    command = f'{exec_path} {input_file} sow {" ".join(map(str,grid))} -{max_neighbour} {template_file}'

    d = pw2py('pw.in')
    d['tprnfor'] = True
    d['tstress'] = True
    d['outdir'] = f"{os.getenv('SCRATCH')}/{d['prefix']}/##NUMBER##"
    d['nat'] = '##NATOMS##'
    d['ibrav'] = 0
    # d['startingwfc'] = 'file'
    # d['startingpot'] = 'file'
    for key in STRUCTURE_PARAMETERS:
        if key in d:
            del d[key]
    del d['ATOMIC_POSITIONS']
    if d['K_POINTS']['type'].lower() == 'automatic':
        new_kpts = [round(int(x)/y) for x, y in zip(d['K_POINTS']['rows'][0][:3],GRID)]
        new_kpts = [x if x != 0 else 1 for x in new_kpts]
        if new_kpts == [1,1,1] and ('noncolin' not in d or d['noncolin'] == False):
            d['K_POINTS']['type'] = 'gamma'
            d['K_POINTS']['rows'] = []
        else:
            d['K_POINTS']['rows'] = [new_kpts+d['K_POINTS']['rows'][0][3:]]
    else:
        raise NotImplementedError("K_POINTS other than automatic not implemented")
    py2pw(d, template_file, ignore_tags=['nat'])
    with open(template_file, 'a') as f:
        f.writelines(['\n', '##CELL##\n', '\n', '##COORDINATES##\n', '\n'])

    os.system(command)

if __name__ == '__main__':
    thirdorder_init()
    # print("thirdorder files created")
    
    # # SCF calculation of BASE to find a similar charge density to start with (why not relaxing?)
    # d = pw2py(f'BASE.{TEMPLATEFILE}')
    # # del d['startingwfc']
    # # del d['startingpot']
    # py2pw(d, f'BASE.{TEMPLATEFILE}')
    # # relax(input_file=f'BASE.{TEMPLATEFILE}')
    # bash.srun(f'BASE.{TEMPLATEFILE}')
    
    # copy charge density to all the other folders
    todo_disps = [ f.split('.')[-1] for f in os.listdir() if f.startswith(f'DISP.{TEMPLATE_FILE}.')]
    todo_disps = [disp for disp in todo_disps if not bash.pw_completed(f'DISP.{TEMPLATE_FILE}.{disp}', warn=False)]
    # for disp in todo_disps:
    #     copytree(f"{os.getenv('SCRATCH')}/{d['prefix']}/0", 
    #              f"{os.getenv('SCRATCH')}/{d['prefix']}/{disp}", dirs_exist_ok=True)
    # print("Charge densities have been copied")
    
    tasks_per_worker = int(os.getenv('SLURM_NTASKS'))//NWORKERS
    working_disps = []
    
    # wait for all the jobs to be finished
    while len(todo_disps) > 0 or len(working_disps) > 0:
        if len(working_disps) != NWORKERS and len(todo_disps) > 0:
            disp = todo_disps.pop(0)
            working_disps.append(disp)
            os.system(f"srun -n {tasks_per_worker} --exclusive --mpi=pmi2 $ESPRESSO_BIN/pw.x -in DISP.{TEMPLATE_FILE}.{disp} > DISP.{TEMPLATE_FILE}.{disp}.out &")
        temp = []
        for wdisp in working_disps:
            if not bash.pw_completed(f'DISP.{TEMPLATE_FILE}.{wdisp}', warn=False):
                temp.append(wdisp)
        working_disps = temp
        sleep(3)
    