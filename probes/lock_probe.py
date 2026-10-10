#!/usr/bin/env python3
"""
lock_probe.py — Claude's challenge: which of the 1:1 "lock" facts survive at
other ratios (esp. 2:3, 3:4)?

Wheel rules (mirror variable.html):
  L[m] = round(m * a/b)      ticks on lap m      (Math.round = floor(x+0.5))
  B[m] = sum_{j<m} L[j]      base of lap m
  N    = B[m] + k            value at tick k of lap m, angle frac = k / L[m]

Facts tested per ratio:
  F1 seam closure   : fraction of laps with B[m] % L[m] == 0 (lap starts at the seam)
                      + seam primality (N_seam = B[m]+L[m] = B[m+1])
  F2 dead rays      : families (f=j/48, offset -16..+4) with >=600 samples, 0 primes
  F3 parity escape  : density ratio in forced-odd (m%4, k-parity) classes vs baseline
  F4 primes/spoke   : max primes landing on a single exact ray (f=j/96, off 0)
  F5 residue lock   : circular concentration R of frac positions of multiples of q
                      (R~1 = class sits on fixed spokes; R~0 = smeared)
  F6 (r=2 only)     : squares at frac 1/2 (k=m), Ulam offsets k=m+c -> N=m^2+c,
                      k=2m+c -> N=m(m+1)+c, Euler n^2-n+41 = fixed tick k=41
"""
import numpy as np
from math import gcd

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
        L[m] = int(a * m / b + 0.5)          # JS Math.round semantics
        B[m] = B[m - 1] + L[m - 1]
        if B[m] > LIMIT and m > 50: break
    return L, B, m

