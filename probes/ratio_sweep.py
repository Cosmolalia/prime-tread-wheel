#!/usr/bin/env python3
"""
ratio_sweep.py — scan ratio space for persistent prime structure on the variable tread.

Wheel rules (mirroring variable.html): lap m lays L[m] = max(1, round(m*r)) ticks;
tick k of lap m is the integer N = base(m)+k where base(m) = sum_{j<m} L[j].
A "line" is a family k = round(f*L[m]) + b for fixed screen fraction f and offset b:
  f=1, b=0 is the seam column (N = base(m+1), the cumulative totals);
  r=1, f=1, b=-T(j) are the proven pure-dead diagonal lines (triangular-offset theorem).

Calls written BEFORE running:
  C1  all-prime families: any family with >= 8 samples and 100% prime?
      (theorem heuristic: at rational r, N(m) is a quadratic quasi-polynomial;
       a nonconstant polynomial sequence takes composite values — expect ZERO everywhere)
  C2  pure-dead families: 0 primes over >= 40 samples with baseline expectation >= 4.
      PREDICT: present at every rational a/b (quasi-polynomial structure survives),
      absent at irrational r. r=1 must reproduce b = -1,-3,-6,-10,-15 at f=1.
  C3  parity-split dead lines: families dead on exactly one m-mod-2 class.
  C4  enrichment: (m mod 4) x (k mod 2) classes with density >= 2x baseline.
      r=1 must reproduce the parity escape: m = 2 mod 4 x even k ~ 2x.
  C5  seam: how often is base(m+1) prime, per ratio.
"""
import numpy as np
from math import gcd, log
from fractions import Fraction

LIMIT = 5_000_000
sieve = np.ones(LIMIT + 1, dtype=bool)
sieve[:2] = False
for p in range(2, int(LIMIT ** 0.5) + 1):
    if sieve[p]:
        sieve[p * p::p] = False

def build(r, m_cap):
    """lap tables truncated so base stays inside the sieve."""
    L = np.ones(m_cap + 2, dtype=np.int64)
    base = np.zeros(m_cap + 2, dtype=np.int64)
    run = 0
    M = 0
    for m in range(1, m_cap + 1):
        L[m] = max(1, int(round(m * r)))
        base[m] = run
        run += L[m]
        if run > LIMIT - L[m] - 2:
            M = m
            break
    else:
        M = m_cap
    return L[:M+1], base[:M+1], M

# ---------------- ratio set ----------------
rats = {}
for a in range(1, 17):
    for b in range(1, 17):
        if gcd(a, b) == 1:
            rats[Fraction(a, b)] = f"{a}:{b}"
for tag, val in [("sqrt2", 2**0.5), ("sqrt3", 3**0.5), ("sqrt5", 5**0.5),
                 ("pi", 3.141592653589793), ("e", 2.718281828459045),
                 ("phi", (1+5**0.5)/2), ("ln2", 0.6931471805599453),
                 ("sqrt2-1", 2**0.5 - 1),
                 ("1e2", 1e2), ("1e3", 1e3), ("1e4", 1e4), ("1e6", 1e6),
                 ("1e-2", 1e-2), ("1e-3", 1e-3), ("1e-4", 1e-4), ("1e-6", 1e-6)]:
    rats[Fraction(val).limit_denominator(10**12)] = tag

Fs = np.array([j/48 for j in range(1, 49)])
Bs = list(range(-20, 9))
M0 = 8  # skip small-lap noise

all_prime, dead, split_dead, enrichment, seam = [], [], [], [], []

