#!/usr/bin/env python3
"""
g5_sturmian.py — is the irrational-ratio "chaos" aperiodically ordered?

Two sides to test, kept separate:
  SUBSTRATE (geometry): the lap word w[m] = L[m+1]-L[m] for L[m]=round(r*m).
    [E claim from mechanical-word theory]: for irrational r this word is
    Sturmian -> factor complexity p(n) = n+1 exactly.
  CERTIFICATE side (the thing L2's 'structureless' actually refers to):
    at irrational r no dead-line algebra exists (L2, established). The
    remaining question is whether the prime coloring on the substrate
    inherits any of the substrate's order. Test: positions of gold ticks
    along one lap, reduced mod small q — uniform (random coloring) or
    structured (inherited order)?
"""
import numpy as np
from math import gcd

LIMIT = 5_000_000

def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False; s[4::2] = False
    for p in range(3, int(n ** 0.5) + 1, 2):
        if s[p]: s[p*p::2*p] = False
    return s

S = sieve(LIMIT)

def factor_complexity(word, nmax):
    """p(n) = number of distinct length-n factors."""
    out = []
    w = word if isinstance(word, str) else "".join(map(str, word))
    for n in range(1, nmax + 1):
        out.append(len({w[i:i+n] for i in range(len(w) - n + 1)}))
    return out

def lap_word(r, M):
    L = np.floor(r * np.arange(1, M + 1) + 0.5).astype(int)
    return L[1:] - L[:-1]

print("=" * 74)
print("SUBSTRATE — lap-word factor complexity (want p(n)=n+1 iff Sturmian)")
print("=" * 74)
irr = {"sqrt(2)": 2 ** 0.5, "phi": (1 + 5 ** 0.5) / 2, "pi": 3.141592653589793,
       "e": 2.718281828459045}
for name, r in irr.items():
    w = lap_word(r, 3000)
    pc = factor_complexity(w, 12)
    sturmian = all(pc[n - 1] == n + 1 for n in range(1, 13))
    print(f"  r={name:8} word alphabet={sorted(set(w.tolist()))} "
          f"p(1..12)={pc}  Sturmian: {sturmian}")
# rational control: ultimately periodic -> p(n) bounded
for name, r in {"5/3": 5/3, "7/4": 7/4}.items():
    w = lap_word(r, 3000)
    pc = factor_complexity(w, 12)
    print(f"  r={name:8} (rational control) p(1..12)={pc}  bounded as predicted: {pc[-1] < 13}")

print()
print("=" * 74)
print("COLORING — do gold (prime) tick positions inherit substrate order?")
print("=" * 74)
print("Test: on deep laps at r=sqrt(2), distribution of (gold tick index * lap)")
print("mod small q vs uniform; and lag-1 autocorrelation of the gold indicator")
print("along the lap vs the iid null.")
r = 2 ** 0.5
m_cap = int((2 * LIMIT / r) ** 0.5)
print(f"(sieve limit 5M caps us at m ~ {m_cap}; coloring test runs at the deepest reachable laps)")
for m in [m_cap - 12, m_cap - 6, m_cap - 2]:
    B = int(np.floor(r * np.arange(1, m) + 0.5).sum())     # B[m] = sum of lap lengths before m
    Lm = int(r * m + 0.5)
    N = B + np.arange(1, Lm + 1)
    N = N[N <= LIMIT]
    gold = S[N]
    idx = np.arange(1, len(N) + 1)
    # (a) mechanism check: the wheel IS the sieve at irrational ratios too —
    #     every gold tick must avoid k ≡ -B[m] (mod p) for p = 2,3,5,7
    viol = {p: int(((idx % p) == (-B) % p)[gold].sum()) for p in (2, 3, 5, 7)}
    # (b) the chi2 'signal' is forced exclusion: predicted = all mass off the
    #     excluded class. Compare observed vs that forced prediction.
    q = 3
    excl = (-B) % q
    cnt = np.bincount((idx % q)[gold], minlength=q)
    forced = gold.sum() / (q - 1) * np.array([0.0 if i == excl else 1.0 for i in range(q)])
    chi2_forced = (((cnt - forced) ** 2) / np.maximum(forced, 1)).sum()
    # (c) residual order: within parity-allowed k, is there lag-1 structure?
    odd = idx % 2 == 1
    g_odd = gold[odd].astype(float)
    ac_odd = np.corrcoef(g_odd[:-1], g_odd[1:])[0, 1]
    # (d) beyond-sieve uniformity: mod 11 (no forced exclusion below 11 beyond
    #     the CRT-allowed classes) -- test uniformity across the 10 non-excluded
    #     classes vs the one excluded class
    q2 = 11
    ex2 = (-B) % q2
    cnt2 = np.bincount((idx % q2)[gold], minlength=q2)
    allowed = np.array([i != ex2 for i in range(q2)])
    exp2 = gold.sum() / (q2 - 1)
    chi2_11 = ((((cnt2 - exp2) ** 2) / exp2)[allowed]).sum()
    print(f"  m={m}: L={len(N)} primes={gold.sum()} | sieve-law violations p=2,3,5,7: {viol} (want 0s)")
    print(f"      chi2(q=3)={(((cnt-gold.sum()/q)**2/(gold.sum()/q)).sum()):.1f} vs FORCED-exclusion prediction: {chi2_forced:.2f} (match => signal is the sieve itself)")
    print(f"      odd-k-only lag-1 autocorr={ac_odd:+.4f} (parity-removed null ~ 0) | chi2 over allowed classes mod 11 = {chi2_11:.2f} (df 9)")
print()
print("Reading: if (a) shows zero violations and (b)'s chi2 matches the forced")
print("prediction, the residue signal IS the sieve itself — present at every")
print("ratio, ratio-independent (primality is a property of N). Then (c),(d) ask")
print("the only remaining question: order BEYOND the sieve. If odd-k autocorr ~ 0")
print("and mod-11 chi2 is ordinary, the irrational sea is:")
print("  ordered floor (Sturmian substrate), sieve furniture (forced exclusions),")
print("  and no detectable order beyond that at this resolution.")
print("DONE")
