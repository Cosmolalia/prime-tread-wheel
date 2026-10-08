#!/usr/bin/env python3
"""
stagger_mc.py — does the quadratic stagger counter change mouth statistics?

The sieve's implicit model: each lap is an independent draw (offsets i.i.d.
uniform). The wheel's claim: all offsets are digits of ONE quadratic counter
s(m) = -T(m-1), so laps are correlated through it.

Composite-ness rule (exact): tick k on lap m is SHUT iff some prime
p <= sqrt(T(m-1)+k) strikes it:  k ≡ s(m) (mod p),  s(m) = -T(m-1).
Arcs from p > sqrt(value) never witness compositeness (their hits are the
prime itself or a multiple already witnessed by a smaller factor), so the
arc set is p <= isqrt(T(m-1)+KMAX) — matching the real sieve limit.

Mouth width W(m) = first open (unstruck) tick in 1..KMAX.

Both models share the prime set, the arc-set rule, and the window, so any
truncation bias cancels in the comparison. Only the generator differs:
  - quad: o_p = s(m) mod p     (the actual stagger field, one counter)
  - iid : o_p ~ uniform(1..p)  (independent-lap / sieve null model)

Validation first: quad model vs actual first-prime offsets (sympy) on a
sample of laps. If they agree, the comparison is meaningful.
"""
import math
import numpy as np
from sympy import nextprime

KMAX = 2000
M_LO, M_HI = 500, 20000   # >=500: lap >> window, arc rule exact (see module docstring)
N_IID = 20000
N_VALIDATE = 400

def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool); sieve[:2] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]: sieve[i*i::i] = False
    return np.nonzero(sieve)[0]

PR_ALL = primes_upto(int(math.isqrt(20000*20001//2 + KMAX)) + 10)

def T(m): return m * (m + 1) // 2

def mouth_width(m, offsets_fn):
    lim = math.isqrt(T(m - 1) + KMAX)
    PR = PR_ALL[PR_ALL <= lim]
    covered = np.zeros(KMAX + 2, dtype=bool)
    for p in PR:
        covered[offsets_fn(p)::p] = True
    w = 1
    while w <= KMAX and covered[w]:
        w += 1
    return w if w <= KMAX else KMAX + 1

print(f"arc primes: up to {PR_ALL[-1]} ({len(PR_ALL)}); window KMAX={KMAX}")

# ---- validation: quad model vs actual ----
print(f"\n== validation: quad-model W vs actual first-prime offset, {N_VALIDATE} laps ==")
bad = 0
for i, m in enumerate(range(M_LO, M_HI + 1, (M_HI - M_LO) // N_VALIDATE)):
    sm = -T(m - 1)
    w = mouth_width(m, lambda p, sm=sm: sm % p or p)
    a = nextprime(T(m - 1)) - T(m - 1)
    if w != a:
        bad += 1
        if bad <= 5:
            print(f"  MISMATCH m={m}: model W={w} actual={a}")
print(f"validation mismatches: {bad}/{N_VALIDATE}")

# ---- quad model over the full range ----
print(f"\n== quad model: laps m={M_LO}..{M_HI} ==")
w_quad = np.empty(M_HI - M_LO + 1, dtype=np.int32)
for i, m in enumerate(range(M_LO, M_HI + 1)):
    sm = -T(m - 1)
    w_quad[i] = mouth_width(m, lambda p, sm=sm: sm % p or p)
    if (i + 1) % 5000 == 0:
        print(f"  quad: {i+1}/{len(w_quad)}", flush=True)

# ---- iid model ----
print(f"\n== iid model: {N_IID} independent draws ==")
rng = np.random.default_rng(7)
w_iid = np.empty(N_IID, dtype=np.int32)
for i in range(N_IID):
    m = rng.integers(M_LO, M_HI + 1)   # same arc-set distribution as quad
    sm = -T(m - 1)                     # unused; offsets drawn fresh below
    cache = {}
    def off(p, cache=cache, rng=rng):
        if p not in cache:
            cache[p] = int(rng.integers(1, p + 1))
        return cache[p]
    w_iid[i] = mouth_width(m, off)
    if (i + 1) % 5000 == 0:
        print(f"  iid: {i+1}/{N_IID}", flush=True)

def report(name, w):
    qs = np.percentile(w, [50, 90, 95, 99, 99.9])
    print(f"{name}: n={len(w)} median={qs[0]:.0f} p90={qs[1]:.0f} p95={qs[2]:.0f} "
          f"p99={qs[3]:.0f} p99.9={qs[4]:.0f} max={w.max()} "
          f"clip={(w > KMAX).mean():.5f}")

print()
report("QUAD (stagger field)", w_quad)
report("IID  (independent laps)", w_iid)

print("\nw : P_quad(W>=w)  P_iid(W>=w)  ratio")
for w in [5, 10, 20, 50, 100, 200, 400, 800, 1600]:
    pq = float((w_quad >= w).mean()); pi = float((w_iid >= w).mean())
    r = pq / pi if pi > 0 else float('inf')
    print(f"{w:5d}: {pq:9.5f}   {pi:9.5f}   {r:8.3f}")

sq = np.sort(w_quad); si = np.sort(w_iid)
xs = np.sort(np.concatenate([sq, si]))
cq = np.searchsorted(sq, xs, side='right') / len(sq)
ci = np.searchsorted(si, xs, side='right') / len(si)
print(f"\nmax |CDF_quad - CDF_iid| = {np.abs(cq - ci).max():.4f}")

np.save("logs/stagger_mc_quad.npy", w_quad)
np.save("logs/stagger_mc_iid.npy", w_iid)
print("saved logs/stagger_mc_{quad,iid}.npy")
