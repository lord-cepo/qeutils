#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

def plot_fc2(path):
    fc2 = np.loadtxt(path+'/MATDYN/MAT2R', skiprows=33)
    with open(path+'/MATDYN/MAT2R') as f:
        lines = f.readlines()
    _, NAT, IBRAV  = map(int, lines[0].split()[:3])
    CELLDM = list(map(float, lines[0].split()[3:]))
    NR = 1
    DIMS = map(int, lines[32].split())
    for dim in DIMS:
        NR *= dim
    
    # array of (9,NAT,NAT,NX*NY*NZ,4). 9=3*3 are the directions of displacement of fc2
    # the last axis has the form (nx+1,ny+1,nz+1,C), where C is fc2
    fc2 = fc2.reshape((-1, NAT, NAT, NR+1, 4))[:, :, :, 1:, :]
    
    # atoms coordinates in bohr
    tau = np.array([line.split()[2:] for line in lines[3:3+NAT]], dtype=np.float64)

    if IBRAV == 5:
        tx = np.sqrt((1-CELLDM[3])/2)
        ty = np.sqrt((1-CELLDM[3])/6)
        tz = np.sqrt((1+2*CELLDM[3])/3)
        AT = [
            CELLDM[0]*np.array([ tx,  -ty, tz]),
            CELLDM[0]*np.array([  0, 2*ty, tz]),
            CELLDM[0]*np.array([-tx,  -ty, tz]),
        ]
    else:
        raise NotImplementedError("solo ibrav = 5")

    # rows of AT are R1,R2,R3, so we have to multiply the columns ji of AT with (nx,ny,nz) of fc2
    # on his last axis
    R = np.einsum('ji,...j->...i', AT, fc2[:, :, :, :, :3]-1)
    
    # tau is summed by broadcasting in the correct axis, negative tau is second axis of fc2, 
    # positive is the third: formula is R_{aijRl} + tau_{jl} - tau_{il}
    R += tau[np.newaxis, np.newaxis, :, np.newaxis, :] - tau[np.newaxis, :, np.newaxis, np.newaxis, :]
    distance = np.linalg.norm(R, axis=-1)

    plt.plot(distance.reshape((-1,1)), np.abs(fc2.reshape((-1,4))[:,-1]), '.')


plot_fc2('/linkhome/rech/genimp01/unr46rr/work/bi2te3/lorenzo/ph333')
plot_fc2('/linkhome/rech/genimp01/unr46rr/work/bi2te3/lorenzo/ph444')
plt.tight_layout()
plt.savefig('fc2.png', dpi=500)
