#!/usr/bin/env python3
"""
PHASE 16 — B=131 slope point + d_home/d_flip omega-accounting.
Date: 2026-10-13. Artifacts: lab/PHASE16_b131_homeflip.py (+ .json, .log).

Frame (GLM CRT-shift collapse, audited STANDS 2026-10-13):
  covered(N)  <=>  exists p in P : N == a (mod p)
  d = number of displaced rings = number of primes whose residue r_p != 0
So the wedge problem is a covering ILP:
  min  sum_p y_p
  s.t. for every N in the layer window: sum_p x_{p, N mod p} >= 1
       for every p: sum_r x_{p,r} = 1        (every ring has exactly one phase)
       y_p >= x_{p,r}  for all r != 0       (y_p = 1 iff ring p displaced)
  x, y binary.  r = 0 is "home".

LEG A — B=131 slope point. The 2-param fit k(B) = 0.876/ln B - 0.117
(measured on B = 31, 53, 97; honest caveat: 2 params, 3 points,
lab/PHASE16_omega_curve.md) predicts k(131) ~ 0.0627. Measure d(m) at
B = 131 (32 primes) for a grid of m, fit k_131, compare.
Frozen predictions BEFORE running:
  A1  every m in the grid is feasible (m <= j(131#) - 1). If some m is
      INFEASIBLE that is not a failure: it certifies m > j(131#) - 1, a
      lower-bound data point on j at 131# (value not in A048669's
      verified prefix). Report it as such, do not treat as a bug.
  A2  k_131 lands within +-20% of 0.0627 (the fit is crude; a 4th point
      inside +-20% keeps the 1/ln B shape alive, outside kills it).
LEG B — d_home/d_flip omega-accounting (GPT handback section 5,
SWARM_HANDBACK_2026-10-12_1719.txt). Ring 2 has only two phases, so
d(m) = min(d_home(m), d_flip(m)) exactly. Under the collapse:
ring 2 home <=> a even (r_2 = 0), flip <=> a odd (r_2 = 1).
So d_home / d_flip are the SAME ILP with x_{2,0} resp. x_{2,1} fixed to 1.
Run at the native schedule (rings = primes <= sqrt(T(m-1))) so results
bind to the existing native points (m=263, d=15, 42 rings, home optimum
already known from PHASE15_dynrings.md -> universal-flip is false there;
the question is the SIZE of the home/flip gap).
Frozen predictions BEFORE running:
  B1  d(263) == 15 == d_home(263)  (binds ILP to the MILP-measured value)
  B2  d_flip(263) >= 15, and the gap d_flip - d_home is small (0-3):
      the wheel's own PHASE15_dynrings note "the turning is not a ring-2
      artefact" predicts ring-2 phase is near-neutral at native scale.
"""
import json
import math
import sys
import time

import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix


