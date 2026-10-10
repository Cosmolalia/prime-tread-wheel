#!/usr/bin/env python3
"""
g1b_boundary.py — G1 round 2: resolve the parity escape at its natural
resolution (m mod 4b, not m mod 4) and test seam deadness in the structural
regime (m >= 50), where small-lap noise (L[m] tiny, seam N small) can't
contaminate it.

Round 1 (g1_boundary.py) showed the m%4 split blurs the law: e.g. 3:8 shows a
single 2.00x class at m%4==1, 7:8 shows 2.00x at m%4==1 AND 0.00x at m%4==3.
Guess: every rational has the full-lock pattern once resolved finely enough;
the lock's *resolution* is set by the denominator. Powers of two may still be
special — or the real law may be "full lock at resolution 2b for every b,
but only powers of two fold down to a mod-4 law".
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
    R = min(4 * b, 48)                      # fine resolution for the escape
    # structural seam: m >= 50
    seam = [(m, B[m] + L[m]) for m in range(50, M + 1) if B[m] + L[m] <= LIMIT]
    seam_p = [(m, N) for m, N in seam if SIEVE[N]]
    # escape classes at fine resolution, odd k only
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
        s = ks % 2 == 1
        if not s.any(): continue
        key = m % R
        t, p = cls.get(key, (0, 0))
        cls[key] = (t + int(s.sum()), p + int(pr[s].sum()))
    baseline = base_p / max(1, base_t)
    n2 = n0 = n1 = 0
    det = []
    for key in sorted(cls):
        t, p = cls[key]
        if t < 300: continue
        r_ = (p / t) / baseline
        det.append((key, r_))
        if 1.7 <= r_ <= 2.3: n2 += 1
        elif r_ <= 0.05: n0 += 1
        elif 0.85 <= r_ <= 1.15: n1 += 1
    big = max((N for _, N in seam_p), default=None)
    print(f"\nr = {label:<8} ({a}/{b})  resolution m mod {R}")
    print(f"   seam m>=50: {len(seam_p)}/{len(seam)} prime, largest seam prime N = {big}")
    print(f"   escape classes: {n2} at ~2.00x, {n1} at ~1.00x, {n0} at ~0.00x "
          f"{'-> FULL LOCK at fine resolution' if n0 >= 1 and n2 >= 1 and n2+n1+n0 == len(det) else ''}")
    print("   detail: " + " ".join(f"m%{R}={k}:{r_:.2f}x" for k, r_ in det))

print("G1 round 2 — fine-resolution lock structure")
print("=" * 78)
for a, b, label in [(1,1,"1:1"), (1,2,"1:2"), (3,8,"3:8"), (5,8,"5:8"), (7,8,"7:8"),
                    (1,16,"1:16"), (3,16,"3:16"),
                    (1,6,"1:6"), (5,6,"5:6"), (3,10,"3:10"), (5,12,"5:12"), (1,14,"1:14"),
                    (2,3,"2:3"), (4,5,"4:5"), (2,7,"2:7")]:
    test(a, b, label)
print("\nDONE")
