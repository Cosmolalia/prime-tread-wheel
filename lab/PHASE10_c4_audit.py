#!/usr/bin/env python3
"""
PHASE 10 — independent audit of GPT-6's C4 closure claim.

Claim under test (relay 2026-10-11): C4's 0.62x anti-correlation vs the probe's
flat null is a null-model artifact. Exact reduction [F, verified analytically
against probes/column_law.py]: for a source prime N = T(m-1)+k the C4 window
|k' - k(m+1)/m| <= 1.0001 contains exactly ticks {k, k+1}; their values are
N+m and N+m+1; exactly one is odd, so C4 == census of prime pairs (N, N+d(m))
with d(m) = m + (m mod 2) = 2*ceil(m/2). HL expectation per source:
S(d)/ln(N+d), S(d) = 2*C2 * prod_{p|d, p>2} (p-1)/(p-2).

CONVENTIONS (stated before running, per house rule):
  - Source: eligible(k,m) AND prime, k in 1..m, same predicate as column_law.py:50.
  - Hit: target value N + d(m) prime (the other candidate is even > 2).
  - Range A (reproduce): m = 3..2999 (the probe's C4 loop range).
  - Range B (out-of-sample): m = 3000..9999, formula untouched.
  - Original null reproduced: rate_next = eligible-prime/eligible at layer m+1,
    expected += rate_next * |window|, |window| = 2 (verified arithmetically).
  - Parity null: rate over odd-VALUE eligible ticks at layer m+1, one draw.
  - HL: sum over sources of S(d(m))/ln(N+d); C2 = 0.6601618158468696.
Independent implementation: single bytearray sieve + numpy; no sympy, no GPT code.
"""
import json
import numpy as np
from math import isqrt, log

C2 = 0.6601618158468696
M_MAX = 10000
LIMIT = (M_MAX - 1) * M_MAX // 2 + M_MAX + M_MAX + 16  # T(9999) + k + d headroom

