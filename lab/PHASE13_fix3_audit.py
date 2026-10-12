#!/usr/bin/env python3
"""
PHASE 13 — audit of Claude's 11d fix 3 (B2/PG bound mismatch).

Claim under test: in lab/PHASE11_calm_slope.py, the generic base G runs over
odd primes <= PG = 1e7 but the common-root (bp) correction is applied only for
split primes <= B2 = 1e5. Every split prime in (1e5, 1e7] then leaves a
uniform -4/p^2 on ln F[d] with no +back on the +/-delta classes, so mean(F)
sits ~7.9e-7 below 1 and S(W) picks up -7.9e-7 * W. That was the "not
summable, drift still growing at 1e7" filed as a mechanism.

Checks (frozen before running):
 K1. (S_fixed - S_asrun)/W == ~+7.9e-7 for every W >= 1e5, lanes 14 and 39.
 K2. band-mean of F over [9e6, 1e7) rises by ~+7.9e-7 under the fix.
 K3. the last-decade slope of S (1e6 -> 1e7) collapses from ~-10 to the
     ~-2.3-per-decade family (C*S steps ~= -ln10).
 K4. C*S per-decade steps for the fixed series are ~= -ln10 = -2.3026,
     cross-lane sd small, EXCEPT a shallow last step attributable to the
     prime bound sitting at Wmax (Claude: moving bound to 3e7 deepens it).

Independence: own code (the filed probe), one module constant changed.
"""
import json
import sys
import time

import numpy as np
from sympy import primerange

sys.path.insert(0, "lab")
import PHASE11_calm_slope as P

Wmax = 10**7
primes_odd = np.array(list(primerange(3, Wmax + 1)), dtype=np.int64)
DEC = [10**k for k in range(2, 8)]
out = {"frozen_checks": ["K1", "K2", "K3", "K4"], "Wmax": Wmax}

asrun = json.load(open("lab/PHASE11_calm_slope.json"))

for c in [14, 39]:
    t0 = time.time()
    P.B2 = 10**5                     # as filed
    F_old = P.build_F(c, Wmax, primes_odd)
    P.B2 = 10**7                     # the fix (bp over all split primes <= plim)
    F_new = P.build_F(c, Wmax, primes_odd)

    S_old, S_new = P.S_curve(F_old, DEC), P.S_curve(F_new, DEC)
    filed = asrun["lanes"][str(c)]["full"]["S"]

    # K1: relative drift per W
    k1 = {str(W): (S_new[str(W)] - S_old[str(W)]) / W for W in DEC if W >= 10**5}
    k1_filed = {str(W): (S_new[str(W)] - filed[str(W)]) / W
                for W in DEC if str(W) in filed}

    # K2: band means
    band = slice(9 * 10**6, 10**7)
    k2 = {"old": float(F_old[band].mean()), "new": float(F_new[band].mean()),
          "delta": float(F_new[band].mean() - F_old[band].mean())}

    # K3/K4: slopes and C*S steps (C = prod (1-rho/p)/(1-1/p), odd primes)
    D = 1 - 8 * c
    chi = P.kronecker_table(D)
    po = primes_odd
    rho = 1 + chi[po % (4 * abs(D))]
    lnC = np.log1p(-rho / po) - np.log1p(-1.0 / po)
    C = float(np.exp(lnC.sum()))
    sl_old = P.slopes(S_old)
    sl_new = P.slopes(S_new)
    cs_steps = {k: C * v for k, v in sl_new.items()}

    # edge check: C*S + ln W at 1e7 (should be O(1), Claude: ~ -0.4 family)
    edge = C * S_new["10000000"] + np.log(10**7)

    out[str(c)] = {
        "C_lane": C,
        "K1_rel_drift_per_W": k1,
        "K1_vs_filed": k1_filed,
        "K2_band_mean": k2,
        "S_old": S_old, "S_new": S_new,
        "slopes_old": sl_old, "slopes_new": sl_new,
        "K4_CS_steps": cs_steps,
        "K4_CS_plus_lnW_at_1e7": float(edge),
        "max_abs_Fdiff": float(np.abs(F_new - F_old).max()),
        "seconds": time.time() - t0,
    }
    print(f"c={c}: C={C:.4f}  drift/W={list(k1.values())}")
    print(f"   band-mean delta={k2['delta']:.3e}  "
          f"last-decade slope old={sl_old['1000000->10000000']:.3f} "
          f"new={sl_new['1000000->10000000']:.3f}")
    print(f"   C*S steps new={ {k: round(v,4) for k,v in cs_steps.items()} }")
    print(f"   C*S+lnW@1e7={edge:.4f}  ({time.time()-t0:.0f}s)")

json.dump(out, open("lab/PHASE13_fix3_audit.json", "w"), indent=1)
print("-> lab/PHASE13_fix3_audit.json")
