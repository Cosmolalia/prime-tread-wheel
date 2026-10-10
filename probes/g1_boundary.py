#!/usr/bin/env python3
"""
g1_boundary.py — G1: is the full 1:1 lock (dead seam + exactly-2.00x parity
escape) conditioned on the denominator being a POWER OF 2, or merely EVEN?

The 13-ratio lock probe found full lock at denominators 1, 2, 4 and diluted
lock at odd denominators. Two competing laws fit that sample:

  L_pow2 : full lock  <=>  b is a power of two            (1:6, 5:12 predict DILUTED)
  L_even : full lock  <=>  b is even (v2(b) >= 1)         (1:6, 5:12 predict FULL)

Mechanism sketch for why odd factors matter: B[m] = sum round(j*a/b) is a
quasi-polynomial whose fluctuation term has period b. The parity escape at full
strength needs B[m] mod 2 to be a clean function of m mod 4. An odd factor q|b
injects a period-q component into B[m] mod 2, which no refinement of m mod 4
can absorb -> the escape classes split and dilute. Powers of two are the only
denominators whose period is 2^k, compatible with a mod-4 (or mod-2^k) law.

Discriminating set: denominators 6, 10, 12, 14 (even, odd part > 1) sit
exactly between the two laws. 8 and 16 confirm the power-of-2 side upward.
"""
import numpy as np

LIMIT = 5_000_000

def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    s[4::2] = False
    for p in range(3, int(n ** 0.5) + 1, 2):
        if s[p]: s[p*p::2*p] = False
    return s

SIEVE = sieve(LIMIT)

def build(a, b, MAXM=6000):
    L = [0] * (MAXM + 2); B = [0] * (MAXM + 2)
    for m in range(1, MAXM + 2):
        L[m] = int(a * m / b + 0.5)
        B[m] = B[m - 1] + L[m - 1]
        if B[m] > LIMIT and m > 50: break
    return L, B, m

def test(a, b, label):
    L, B, M = build(a, b)
    # clean-lap fraction over first 3000 laps
    closed = sum(1 for m in range(2, min(M, 3000) + 1) if L[m] and (2 * B[m]) % L[m] == 0)
    # seam primes
    seam_primes = []
    for m in range(2, M + 1):
        N = B[m] + L[m]
        if N > LIMIT: break
        if SIEVE[N]: seam_primes.append((m, N))
    # parity escape per (m%4, k-parity) class
    base_t = base_p = 0
    cls = {}
    for m in range(10, M + 1):
        Lm, Bm = L[m], B[m]
        if Bm + 1 > LIMIT: break
        ks = np.arange(1, Lm + 1)
        Ns = Bm + ks
        ok = Ns <= LIMIT
        Ns, ks = Ns[ok], ks[ok]
        if len(Ns) == 0: continue
        pr = SIEVE[Ns]
        base_t += len(Ns); base_p += pr.sum()
        for mp4 in range(4):
            if m % 4 != mp4: continue
            for kp in (0, 1):
                s = ks % 2 == kp
                t, p = cls.get((mp4, kp), (0, 0))
                cls[(mp4, kp)] = (t + int(s.sum()), p + int(pr[s].sum()))
    baseline = base_p / max(1, base_t)
    odd_dens = {mp4: (cls[(mp4,1)][1] / cls[(mp4,1)][0]) for mp4 in range(4) if cls[(mp4,1)][0] > 500}
    ratios = {mp4: d / baseline for mp4, d in odd_dens.items()}
    full = sorted(ratios.values())
    # verdict: FULL lock = two m%4 classes near 2.00x and two near 0
    near2 = sum(1 for v in ratios.values() if 1.7 <= v <= 2.3)
    near0 = sum(1 for v in ratios.values() if v <= 0.05)
    verdict = "FULL LOCK" if (near2 == 2 and near0 == 2) else \
              ("diluted" if near2 == 0 else "partial/intermediate")
    print(f"\nr = {label:<12} ({a}/{b})  clean laps {closed}/{min(M,3000)}  seam primes: {len(seam_primes)} {seam_primes[:2]}")
    print(f"   baseline {baseline:.4f} | odd-k density by m%4: " +
          " ".join(f"{mp4}:{odd_dens[mp4]:.4f}({ratios[mp4]:.2f}x)" for mp4 in sorted(odd_dens)))
    print(f"   -> {verdict}")

print("G1 — the power-of-2 boundary:  full lock <=> denominator is a power of 2?")
print("=" * 78)
groups = [
    ("power-of-2 denominators (predict FULL)", [(1,2,"1:2"), (3,8,"3:8"), (5,8,"5:8"), (7,8,"7:8"), (1,16,"1:16"), (3,16,"3:16")]),
    ("even, odd part > 1 (DISCRIMINATING: pow2 says diluted, even says full)", [(1,6,"1:6"), (5,6,"5:6"), (3,10,"3:10"), (7,10,"7:10"), (5,12,"5:12"), (1,14,"1:14")]),
    ("odd denominators (control: both laws predict diluted)", [(2,3,"2:3"), (4,5,"4:5"), (2,7,"2:7")]),
]
for gname, rs in groups:
    print(f"\n### {gname}")
    for a, b, label in rs:
        test(a, b, label)
print("\nDONE")
