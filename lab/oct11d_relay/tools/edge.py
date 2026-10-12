# Is the slightly shallow last step (1e6->1e7: -2.25 vs -2.30) the prime bound sitting AT Wmax?
# Same build as PHASE 11 (bound-consistent), but primes for G and bp run to PG > Wmax.
import sys, json, numpy as np
from sympy import primerange
sys.path[:0] = ['lab', '.']   # run from the repo root
try:
    import PHASE11_calm_slope as K
except ImportError:
    import p11_kimi as K
c, Wmax, PG = int(sys.argv[1]), 10**7, int(float(sys.argv[2]))
po = np.array(list(primerange(3, PG + 1)), dtype=np.int64)
D = 1 - 8 * c; M = 4 * abs(D); chi = K.kronecker_table(D); special3 = (D % 3 == 1)
rho = 1 + chi[po % M]
sel = (rho > 0) & ~((po == 3) & special3)
G = float(np.exp((np.log1p(-2.0 * rho[sel] / po[sel]) - 2.0 * np.log1p(-rho[sel] / po[sel])).sum()))
F = np.full(Wmax + 1, G); F[2::4] = 0.0; F[4::4] *= 2.0
for p in po[(rho == 2) & (po <= Wmax)]:
    if p == 3: F[3::3] *= 3.0
    else: F[p::p] *= (p - 2) / (p - 4)
for p in po[(rho == 1) & (po <= Wmax)]:
    F[p::p] *= (p - 1) / (p - 2)
for p in po[rho == 2]:
    dl = K.tonelli(D, p); bp = (p - 3) / (p - 4)
    F[dl::p] *= bp; F[p - dl::p] *= bp
S = K.S_curve(F)
print(json.dumps({"c": c, "PG": PG, "S": S}))
