import os
import subprocess
from types import SimpleNamespace
from warnings import warn

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

def srun(_input, _output=None, exe='pw', debug=False, vars=False):
    if _output is None:
        if _input[-3:] == '.in':
            _output = _input[:-3] + '.out'
        else:
            raise ValueError("output not defined and file doesn't end with .in")
    command = f"srun -n {env.NTASKS} --mpi=pmi2 $ESPRESSO_BIN/{exe}.x -in {_input} > {_output}"
    if vars:
        command = f'source {env.WORK}/bin/VARS.sh; ' + command
    print(command)
    if not debug:
        subprocess.run(command, shell=True)
        if not pw_completed(_output):
            warn("The job is not DONE")
        
def conditional_warn(message, print_message=True):
    if print_message:
        warn(message)

def pw_completed(outfile, warn=True):
    if not os.path.exists(outfile):
        conditional_warn(f"Output file {outfile} not found in {os.getcwd()}", print_message=warn)
        return False
    if len(grep("JOB DONE", outfile)) == 1:
        if len(grep("convergence NOT achieved", outfile)) > 0:
            conditional_warn("Convergence has NOT achieved", print_message=warn)
        return True
    return False