def primes_upto(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = [False] * len(sieve[i * i :: i])
    return [i for i in range(2, n + 1) if sieve[i]]


def wedge_ilp(m, prs, ring2=None):
    """Min displaced rings for layer m under the collapse.
    ring2: None (free), 'home' (x_{2,0}=1), or 'flip' (x_{2,1}=1).
    Returns (d, status, seconds); status 0 = optimal."""
    T = (m - 1) * m // 2
    window = list(range(T + 1, T + 1 + m))
    residues = [(p, r) for p in prs for r in range(p)]
    nres = len(residues)
    nprime = len(prs)
    nvar = nres + nprime  # x first, then y
    idx = {}
    for j, pr in enumerate(residues):
        idx[pr] = j

    c = np.zeros(nvar)
    c[nres:] = 1.0  # minimize sum y_p

    rows, cols, vals = [], [], []

    def add(row, col, v):
        rows.append(row)
        cols.append(col)
        vals.append(v)

    nrow = 0
    # coverage: every window position hit by some ring's residue
    for N in window:
        for p in prs:
            add(nrow, idx[(p, N % p)], 1.0)
        nrow += 1
    cov_lb = np.ones(m)
    cov_ub = np.full(m, np.inf)
    # one residue per ring
    rstart = nrow
    for p in prs:
        for r in range(p):
            add(nrow, idx[(p, r)], 1.0)
        nrow += 1
    one_lb = np.ones(nprime)
    one_ub = np.ones(nprime)
    # y_p >= x_{p,r} for r != 0
    yidx = {p: nres + i for i, p in enumerate(prs)}
    ystart = nrow
    for p in prs:
        for r in range(1, p):
            add(nrow, yidx[p], 1.0)
            add(nrow, idx[(p, r)], -1.0)
            nrow += 1
    y_lb = np.zeros(nrow - ystart)
    y_ub = np.full(nrow - ystart, np.inf)

    A = lil_matrix((nrow, nvar), dtype=float)
    A[rows, cols] = vals
    lc = [
        LinearConstraint(A[:m], cov_lb, cov_ub),
        LinearConstraint(A[rstart:rstart + nprime], one_lb, one_ub),
        LinearConstraint(A[ystart:], y_lb, y_ub),
    ]

    lb = np.zeros(nvar)
    ub = np.ones(nvar)
    if ring2 == "home":
        lb[idx[(2, 0)]] = ub[idx[(2, 0)]] = 1.0
    elif ring2 == "flip":
        lb[idx[(2, 1)]] = ub[idx[(2, 1)]] = 1.0

    t0 = time.time()
    res = milp(
        c=c,
        constraints=lc,
        integrality=np.ones(nvar),
        bounds=Bounds(lb, ub),
        options={"time_limit": 300, "mip_rel_gap": 0.0},
    )
    return res.fun, res.status, time.time() - t0


def main():
    out = {"legs": {}}

    # ---------------- LEG A: B=131 slope point
    print("LEG A — B=131 (32 primes) slope grid", flush=True)
    prs131 = primes_upto(131)
    assert len(prs131) == 32, len(prs131)
    pts = []
    for m in [25, 50, 100, 150, 200]:
        d, status, secs = wedge_ilp(m, prs131)
        rec = {"m": m, "d": d, "status": int(status), "seconds": round(secs, 2)}
        pts.append(rec)
        print(f"  m={m}: d={d} status={status} ({secs:.1f}s)", flush=True)
        if status != 0:
            rec["note"] = "infeasible/time-limited -> certifies m > j(131#)-1 (A1)"
            break  # larger m only worse
    feas = [p for p in pts if p["status"] == 0]
    legA = {"points": pts}
    if len(feas) >= 2:
        A = np.array([[p["m"], 1.0] for p in feas])
        k, c = np.linalg.lstsq(A, [p["d"] for p in feas], rcond=None)[0]
        pred = 0.876 / math.log(131) - 0.117
        legA.update(
            k_131=round(k, 4), c_131=round(c, 3),
            k_pred_2param=round(pred, 4),
            within_20pct=bool(abs(k - pred) <= 0.2 * pred),
            A2=bool(abs(k - pred) <= 0.2 * pred),
        )
        print(f"  fit: k={k:.4f} c={c:.3f} | pred={pred:.4f} -> A2={'PASS' if legA['A2'] else 'FAIL'}", flush=True)
    legA["A1"] = all(p["status"] == 0 for p in pts)
    out["legs"]["A_b131_slope"] = legA

    # ---------------- LEG B: d_home/d_flip at native schedule
    print("LEG B — d_home/d_flip, native schedule", flush=True)
    legB = {}
    for m in [100, 263]:
        Bnat = int(math.isqrt((m - 1) * m // 2))
        prs = primes_upto(Bnat)
        row = {"m": m, "native_bound": Bnat, "n_rings": len(prs)}
        for mode in ["free", "home", "flip"]:
            d, status, secs = wedge_ilp(m, prs, ring2=None if mode == "free" else mode)
            row[f"d_{mode}"] = d
            row[f"status_{mode}"] = int(status)
            print(f"  m={m} ({len(prs)} rings) {mode}: d={d} status={status} ({secs:.1f}s)", flush=True)
        row["B1"] = bool(m != 263 or (row["d_free"] == 15 and row["d_home"] == 15))
        row["home_flip_gap"] = (row["d_flip"] - row["d_home"]) if row["status_flip"] == 0 and row["status_home"] == 0 else None
        legB[str(m)] = row
    b = legB.get("263", {})
    legB["B1"] = bool(b.get("d_free") == 15 and b.get("d_home") == 15)
    legB["B2"] = bool(b.get("home_flip_gap") is not None and 0 <= b["home_flip_gap"] <= 3)
    out["legs"]["B_homeflip"] = legB

    with open("lab/PHASE16_b131_homeflip.json", "w") as f:
        json.dump(out, f, indent=2)
    print("JSON -> lab/PHASE16_b131_homeflip.json", flush=True)


if __name__ == "__main__":
    main()
