# Re-run PHASE 11's own build_F with ONE change: common-root (bp) terms applied for
# split primes up to PG = 1e7 (same bound as the generic base G), instead of 1e5.
import sys, json, time
import numpy as np
from sympy import primerange
sys.path[:0] = ['lab', '.']   # run from the repo root
try:
    import PHASE11_calm_slope as K
except ImportError:
    import p11_kimi as K
K.B2 = 10**7
Wmax = 10**7
lanes = [int(x) for x in sys.argv[1:]]
po = np.array(list(primerange(3, Wmax + 1)), dtype=np.int64)
for c in lanes:
    t = time.time()
    F = K.build_F(c, Wmax, po)
    S = K.S_curve(F)
    mean = float(F[1:Wmax].mean())
    print(json.dumps({"c": c, "S": S, "meanF": mean, "sec": round(time.time() - t, 1)}), flush=True)
