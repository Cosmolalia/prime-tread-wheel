"""P5 check: composites flagged by the wheel's own geometry on each number's layer, no division of x:
   the mirror (x even, past 2) and the visit lock (visit number g = gcd(tick, layer): g odd >= 3, or g even >= 4)."""
import numpy as np
from math import gcd
from primes_util import sieve
M = 2000
T = lambda m: m * (m + 1) // 2
IS = sieve(T(M) + 10)
comp = flag = by_mirror = by_visit = primes_flagged = 0
for m in range(3, M + 1):
    k = np.arange(1, m + 1, dtype=np.int64)
    x = T(m - 1) + k
    g = np.gcd(k, m)
    mirror = (x % 2 == 0) & (x > 2)          # parity read off the mirror: steps from the halfway tick
    visit = ((g % 2 == 1) & (g >= 3)) | ((g % 2 == 0) & (g >= 4))
    f = mirror | visit
    isc = ~IS[x]
    comp += int(isc.sum()); flag += int((f & isc).sum())
    by_mirror += int((mirror & isc).sum()); by_visit += int((visit & ~mirror & isc).sum())
    primes_flagged += int((f & IS[x]).sum())
print(f"layers 3..{M}: composites {comp}, flagged by geometry {flag} ({flag/comp:.1%}); "
      f"mirror alone {by_mirror/comp:.1%}, visit lock adds {by_visit/comp:.1%}; primes wrongly flagged: {primes_flagged}")
