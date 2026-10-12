#!/usr/bin/env python3
"""
J1c v2 — wedge distance / near-wipe spectrum, CORRECTED home phase.

CORRECTION (2026-10-11, after Grok's relay audit): v1 measured distance from
c*_p = (-T(m-1)) mod p. But the frozen cover rule is: ring p covers tick j iff
chosen phase c == (j + T(m-1)) mod p. The realized turning (ring p resting on
its shadow = hitting exactly the ticks whose VALUE is divisible by p, i.e.
j ≡ -T mod p) therefore corresponds to phase c = 0, not c = -T. v1's home was
the phase hitting ticks j ≡ -2T (mod p) — off the wheel. The error is traced
to GLM's frozen spec, which stated c* = -T mod p AND cover c ≡ j - o_p with
o_p = -T (jointly inconsistent by 2T). v1's feasibility results (all-ticks
wipeable = {2..13}) are unaffected — feasibility is phase-independent.

v2 conventions (stated before running):
  - Rings: primes <= 97 (25), one-hot x[p,c], home phase c* = 0.
  - Cover: tick j covered iff chosen phase c == (j + T) mod p, T = T(m-1).
  - d(m) = min #rings at phase != 0 covering the object.
  - Objects per layer m in 41..391:
      A 'all'      : every tick j in 1..m (GLM's primary spec)
      B 'eligible' : habitat-eligible ticks (column_law.py eligible())
      C 'prime'    : B minus provably-composite: for m ≡ 2 mod 4 drop gcd-1
                     ticks (value = odd + odd = even > 2, never prime — C1)
      D 'ends'     : ticks {1, m} (the sparse-render object)
  - d = 0 decided arithmetically (every object's tick has a factor <= 97);
    MILP only where d >= 1. Near-wipe spectrum = {m : d = 2}.

FROZEN PREDICTIONS (before running):
  P1 (Grok): on D, d = 0 on exactly the layers where T(m-1)+1 is 97-smooth;
             expect ~258 such layers in 41..391; rest have d = 1.
  P2 (GLM parity wedge theorem): on C, every EVEN m has d = 1 (prime-ticks
             share one parity: m≡0 mod4 -> coprime/odd, m≡2 mod4 -> gcd-2/
             even; one flip of ring 2 stamps the class; every layer 41..391
             holds primes > 97 forcing d >= 1). On odd m, d >= 2 iff some
             prime-eligible tick's value has no odd prime factor <= 97.
"""
import json
import numpy as np
from math import isqrt
from scipy.optimize import milp, LinearConstraint, Bounds

PRIMES = [p for p in range(2, 98) if all(p % q for q in range(2, isqrt(p) + 1))]
assert len(PRIMES) == 25

