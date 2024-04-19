#!/usr/bin/env python
import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

read = False
out = []
if sys.argv[2] == 'fr':
    out.append('# __FR__\n')
for line in lines:
    if "</PP_INPUTFILE>" in line:
        read = False
    if read:
       out.append(line) 
    if "<PP_INPUTFILE>" in line:
        read = True

with open(sys.argv[1].split('.')[0]+'.dat', 'w') as f:
    f.writelines(out)