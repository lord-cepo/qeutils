import numpy as np
import matplotlib.pyplot as plt

sfile = f'bi2se3-pbe-nc-sr.qbands'
tfile = f'bi2te3-pbe-nc-sr.qbands'

vlines = ['$\\Gamma$', 'T', 'H2|H0', 'L', '$\\Gamma$', 'S0|S2', 'F', '$\\Gamma$']
xvlines = [0,30,60,61,91,121,151,152,182,212]
xvticks = [0,30,60,91,121,152,182,212]
shifts = {
    "bi2se3": {
        'pbe' : 7.14,
        'lda' : 9.92,
        'pbefr' : 7.9451
    },
    "bi2te3": {
        'pbe' : 8.3293,
        'lda' : 9.9059-0.095,
        'pbefr' : 8.5416
    }
}
def get_bandstructure(filename):
    with open(filename, encoding="utf-8") as f:
        words = f.read().split()
    _qe_nbnd = int(words[2][:-1])
    _qe_nks = int(words[4])
    qe_bands = np.empty((_qe_nks, _qe_nbnd))
    _qe_nbnd_3 = _qe_nbnd+3
    count = -1
    for i, word in enumerate(words[6:]):
        if i %  _qe_nbnd_3 not in [0,1,2]:
            qe_bands[count][(i-3)%_qe_nbnd_3] = float(word)
        elif i %  _qe_nbnd_3 == 0:
            count += 1
    return {"bands": qe_bands, "nbnd": _qe_nbnd, "nks": _qe_nks}

s = get_bandstructure(sfile)
t = get_bandstructure(tfile)
x = np.linspace(0, 1, s["nks"])

for i in range(s["nbnd"]):
    plt.plot(x, s['bands'][:, i], color="red", label='bi2se3 PBE' if i == 1 else None)
for i in range(t["nbnd"]):
    plt.plot(x, t['bands'][:, i], color="blue", label='bi2te3 PBE' if i == 1 else None)

for xv in xvlines:
    plt.axvline(x=x[xv], color="black")

plt.xticks([x[xv] for xv in xvticks], vlines)
plt.legend()
plt.tight_layout()
plt.savefig("../../Desktop/results/qbands.png", dpi=300)

plt.show()