def test_ratio(a, b, label):
    L, B, M = build(a, b)
    print(f"\n=== r = {label} ({a}/{b}), laps to N<={LIMIT}: {M} ===")

    # F1: seam closure (start at seam OR half-turn = "clean lap") + start-phase spread + seam primality
    closed = sum(1 for m in range(2, min(M, 2000) + 1)
                 if L[m] and (2 * B[m]) % L[m] == 0)
    phases = {}
    for m in range(2, 500):
        if L[m]: phases[(24 * B[m] // L[m]) % 24] = phases.get((24 * B[m] // L[m]) % 24, 0) + 1
    seam_primes = []
    for m in range(2, M + 1):
        N = B[m] + L[m]
        if N > LIMIT: break
        if SIEVE[N]: seam_primes.append((m, N))
    print(f" F1 clean laps (seam or half-turn): {closed}/{min(M,2000)} | "
          f"distinct start phases: {len(phases)} | seam primes: {len(seam_primes)} {seam_primes[:3]}")

    # F2: dead rays, split by m % 12 class (dead lines at rational r are quasi-periodic)
    dead, fams = 0, 0
    examples = []
    for j in range(0, 48):
        f = j / 48
        for off in range(-16, 5):
            for cls in range(12):
                n, p = 0, 0
                for m in range(max(50, cls), M + 1, 12):
                    Lm = L[m]
                    k = int(f * Lm + 0.5) + off
                    if 1 <= k <= Lm:
                        N = B[m] + k
                        if N <= LIMIT:
                            n += 1; p += SIEVE[N]
                if n >= 150:
                    fams += 1
                    if p == 0:
                        dead += 1
                        if len(examples) < 3: examples.append((round(f,4), off, f"m%12={cls}", n))
    print(f" F2 dead rays (m%12-split): {dead}/{fams} families with >=150 samples | e.g. {examples}")

    # F3: parity escape in forced-odd classes
    base_total = base_p = 0
    cls = {}
    for m in range(10, M + 1):
        Lm, Bm = L[m], B[m]
        if Bm + 1 > LIMIT: break
        ks = np.arange(1, Lm + 1)
        Ns = Bm + ks
        ok = Ns <= LIMIT
        Ns, ks = Ns[ok], ks[ok]
        pr = SIEVE[Ns]
        base_total += len(Ns); base_p += pr.sum()
        for mp4 in range(4):
            sel = (m % 4 == mp4)
            if not sel: continue
            for kp in (0, 1):
                s = ks % 2 == kp
                key = (mp4, kp)
                t, p = cls.get(key, (0, 0))
                cls[key] = (t + s.sum(), p + pr[s].sum())
    baseline = base_p / max(1, base_total)
    hits = []
    for (mp4, kp), (t, p) in sorted(cls.items()):
        if t >= 2000:
            r_ = (p / t) / baseline
            hits.append((f"m%4={mp4} k{'odd' if kp else 'even'}", f"{p/t:.4f}", f"{r_:.2f}x"))
    print(f" F3 parity escape (baseline {baseline:.4f}):")
    for h in hits: print(f"    {h[0]}: density {h[1]} ratio {h[2]}")

    # F4: max primes on one exact ray
    best = []
    for j in range(0, 96):
        f = j / 96
        p = 0
        for m in range(50, M + 1):
            Lm = L[m]
            k = int(f * Lm + 0.5)
            if 1 <= k <= Lm:
                N = B[m] + k
                if N <= LIMIT: p += SIEVE[N]
        best.append((p, f))
    best.sort(reverse=True)
    print(f" F4 primes/exact-ray: max {best[0][0]} (f={best[0][1]:.4f}), "
          f"median {sorted(p for p,_ in best)[len(best)//2]}")

    # F5: residue lock (multiples of 3) — circular concentration of frac positions
    for q in (3,):
        zs = []
        for m in range(200, 600):
            Lm, Bm = L[m], B[m]
            if Bm + Lm > LIMIT: break
            ks = np.arange(1, Lm + 1)
            Ns = Bm + ks
            sel = (Ns % q == 0) & (Ns <= LIMIT)
            zs.append(np.exp(2j * np.pi * ks[sel] / Lm))
        z = np.concatenate(zs) if zs else np.zeros(1)
        R = abs(z.sum()) / max(1, len(z))
        print(f" F5 multiples-of-{q} frac concentration R = {R:.3f}  (1.0=locked spokes, 0=smeared)")

def specials_r2():
    print("\n=== r = 2 special-structure verification ===")
    a, b = 2, 1
    L, B, M = build(a, b, 3000)
    # squares at k=m -> N = m(m-1)+m = m^2, frac = 1/2
    sq = [(m, B[m] + m) for m in range(2, 2000) if B[m] + m <= LIMIT]
    print(f" squares: k=m on every lap, N=m^2, frac exactly 1/2 — e.g. {sq[9]}, {sq[14]}")
    # Ulam diagonals as constant seam offsets
    for c in (41,):
        fam1 = sum(1 for m in range(0, 300) if m * m + c <= LIMIT and SIEVE[m * m + c])   # k=m+c
        fam2 = sum(1 for m in range(0, 300) if m * (m + 1) + c <= LIMIT and SIEVE[m * (m + 1) + c])  # k=2m+c
        print(f" Ulam offsets c={c}: N=m^2+{c} primes m<300: {fam1}/300 | N=m(m+1)+{c}: {fam2}/300")
    # Euler n^2-n+41 = fixed tick k=41
    eu = [m for m in range(1, 60) if m * (m - 1) + 41 <= LIMIT and SIEVE[m * (m - 1) + 41]]
    run = 1
    while run in eu: run += 1
    print(f" Euler n^2-n+41 as fixed tick k=41 at r=2: consecutive primes m = 1..{run-1} (theorem says 40; breaks at {run})")
    # frac drift of the Euler tick: 41/(2m) — spiral converging to the seam
    print(f"   its frac at laps m=21,41,101: {41/42:.3f}, {41/82:.3f}, {41/202:.3f} → spirals into the square ray")

print("LOCK PROBE — which 1:1 facts survive at other ratios")
for a, b, label in [(1,1,"1:1 control"), (2,3,"2:3"), (3,4,"3:4"), (4,3,"4:3"), (3,2,"3:2"),
                    (5,3,"5:3"), (5,2,"5:2"), (7,4,"7:4"), (3,5,"3:5"), (2,1,"2:1"),
                    (3,1,"3:1"), (10**6,1,"1000000:1"), (1,10**6,"1:1000000")]:
    test_ratio(a, b, label)
specials_r2()
print("\nDONE")
