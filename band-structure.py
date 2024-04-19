from mp_api.client import MPRester
# from pymatgen.electronic_structure.plotter import BSPlotter
import matplotlib.pyplot as plt
import numpy as np
import clipboard
s = {
    "bi2se3": "mp-541837",
    "bi2te3": "mp-34202",
}

with MPRester(api_key="YEqBAsdp3OAsAD5UmnZ47PITnp3Xni9d") as mpr:
    bandstructure = mpr.get_bandstructure_by_material_id(s["bi2se3"])
x = bandstructure.distance
for bands in bandstructure.bands.values():
    for band in bands:
        plt.plot(x, band, color="blue")
# n_points = 20
indices = []
labels = []
# distances = []
sparseness = len(bandstructure.kpoints)//100
if sparseness == 0:
    sparseness = 1
clip = ""
for i, k in enumerate(bandstructure.kpoints):
    if k.label is not None:
        if "\\" in k.label:
            labels.append("$" + k.label + "$")
        labels.append(k.label)
        # indices.append(i)
        # if i > 1:
        #     distances.append(x[i-1]-x[i-2])
for k in bandstructure.kpoints[::sparseness]:
    clip += str(k.frac_coords[0])  + ' ' \
        + str(k.frac_coords[1]) + ' ' \
        + str(k.frac_coords[2]) + ' 1 \n'
clipboard.copy(clip)

with open("hexagonal-pbe-nc-sr.bands", encoding="utf-8") as f:
    lines = f.readlines()
qe_nbnd = int(lines[0].split()[2][:-1])
qe_nks = int(lines[0].split()[4])
qe_bands = np.empty((qe_nks, qe_nbnd))
# qe_kpoints = []
arr = []
count = 0
for line in lines[1:]:
    if len(line.split()) != 3:
        arr += [float(el) for el in line.split()]
    if len(arr) == qe_nbnd:
        qe_bands[count] = np.array(arr)
        arr = []
        count += 1
    # if len(line.split()) == 3:
    #     qe_kpoints.append([float(el) for el in line.split()])
for i in range(qe_nbnd):
    plt.plot(x[::sparseness], qe_bands[:, i]-3, color="red")

# mp_kpoints = [k.frac_coords for k in bandstructure.kpoints[::sparseness]]
# for mp, qe in zip(mp_kpoints, qe_kpoints):
#     norm = np.linalg.norm(np.array(mp)-np.array(qe))
#     if norm > 1e-3:
#         print(mp, qe, norm)

xticks = []
xticklabels = [] 
lab = "vuota"
for index, label in zip(indices, labels):
    if lab != label:
        plt.axvline(x[int(index)], color="black")
        xticks.append(x[int(index)])
        xticklabels.append(label)
    lab = label
    
    
# plotter = BSPlotter(bandstructure)
# # plotter.get_plot()
# plotter.show()

plt.xticks(xticks, xticklabels)
plt.show()