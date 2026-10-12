# All 300 P9 lanes: full pair series (consistent bound 1e7) and the rings<=1000 truncation (P9's sched stream).
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
    S = K.S_curve(K.build_F(c, Wmax, po))
    St = K.S_curve(K.build_F(c, Wmax, po, trunc=1000))
    print(json.dumps({"c": c, "S": S, "Strunc": St, "sec": round(time.time() - t, 1)}), flush=True)
