import numpy as np
import matplotlib.pyplot as plt

DIR="epw-new"
# filenames
POINT_NAMES = ["G", "Z", "F", "G", "L"]
POINTS = [0.00000, 0.30962,  1.14144,  1.99225, 2.82408]
NKPOINTS = 137

# read data
dft = np.loadtxt(DIR+'/'+"dft.gnu")
dft = dft.reshape(-1, NKPOINTS, 2)
w90 = np.loadtxt(DIR+'/'+"epw.gnu")
w90 = w90.reshape(-1, NKPOINTS, 2)
# w90_1 = np.loadtxt(DIR+'/'+"w90.k12_b40_p.gnu")
# w90_1 = w90.reshape(-1, NKPOINTS, 2)

lab = True
for i in range(30):
    plt.plot(w90[0,:,0], dft[i+60,:,1], color="red", label="DFT" if lab else None)
    plt.plot(w90[0,:,0], w90[i,:,1],  color="blue", label="W90" if lab else None)
    lab = False
plt.legend()
plt.xticks(POINTS, POINT_NAMES)
for point in POINTS:
    plt.axvline(x=point, color="black", linestyle="-")
plt.tight_layout()
plt.show()

plt.plot(w90[0,:,0], dft[77,:,1]-w90[17,:,1], color="blue", label="valence_30")
plt.plot(w90[0,:,0], dft[78,:,1]-w90[18,:,1], color="red", label="conduction_30")


# plt.plot(w90_1[0,:,0], dft[77,:,1]-w90_1[17,:,1], linestyle='--', color="green", label="valence_40")
# plt.plot(w90_1[0,:,0], dft[78,:,1]-w90_1[18,:,1], linestyle='--', color="darkgreen", label="conduction_40")

plt.legend()
plt.xticks(POINTS, POINT_NAMES)
for point in POINTS:
    plt.axvline(x=point, color="black", linestyle="-")
plt.tight_layout()
plt.show()