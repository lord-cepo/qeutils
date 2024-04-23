import os
import subprocess
from types import SimpleNamespace

env = SimpleNamespace( **{
    'NTASKS': os.getenv('SLURM_NTASKS'),
    'SCRATCH': os.getenv('SCRATCH'),
    'HOME': os.getenv('HOME'),
    'WORK': os.getenv('WORK'),
})

def grep(match, file):
    result = []
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        if match in line:
            result.append(line)
    return result

def grepA(match, file, num_lines):
    result = []
    with open(file) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if match in line:
            result += lines[i+1:i+16]
            return result

def run(command, debug=False):
    if not debug:
        subprocess.run(command, shell=True)

def srun(_input, _output=None, exe='pw', debug=False):
    if not debug:
        if _output is None:
            if _input[-3:] == '.in':
                _output = _input[:-3] + '.out'
        subprocess.run(f"source {env.WORK}/bin/VARS.sh; srun -n {env.NTASKS} --mpi=pmi2 $ESPRESSO_BIN/{exe}.x -in {_input} > {_output}", shell=True)
        if len(grep("convergence NOT achieved", _output)) > 0:
            exit(16)
