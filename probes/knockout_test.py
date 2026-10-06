"""
knockout_test.py: can the wheel's geometry pin a layer's primes with fewer gears than the sieve?

Layer m holds T(m-1)+1 .. T(m), T(m)=m(m+1)/2. Tick k sits at angle k/m.
Visit theorem: a prime can only sit on a fresh tick (gcd(k,m)=1, layers m not = 2 mod 4, plus layer 2)
or on a second visit (gcd=2 with m/2 odd). Those are the layer's "seats".
For each layer, list the gears (smallest prime factors) needed to clear every composite seat.

Finding to check: only about half the gears up to sqrt(top of layer) are ever needed on a layer
(the rest only hit numbers a smaller gear already removed). The same share holds for any interval
that short, so it is not special to the wheel. And the biggest gear needed creeps up to the square
root (98% by layers 2000-3000). No layer stops short of the wall.
"""
import math, statistics as st
from math import gcd

def spf_table(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j: spf[j] = i
    return spf

M = 3000
SPF = spf_table(M * (M + 1) // 2 + 1)
PR = [p for p in range(2, M) if SPF[p] == p]
rows = []
for m in range(10, M + 1):
    base = (m - 1) * m // 2; top = base + m; r = math.isqrt(top)
    seats = [base + k for k in range(1, m + 1)
             if (gcd(k, m) == 1 and m % 4 != 2) or (gcd(k, m) == 2 and (m // 2) % 2 == 1)]
    needed = {SPF[x] for x in seats if SPF[x] != x}
    allp = [p for p in PR if p <= r]
    rows.append((m, len(allp), len(needed), max(needed) / r if needed else 0))
for lo, hi in [(10, 100), (100, 500), (500, 1000), (1000, 2000), (2000, 3001)]:
    sel = [x for x in rows if lo <= x[0] < hi]
    print(f"layers {lo:>4}-{hi-1:<4}: gears to sqrt {st.mean(x[1] for x in sel):6.1f} | needed {st.mean(x[2] for x in sel):6.1f} "
          f"| share {st.mean(x[2]/x[1] for x in sel):.2f} | biggest needed / sqrt {st.mean(x[3] for x in sel):.3f} (lowest {min(x[3] for x in sel):.3f})")