print(f"sieving to {LIMIT:,} ...", flush=True)
comp = bytearray(LIMIT)
comp[0] = comp[1] = 1
for p in range(2, isqrt(LIMIT) + 1):
    if not comp[p]:
        comp[p * p::p] = b'\x01' * (((LIMIT - 1 - p * p) // p) + 1)
COMP = np.frombuffer(comp, dtype=np.uint8)


def eligible_mask(ks, m):
    g = np.gcd(ks, m)
    return (g == 1) | ((g == 2) & (m % 4 == 2))


# --- pre-pass: per-layer eligible stats (also odd-value subsets) ---
print("layer pre-pass ...", flush=True)
ELIG_N = np.zeros(M_MAX + 2, dtype=np.int64)   # eligible tick count
ELIG_P = np.zeros(M_MAX + 2, dtype=np.int64)   # eligible primes
ODD_N = np.zeros(M_MAX + 2, dtype=np.int64)    # odd-value eligible ticks
ODD_P = np.zeros(M_MAX + 2, dtype=np.int64)    # odd-value eligible primes
for m in range(2, M_MAX + 2):
    base = (m - 1) * m // 2
    ks = np.arange(1, m + 1, dtype=np.int64)
    e = eligible_mask(ks, m)
    vals = base + ks
    ELIG_N[m] = int(np.count_nonzero(e))
    ELIG_P[m] = int(np.count_nonzero(e & (COMP[vals] == 0)))
    odd = e & ((vals & 1) == 1)
    ODD_N[m] = int(np.count_nonzero(odd))
    ODD_P[m] = int(np.count_nonzero(odd & (COMP[vals] == 0)))


def singular(d, cache={}):
    if d in cache:
        return cache[d]
    s = 2 * C2
    x = d // 2 if d % 2 == 0 else d   # factor 2 excluded from product but divided out
    while x % 2 == 0:
        x //= 2
    p = 3
    while p * p <= x:
        if x % p == 0:
            s *= (p - 1) / (p - 2)
            while x % p == 0:
                x //= p
        p += 2
    if x > 1:  # single remaining prime factor
        s *= (x - 1) / (x - 2)
    cache[d] = s
    return s


def run(lo, hi):
    """C4 census on source layers m = lo..hi-1 (probe convention: range(lo, hi))."""
    obs = 0
    src_total = 0
    exp_orig = 0.0
    exp_parity = 0.0
    exp_hl = 0.0
    win_total = 0
    by_m4 = {0: [0, 0.0], 1: [0, 0.0], 2: [0, 0.0], 3: [0, 0.0]}
    by_d3 = {0: 0, 1: 0, 2: 0}
    hl_by_m3 = {0: [0, 0.0], 1: [0, 0.0], 2: [0, 0.0]}
    for m in range(lo, hi):
        base = (m - 1) * m // 2
        ks = np.arange(1, m + 1, dtype=np.int64)
        e = eligible_mask(ks, m)
        vals = base + ks
        src = np.where(e & (COMP[vals] == 0))[0]  # indices; k = idx+1
        n_src = len(src)
        if n_src == 0:
            continue
        d = m + (m % 2)
        sv = vals[src]                 # source prime values
        hits = COMP[sv + d] == 0
        obs += int(np.count_nonzero(hits))
        src_total += n_src
        # window-size audit (arithmetical identity expected = 2 per source)
        win_total += 2 * n_src
        # original null
        rate = ELIG_P[m + 1] / max(1, ELIG_N[m + 1])
        exp_orig += rate * 2 * n_src
        # parity null
        prate = ODD_P[m + 1] / max(1, ODD_N[m + 1])
        exp_parity += prate * n_src
        # HL
        S = singular(d)
        e_hl = S * float(np.sum(1.0 / np.log((sv + d).astype(np.float64))))
        exp_hl += e_hl
        by_m4[m % 4][0] += int(np.count_nonzero(hits))
        by_m4[m % 4][1] += e_hl
        by_d3[d % 3] += int(np.count_nonzero(hits))
        for r in (0, 1, 2):
            sub = (sv % 3 == r)
            hl_by_m3[r][0] += int(np.count_nonzero(hits & sub))
            hl_by_m3[r][1] += S * float(np.sum(1.0 / np.log((sv[sub] + d).astype(np.float64))))
    return dict(src=src_total, obs=obs, exp_orig=exp_orig, exp_parity=exp_parity,
                exp_hl=exp_hl, by_m4=by_m4, by_d3=by_d3, hl_by_m3=hl_by_m3)


print("range A: m = 3..2999 ...", flush=True)
A = run(3, 3000)
print("range B: m = 3000..9999 ...", flush=True)
B_full = run(3000, 10000)
print("range B sub-windows ...", flush=True)
B1 = run(3000, 5000)
B2 = run(5000, 7500)
B3 = run(7500, 10000)


def show(tag, r):
    print(f"\n[{tag}] source primes: {r['src']:,}")
    print(f"  observed hits            : {r['obs']:,}")
    print(f"  original flat null       : {r['exp_orig']:,.1f}  ratio {r['obs']/r['exp_orig']:.4f}")
    print(f"  parity-restricted null   : {r['exp_parity']:,.1f}  ratio {r['obs']/r['exp_parity']:.4f}")
    print(f"  HL singular series       : {r['exp_hl']:,.1f}  ratio {r['obs']/r['exp_hl']:.5f}")
    print(f"  m mod 4 strata (obs / HL / ratio):")
    for q in (0, 1, 2, 3):
        o, e = r['by_m4'][q]
        print(f"    m%{4}={q}: {o:,} / {e:,.1f} / {o/e:.4f}" if e else f"    m%{4}={q}: {o:,} / 0")
    print(f"  d mod 3 observed hits: {r['by_d3']}")
    print(f"  source-value mod 3 strata (obs / HL / ratio):")
    for q in (0, 1, 2):
        o, e = r['hl_by_m3'][q]
        if e > 0:
            print(f"    N%{3}={q}: {o:,} / {e:,.1f} / {o/e:.4f}")
        else:
            print(f"    N%{3}={q}: {o:,} / 0 (no sources; primes > 3 are never 0 mod 3)")


show("A: 3..2999 (reproduction)", A)
show("B: 3000..9999 (out-of-sample)", B_full)
for tag, r in (("B1: 3000..4999", B1), ("B2: 5000..7499", B2), ("B3: 7500..9999", B3)):
    print(f"\n[{tag}] obs {r['obs']:,} / HL {r['exp_hl']:,.2f} = {r['obs']/r['exp_hl']:.5f}")

with open('lab/PHASE10_c4_audit.json', 'w') as f:
    json.dump({'A': A, 'B': B_full, 'B1': B1, 'B2': B2, 'B3': B3}, f, indent=1)
print("\nwrote lab/PHASE10_c4_audit.json")
