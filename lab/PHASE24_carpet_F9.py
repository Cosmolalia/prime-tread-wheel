#!/usr/bin/env python3
"""
PHASE 24 — midday-handback executions: F9 carpet edge-tilt at m in [1e4, 2e4],
Claude's three-histogram convention discriminator, and the Grok/GPT pair-count
reconciliation.

Conventions frozen from PHASE9/PHASE22: T(m) = m(m+1)/2; window (T(m-1), T(m)];
pair = p prime, T(m-1) < p <= m^2/2, m^2 - p prime; unordered; m=2 self-pair
included. Singles = window primes in no pair. Relative position
u = (x - T(m-1))/m in (0,1], 24 bins. Both-members convention for paired mass
(each endpoint credited), matching PHASE22's even_all - even_sing histogram.
"""
import numpy as np, math, json, time

T = lambda n: n * (n + 1) // 2

# --- sieve primes up to T(20000) = 200_010_000, odd-only bytearray ---
LIM = T(20000)
half = (LIM + 1) // 2          # index i -> odd number 2i+1
s = bytearray(b"\x01") * half
s[0] = 0                        # 1 is not prime
for i in range(1, int(half ** 0.5) + 1):
    if s[i]:
        v = 2 * i + 1
        start = (v * v - 1) // 2
        s[start::v] = b"\x00" * (((half - 1 - start) // v) + 1)
odd_idx = np.nonzero(np.frombuffer(s, dtype=np.uint8))[0]
primes = np.concatenate(([2], 2 * odd_idx + 1)).astype(np.int64)
print(f"sieved {len(primes)} primes up to {LIM}", flush=True)

# deterministic MR for n < 2^32 (bases 2,7,61); trial divide small primes first
SMALL = primes[primes <= 1000].tolist()
def isprime(n):
    if n < 2: return False
    for p in SMALL:
        if p * p > n: return True
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 7, 61):
        if a % n == 0: continue
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else:
            return False
    return True

# --- pair-count reconciliation over 2 <= m < 3000 under convention variants ---
def count_pairs(mmax, excl_m2=False):
    tot = 0
    for m in range(2 if not excl_m2 else 3, mmax):
        lo, hi = T(m - 1), T(m)
        n = m * m
        i0 = np.searchsorted(primes, lo, side="right")
        for p in primes[i0:]:
            p = int(p)
            if p > hi or p > n // 2:
                break
            if isprime(n - p):
                tot += 1
    return tot

base = count_pairs(3000)
print(f"pair census 2<=m<3000, frozen convention (p <= m^2/2, incl m=2): {base}", flush=True)
print(f"  pairs 2<=m<2000 (reference range): {count_pairs(2000)}", flush=True)
print(f"  excl m=2 self-pair, m<3000: {count_pairs(3000, excl_m2=True)}", flush=True)

# --- histograms for m in [10000, 20000), even layers ---
NB = 24
LO_M, HI_M = 10000, 20000
hist = {k: np.zeros(NB) for k in ("all", "paired", "single",
                                  "allA", "allB", "pairA", "pairB")}
edge_bins = [0, 1, NB - 2, NB - 1]           # outer two each side
edge1_bins = [0, NB - 1]                      # outer one each side
tot_pairs = 0; layers_used = 0
t0 = time.time()
for m in range(LO_M, HI_M):
    if m % 2: continue
    lo, hi = T(m - 1), T(m)
    n = m * m
    i0 = np.searchsorted(primes, lo, side="right")
    i1 = np.searchsorted(primes, hi, side="right")
    pr = primes[i0:i1]
    inpair = set()
    B = 0
    for p in pr[pr <= n // 2]:
        if isprime(n - int(p)):
            B += 1
            inpair.add(int(p)); inpair.add(n - int(p))
    singles = [int(x) for x in pr if int(x) not in inpair]
    assert len(pr) == 2 * B + len(singles)
    tot_pairs += B; layers_used += 1
    halfAB = "A" if m % 2000 < 1000 else "B"
    for x in pr:
        u = (int(x) - lo) / m
        i = min(int(u * NB), NB - 1)
        hist["all"][i] += 1; hist["all" + halfAB][i] += 1
    for x in inpair:
        u = (x - lo) / m
        i = min(int(u * NB), NB - 1)
        hist["paired"][i] += 1; hist["pair" + halfAB][i] += 1
    for x in singles:
        u = (x - lo) / m
        i = min(int(u * NB), NB - 1)
        hist["single"][i] += 1
    if layers_used % 1000 == 0:
        print(f"  ...{layers_used} layers, {time.time()-t0:.0f}s", flush=True)

def report(name, h):
    N = h.sum()
    p = 1.0 / NB
    exp = N * p
    chi2 = ((h - exp) ** 2 / exp).sum()
    # edge tilt: observed edge mass vs expected, multinomial sigma
    for tag, eb in (("edge2", edge_bins), ("edge1", edge1_bins)):
        eo = h[eb].sum(); ee = N * len(eb) * p
        var = N * (len(eb) * p) * (1 - len(eb) * p)
        z = (eo - ee) / math.sqrt(var)
        print(f"  {name:8s} {tag}: edge mass {eo:.0f} vs exp {ee:.0f}  z = {z:+.2f}", flush=True)
    mir = h[::-1]
    l1 = 0.5 * np.abs(h / N - mir / N).sum()
    print(f"  {name:8s} chi2/dof = {chi2/(NB-1):.2f}   mirror-L1 = {l1:.5f}   N = {N:.0f}", flush=True)
    return chi2 / (NB - 1)

print(f"\n=== m in [{LO_M},{HI_M}) even layers: {layers_used} layers, {tot_pairs} pairs ===")
c_all = report("all", hist["all"])
c_pair = report("paired", hist["paired"])
c_sing = report("single", hist["single"])

# split-half noise floors for chi2/dof and edge z
for nm in ("all", "pair"):
    hA, hB = hist[nm + "A"], hist[nm + "B"]
    NA = hA.sum(); NBo = hB.sum(); p = 1.0 / NB
    zA = (hA[edge_bins].sum() - NA * 4 * p) / math.sqrt(NA * 4 * p * (1 - 4 * p))
    zB = (hB[edge_bins].sum() - NBo * 4 * p) / math.sqrt(NBo * 4 * p * (1 - 4 * p))
    print(f"  split-half edge-z {nm}: A {zA:+.2f}  B {zB:+.2f}", flush=True)

# paired-mass per-bin table (carpet check)
N = hist["paired"].sum()
print("\npaired-mass per bin (share of paired N):")
for i in range(NB):
    print(f"  bin {i:2d}: {hist['paired'][i]/N:.4f}")
print(json.dumps({"layers": layers_used, "pairs": tot_pairs,
                  "chi2dof_all": c_all, "chi2dof_pair": c_pair,
                  "chi2dof_single": c_sing}), flush=True)
