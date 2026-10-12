#!/usr/bin/env python3
"""
PHASE 15 (part 2) — wedge d-curve under varying ring schedules.

Part 1 (PHASE15_wedge_slope) found, on object A with the 25 fixed rings
(primes <= 97), over 244 measured layers 14..257:
    d(m) ~ 0.215*U(m) + 0.051*m + 0.35      (R^2 = 0.974)
where U(m) = #{j in 1..m : T(m-1)+j has no prime factor <= 97} (the
home-uncoverable "rough" ticks). U/m ~ e^{-gamma}/ln 97 ~ 0.123. So the
famous slope 1/13.5 decomposes as 0.215*0.1227 + 0.051 ~ 0.077 ~ 1/13.0:
~1/3 rough-tick harvesting, ~2/3 re-cover overhead.

Consequence [F from that fit, mechanism attribution [S]]: the slope must
depend on the ring bound B. Two legs test this:

LEG S (fixed-B sensitivity): B = 31 (11 rings) and B = 53 (16 rings),
object A, m in {60, 100, 150}. Predict d from the B=97 constants with
U_B density e^{-gamma}/ln B:
    d_pred(m; B) = 0.215*U_B(m) + 0.051*m + 0.35
Feasibility caveat: layers with m >= h(#B) (Jacobsthal of the primorial)
return None; None on m <= 150 for B=31 would itself be informative
(j(31#) <= 150). Frozen: report d values and the None pattern either way.

LEG N (native schedule): rings = primes <= sqrt(T(m-1)) -- the wheel's
own sieve bound. Then EVERY composite value <= T has a factor <= sqrt(T),
so all composite ticks are home-covered and U collapses to the prime-value
count P(m) = #{j : T+j prime} ~ m/(2 ln m) [F]. Predictions, object A:
  N1: d finite on all sampled layers m in {263, 300, 400, 600, 1000}.
  N2: d(m) within [0.65*P(m), 0.65*P(m) + 0.06*m] (harvest-only band to
      harvest+overhead band, reusing part-1 constants).
  N3: d(m)/m at m=1000 < d(m)/m at m=263 (sublinear growth).
Convention: identical to probes/j1c_wedge_milp.py v2 and
lab/PHASE14_objA_dcurve.py (home c*=0, cover iff c == (j+T) mod p,
d = min #rings off home; d=0 decided arithmetically, MILP else).
"""
import json
import os
import sys
import time
from math import isqrt

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

LIMIT = 1010000
comp = bytearray(LIMIT)
comp[0] = comp[1] = 1
for p in range(2, isqrt(LIMIT) + 1):
    if not comp[p]:
        comp[p * p::p] = b'\x01' * (((LIMIT - 1 - p * p) // p) + 1)


def primes_upto(n):
    return [p for p in range(2, n + 1) if not comp[p]]


def T(m):
    return m * (m - 1) // 2


def solve_layer_rings(m, rings):
    """Exact d(m) for object 'all' with an explicit ring list."""
    t = T(m)
    ticks = list(range(1, m + 1))
    idx = {}
    i = 0
    for p in rings:
        for c in range(p):
            idx[('x', p, c)] = i
            i += 1
    ybase = i
    for p in rings:
        idx[('y', p)] = i
        i += 1
    NVAR = i
    rows, lbs, ubs = [], [], []
    for p in rings:
        row = np.zeros(NVAR)
        for c in range(p):
            row[idx[('x', p, c)]] = 1
        rows.append(row); lbs.append(1); ubs.append(1)
    for j in ticks:
        row = np.zeros(NVAR)
        for p in rings:
            row[idx[('x', p, (j + t) % p)]] = 1
        rows.append(row); lbs.append(1); ubs.append(np.inf)
    for p in rings:
        for c in range(1, p):
            row = np.zeros(NVAR)
            row[idx[('y', p)]] = 1
            row[idx[('x', p, c)]] = -1
            rows.append(row); lbs.append(0); ubs.append(np.inf)
    cobj = np.zeros(NVAR)
    for p in rings:
        cobj[idx[('y', p)]] = 1
    res = milp(c=cobj, constraints=LinearConstraint(np.array(rows), lbs, ubs),
               bounds=Bounds(0, 1), integrality=np.ones(NVAR))
    if res.status != 0:
        return None, int(res.status), str(getattr(res, 'message', ''))
    return int(round(res.fun)), 0, 'optimal'


def P(m):
    t = T(m)
    return sum(1 for j in range(1, m + 1) if not comp[t + j])


def U_B(m, B):
    t = T(m)
    small = primes_upto(B)
    return sum(1 for j in range(1, m + 1)
               if t + j > B and all((t + j) % p for p in small))


OUT = 'lab/PHASE15_dynrings.json'


def main():
    out = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            out = json.load(f)
    done = out.get('done', {})

    # LEG S: fixed-B sensitivity
    for B in (31, 53):
        rings = primes_upto(B)
        for m in (60, 100, 150):
            key = f"S_B{B}_m{m}"
            if key in done:
                continue
            t1 = time.time()
            d, st, msg = solve_layer_rings(m, rings)
            u = U_B(m, B)
            pred = 0.215 * u + 0.051 * m + 0.35
            done[key] = {'d': d, 'status': st, 'msg': msg[:120], 'U_B': u,
                         'pred': round(pred, 2), 'nrings': len(rings)}
            out['done'] = done
            with open(OUT, 'w') as f:
                json.dump(out, f, indent=1)
            print(f"{key}: d={d} U_B={u} pred={pred:.2f} "
                  f"({time.time()-t1:.1f}s)", flush=True)

    # LEG N: native schedule
    for m in (263, 300, 400, 600, 1000):
        key = f"N_m{m}"
        if key in done:
            continue
        t1 = time.time()
        rings = primes_upto(isqrt(T(m)))
        d, st, msg = solve_layer_rings(m, rings)
        p = P(m)
        done[key] = {'d': d, 'status': st, 'msg': msg[:120], 'P': p,
                     'nrings': len(rings),
                     'band': [round(0.65 * p, 1), round(0.65 * p + 0.06 * m, 1)]}
        out['done'] = done
        with open(OUT, 'w') as f:
            json.dump(out, f, indent=1)
        print(f"{key}: d={d} P={p} nrings={len(rings)} "
              f"band={done[key]['band']} ({time.time()-t1:.1f}s)", flush=True)

    print("ALL DONE", flush=True)


if __name__ == '__main__':
    main()
