#!/usr/bin/env python3
"""
J1c — wedge distance / near-wipe spectrum (GLM frozen spec, CP-SAT one-hot
encoded as MILP; scipy.optimize.milp / HiGHS — no ortools needed).

Conventions (stated BEFORE running, per house rule):
  - Rings: primes <= 97 (25 rings), one-hot phase x[p,c] in {0,1}, sum_c x = 1.
  - Realized phase: c*_p = (-T(m-1)) mod p where T = triangular.
  - Tick j on layer m has value n = T(m-1) + j; ring p covers tick j iff its
    chosen phase c == (j + T(m-1)) mod p  (GLM's c ≡ j - o_p with o_p = -T(m-1)).
  - Wipe(m): EVERY tick j in 1..m covered by >= 1 ring. (seats-only variant:
    j in {1, m} — run as sensitivity, flagged.)
  - Distance: y[p] >= x[p,c] for all c != c*_p; minimize sum_p y[p].
    d(m) = optimal objective. Near-wipe spectrum = {m : d(m) = 2}.
  - Layers 41..391 (GLM's range).
"""
import json
from math import isqrt
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np

PRIMES = [p for p in range(2, 98) if all(p % q for q in range(2, isqrt(p) + 1))]
assert len(PRIMES) == 25, len(PRIMES)

# variable layout: x[p][c] flattened, then y[p]
idx = {}
i = 0
for p in PRIMES:
    for c in range(p):
        idx[('x', p, c)] = i
        i += 1
ybase = i
for p in PRIMES:
    idx[('y', p)] = i
    i += 1
NVAR = i

def solve_layer(m, seats_only=False):
    T = m * (m - 1) // 2
    cstar = {p: (-T) % p for p in PRIMES}
    ticks = [1, m] if seats_only else range(1, m + 1)

    rows, lbs, ubs = [], [], []
    # one-hot per ring
    for p in PRIMES:
        row = np.zeros(NVAR)
        for c in range(p):
            row[idx[('x', p, c)]] = 1
        rows.append(row); lbs.append(1); ubs.append(1)
    # cover each tick
    for j in ticks:
        row = np.zeros(NVAR)
        for p in PRIMES:
            row[idx[('x', p, (j + T) % p)]] = 1
        rows.append(row); lbs.append(1); ubs.append(np.inf)
    # y[p] >= x[p,c] for c != c*
    for p in PRIMES:
        for c in range(p):
            if c == cstar[p]:
                continue
            row = np.zeros(NVAR)
            row[idx[('y', p)]] = 1
            row[idx[('x', p, c)]] = -1
            rows.append(row); lbs.append(0); ubs.append(np.inf)

    cobj = np.zeros(NVAR)
    for p in PRIMES:
        cobj[idx[('y', p)]] = 1

    res = milp(c=cobj, constraints=LinearConstraint(np.array(rows), lbs, ubs),
               bounds=Bounds(0, 1),
               integrality=np.ones(NVAR))
    if res.status not in (0,):
        return None
    return int(round(res.fun))

def main():
    spectrum, dists = [], {}
    for m in range(41, 392):
        d = solve_layer(m)
        dists[m] = d
        if d == 2:
            spectrum.append(m)
        if (m - 40) % 50 == 0:
            print(f"  ...layer {m}", flush=True)
    print("near-wipe spectrum {m : d(m)=2}:", spectrum)
    from collections import Counter
    print("d(m) distribution:", dict(sorted(Counter(dists.values()).items())))
    with open('lab/J1C_spectrum.json', 'w') as f:
        json.dump({'spectrum_d2': spectrum, 'dist': dists}, f)

if __name__ == '__main__':
    main()