LIMIT = 391 * 392 // 2 + 8
comp = bytearray(LIMIT)
comp[0] = comp[1] = 1
for p in range(2, isqrt(LIMIT) + 1):
    if not comp[p]:
        comp[p * p::p] = b'\x01' * (((LIMIT - 1 - p * p) // p) + 1)
SPF = list(range(LIMIT))          # spf sieve
for p in range(2, isqrt(LIMIT) + 1):
    if SPF[p] == p:
        for q in range(p * p, LIMIT, p):
            if SPF[q] == q:
                SPF[q] = p


def smooth(n, B=97):
    """True iff n has a prime factor <= B (n <= LIMIT, composite or not)."""
    if n <= B:
        return True
    return SPF[n] <= B


def eligible(k, m):
    import math
    d = math.gcd(k, m)
    return d == 1 or (d == 2 and m % 4 == 2)


def object_ticks(m, obj):
    T = m * (m - 1) // 2
    if obj == 'all':
        return [j for j in range(1, m + 1)], T
    ticks = []
    for j in range(1, m + 1):
        if not eligible(j, m):
            continue
        if obj == 'prime' and m % 4 == 2:
            import math
            if math.gcd(j, m) == 1:
                continue  # value even > 2, never prime (C1)
        ticks.append(j)
    if obj == 'ends':
        return [1, m], T
    return ticks, T


def solve_layer(m, obj):
    """Exact d(m); 0 decided arithmetically, MILP for d >= 1."""
    ticks, T = object_ticks(m, obj)
    if all(smooth(T + j) for j in ticks):
        return 0
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
    rows, lbs, ubs = [], [], []
    for p in PRIMES:
        row = np.zeros(NVAR)
        for c in range(p):
            row[idx[('x', p, c)]] = 1
        rows.append(row); lbs.append(1); ubs.append(1)
    for j in ticks:
        row = np.zeros(NVAR)
        for p in PRIMES:
            row[idx[('x', p, (j + T) % p)]] = 1
        rows.append(row); lbs.append(1); ubs.append(np.inf)
    for p in PRIMES:
        for c in range(1, p):          # home is c = 0
            row = np.zeros(NVAR)
            row[idx[('y', p)]] = 1
            row[idx[('x', p, c)]] = -1
            rows.append(row); lbs.append(0); ubs.append(np.inf)
    cobj = np.zeros(NVAR)
    for p in PRIMES:
        cobj[idx[('y', p)]] = 1
    res = milp(c=cobj, constraints=LinearConstraint(np.array(rows), lbs, ubs),
               bounds=Bounds(0, 1), integrality=np.ones(NVAR))
    if res.status != 0:
        return None
    return int(round(res.fun))


def dist_str(dists):
    from collections import Counter
    c = Counter(dists.values())
    return {repr(k): v for k, v in sorted(c.items(), key=lambda kv: (kv[0] is None, kv[0] or 0))}


def save(out):
    with open('lab/J1C_spectrum_v2.json', 'w') as f:
        json.dump(out, f, indent=1)


def main():
    # Object D ('ends') recovered from the crashed run's log: d distribution
    # {0: 258, 1: 93}; reuse via checkpoint if present.
    import os
    out = {}
    if os.path.exists('lab/J1C_spectrum_v2.json'):
        with open('lab/J1C_spectrum_v2.json') as f:
            out = json.load(f)

    # Object A (all ticks): arithmetic only — capacity bound excludes every
    # layer m >= 157 (sum ceil(m/p) over 25 rings ~ 0.84m + 25 < m); below
    # that, 97-rough ticks still block d=0 (v1: wipeable = {2..13} to 3000).
    cap = {m: sum(-(-m // p) for p in PRIMES) for m in (41, 100, 156, 157, 391)}
    out['all_capacity'] = {str(m): c for m, c in cap.items()}
    print("capacity bound (max coverable ticks):", cap, flush=True)

    # Object C (prime-eligible): odd m full sweep (the live hunt); even m
    # every 10th as a parity-theorem check (GLM: d = 1 throughout).
    # None = infeasible (capacity-impossible wipe). Checkpointed per layer.
    todo = [m for m in range(41, 392) if m % 2 == 1] + list(range(42, 392, 10))
    prime = out.get('prime', {})
    for i, m in enumerate(todo):
        if str(m) in prime:
            continue
        prime[m] = solve_layer(m, 'prime')
        out['prime'] = prime
        save(out)
        if (i + 1) % 20 == 0:
            print(f"  prime: {i+1}/{len(todo)} (layer {m})", flush=True)
    print("[prime] d distribution:", dist_str(prime), flush=True)
    print("[prime] d>=2 layers:", sorted((m, d) for m, d in prime.items() if d and d >= 2), flush=True)
    print("[prime] infeasible layers:", sorted(m for m, d in prime.items() if d is None), flush=True)
    evens = {m: d for m, d in prime.items() if m % 2 == 0}
    print("[prime] even-sample d=1 verdict:", all(d == 1 for d in evens.values()),
          evens, flush=True)

    # Object B (habitat-eligible) on m ≡ 2 mod 4 sample: differs from C
    # because flipping ring 2 off the odd even-valued coprime ticks can
    # orphan them — test whether d stays 1.
    todo_b = [m for m in range(42, 392, 4)]
    elig = out.get('eligible_m2mod4', {})
    for i, m in enumerate(todo_b):
        if str(m) in elig:
            continue
        elig[m] = solve_layer(m, 'eligible')
        out['eligible_m2mod4'] = elig
        save(out)
    print("[eligible, m≡2 mod 4 sample] d distribution:", dist_str(elig), flush=True)
    save(out)
    # P1 arithmetic check on object D: d=0 <=> T(m-1)+1 smooth (tick m always
    # smooth: T(m) = m(m+1)/2, and any prime factor of T(m) is <= m+1 <= 392;
    # verify directly anyway)
    zeros = [m for m in range(41, 392)
             if smooth(m * (m - 1) // 2 + 1) and smooth(m * (m + 1) // 2)]
    print("P1 check: arithmetic d=0 layers on 'ends':", len(zeros), zeros[:20])
    # P2 support: odd-m obstruction scan (prime-eligible tick with no odd
    # prime factor <= 97)
    obstr = []
    for m in range(41, 392, 2):
        ticks, T = object_ticks(m, 'prime')
        bad = [j for j in ticks if not smooth(T + j) and (T + j) % 2 == 1
               and all((T + j) % p for p in PRIMES if p != 2)]
        if bad:
            obstr.append((m, bad[:3]))
    print("P2 check: odd layers with a prime-eligible 2x97-rough tick:",
          len(obstr), obstr[:10])


if __name__ == '__main__':
    main()
