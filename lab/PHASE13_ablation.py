#!/usr/bin/env python3
"""
PHASE 13 — reproduction of GPT's mean-preserving common-root ablation.
Conventions: lab/PHASE13_ablation_prereg.md (frozen before running).
"""
import json
import sys

import numpy as np
from sympy import primerange

sys.path.insert(0, "lab")
import PHASE11_calm_slope as P

Wmax = 10**6
DEC = [10**k for k in range(2, 7)]
po = np.array(list(primerange(3, min(1000, Wmax) + 1)), dtype=np.int64)
out = {}

# mu = product over split p<=1000 of (1 - 2/(p-2)^2)  [GPT's corrected factor]
c = 14
D = 1 - 8 * c
chi = P.kronecker_table(D)
rho = 1 + chi[po % (4 * abs(D))]
sp = po[rho == 2] - 2
ln_mu = np.log1p(-2.0 / sp**2).sum()
mu = float(np.exp(ln_mu))
print("mu computed:", mu, " GPT claimed: 0.7016491483")

P.B2 = 1000  # consistent bound at the truncation
FA = P.build_F(c, Wmax, po, trunc=1000)
FB = P.build_F(c, Wmax, po, trunc=1000, no_cd=True)
FC = FB / mu

for tag, F in [("A", FA), ("B", FB), ("C", FC)]:
    S = P.S_curve(F, DEC)
    out[tag] = S
    print(tag, {w: round(v, 3) for w, v in S.items()})

band = slice(9 * 10**5, 10**6)
print("band-mean B:", float(FB[band].mean()), " C:", float(FC[band].mean()))

# P2: linearity of B
r = out["B"]["1000000"] / out["B"]["100000"]
print("P2 S_B(1e6)/S_B(1e5) =", round(r, 3))

# P4: slope ratio for C
s1 = abs(out["C"]["10000"] - out["C"]["1000"])
s2 = abs(out["C"]["1000000"] - out["C"]["100000"])
print("P4 slope ratio (1e5-1e6)/(1e3-1e4) for C =", round(s2 / s1, 4))

# P5: log-fit vs linear-fit on [1e3, 1e6]
Ws = np.array([10**3, 10**4, 10**5, 10**6], dtype=float)
y = np.array([out["C"][str(int(w))] for w in Ws])
Xl = np.vstack([np.ones_like(Ws), np.log(Ws)]).T
Xw = np.vstack([np.ones_like(Ws), Ws]).T
bl, *_ = np.linalg.lstsq(Xl, y, rcond=None)
bw, *_ = np.linalg.lstsq(Xw, y, rcond=None)
resl = float(((y - Xl @ bl) ** 2).sum())
resw = float(((y - Xw @ bw) ** 2).sum())
print("P5 log-fit resid SS:", round(resl, 6), " W-fit resid SS:", round(resw, 6),
      " ->", "PASS (log-like)" if resl < resw else "FAIL")

# P1: compare with GPT's A
gptA = {"100": -6.119, "1000": -9.285, "10000": -11.520,
        "100000": -13.073, "1000000": -13.951}
print("P1 max |A - GPT| =", max(abs(out["A"][w] - g) for w, g in gptA.items()))

json.dump({"mu": mu, **out, "P2_ratio": r, "P4_ratio": s2 / s1,
           "P5_resid_log": resl, "P5_resid_W": resw},
          open("lab/PHASE13_ablation.json", "w"), indent=1)
print("-> lab/PHASE13_ablation.json")