for rf, tag in sorted(rats.items(), key=lambda kv: float(kv[0])):
    r = float(rf)
    L, base, M = build(r, 4000)
    if M - M0 < 60:
        print(f"SKIP {tag} (r={r:g}): only {M} laps in sieve range")
        continue
    baseline = sieve[base[M0]:base[M]+L[M]+1].mean()
    # C5: seam — cumulative totals
    seam_N = base[2:M+1] + L[2:M+1]
    seam.append((tag, r, int(sieve[seam_N].sum()), len(seam_N)))
    # family scans: N = base + round(f*L) + b, vectorized over f
    k0 = np.rint(Fs[None, :] * L[:, None]).astype(np.int64)  # M x 48
    for b in Bs:
        k = k0 + b
        valid = (k >= 1) & (k <= L[:, None])
        kc = np.clip(k, 1, L[:, None])
        N = base[:, None] + kc
        prime = sieve[N] & valid
        n_samples = valid[M0:].sum(axis=0)
        n_primes = prime[M0:].sum(axis=0)
        for fi, f in enumerate(Fs):
            ns, npr = int(n_samples[fi]), int(n_primes[fi])
            if ns < 8:
                continue
            if npr == ns:
                all_prime.append((tag, r, float(f), b, ns))
            if npr == 0 and ns >= 40 and ns * baseline >= 4:
                # C3: split by m parity / m mod 4
                mm = np.arange(M + 1)
                v = valid[:, fi]; pr = prime[:, fi]
                dead_classes = []
                for mod in (2, 4):
                    cls = [((mm % mod) == c) & v for c in range(mod)]
                    if all(int(pr[c][M0:].sum()) == 0 and int(c[M0:].sum()) >= 20 for c in cls if int(c[M0:].sum()) > 0) and sum(int(c[M0:].sum()) for c in cls) >= 40:
                        dead_classes.append(f"all m mod {mod}")
                split = ""
                if len(dead_classes) != 1:  # exactly one mod-class dead => interesting split
                    for mod in (2, 4):
                        for c in range(mod):
                            sel = ((mm % mod) == c) & v
                            nsel = int(sel[M0:].sum())
                            if nsel >= 20 and int(pr[sel][M0:].sum()) == 0 and ns - nsel >= 20 and ns >= 60:
                                split = f"m%{mod}=={c} dead ({nsel}/{ns} samples)"
                dead.append((tag, r, float(f), b, ns, split))
    # C4: enrichment by (m mod 4) x (k mod 2)
    mm = np.arange(1, M + 1)
    for c4 in range(4):
        for kp in range(2):
            sel = (mm % 4 == c4)
            if sel.sum() < 10:
                continue
            tot = pr_ = 0
            for m in mm[sel]:
                Lm = int(L[m]); bm = int(base[m])
                ks = np.arange(1 + kp, Lm + 1, 2)
                if len(ks) == 0:
                    continue
                Ns = bm + ks
                tot += len(Ns); pr_ += int(sieve[Ns].sum())
            if tot >= 2000 and baseline > 0 and pr_ / tot >= 2 * baseline:
                enrichment.append((tag, r, c4, kp, tot, pr_ / tot, baseline))

print(f"\n=== C1: all-prime families (>=8 samples, 100% prime) — theorem expects ZERO ===")
print(all_prime if all_prime else "  NONE — as obstructed")
print(f"\n=== C2/C3: pure-dead families (0 primes, >=40 samples, expected>=4) ===")
for tag, r, f, b, ns, split in dead:
    print(f"  r={tag:>8} ({r:>10.6g})  f={f:.4f} b={b:+d}  n={ns:4d}  {split}")
print(f"\n=== C4: enrichment >= 2x baseline, class ticks >= 2000 ===")
for tag, r, c4, kp, tot, d, bl in enrichment:
    print(f"  r={tag:>8} ({r:>10.6g})  m%4=={c4} k%2=={kp}  n={tot:6d}  density={d:.4f} vs {bl:.4f}  ({d/bl:.2f}x)")
print(f"\n=== C5: seam (cumulative totals base(m+1)) prime counts, out of M-1 ===")
for tag, r, pr, n in seam:
    print(f"  r={tag:>8} ({r:>10.6g})  {pr}/{n}")
