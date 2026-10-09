"""The first odd after each seam: total+1 when the layer total T(m-1) is even ("n2+1"),
total+2 when it is odd ("n1+2"). How often is it prime, against a random odd of the same size?"""
import math
import numpy as np
from primes_util import is_prime, sieve

T = lambda m: m * (m + 1) // 2
M = 200_000
stats = {1: [0, 0.0, 0], 2: [0, 0.0, 0]}      # route: [primes, expected for random odds, layers]
first_gap = []
for m in range(3, M + 1):
    tot = T(m - 1)
    c = 1 if tot % 2 == 0 else 2
    f = tot + c
    s = stats[c]
    s[2] += 1
    s[1] += 2 / math.log(f)
    if is_prime(f):
        s[0] += 1
for c, (pr, exp, n) in stats.items():
    print(f"route total+{c}: {n} layers, {pr} primes, random odds would give {exp:.0f}  -> {pr/exp:.2f}x  ({pr/n:.1%} of those layers)")
allp = stats[1][0] + stats[2][0]; alle = stats[1][1] + stats[2][1]; alln = stats[1][2] + stats[2][2]
print(f"both routes: {allp/alle:.2f}x a random odd; prime on {allp/alln:.1%} of layers 3..{M}")

# Bateman-Horn style constant for each lane: odd primes only (p=2 handled by taking the odd members)
PR = [int(p) for p in np.nonzero(sieve(3_000_000))[0] if p > 2]
def boost(c):
    D = 1 - 8 * c
    C = 1.0
    for p in PR:
        w = 1 if D % p == 0 else 1 + (1 if pow(D % p, (p - 1) // 2, p) == 1 else -1)
        C *= (1 - w / p) / (1 - 1 / p)
    return C
print(f"predicted boost: total+1 lane {boost(1):.3f}, total+2 lane {boost(2):.3f}")
never = lambda c, n: [p for p in PR[:n] if (1 - 8 * c) % p and pow((1 - 8 * c) % p, (p - 1) // 2, p) != 1]
print("gears that can never land on total+1:", never(1, 14))
print("gears that can never land on total+2:", never(2, 14))

# how far past the seam is the first prime of each layer, as a share of the layer (layers 100..20000)
IS = sieve(T(20000) + 10)
worst, tot_share, cnt, wm = 0.0, 0.0, 0, None
for m in range(100, 20001):
    lo, hi = T(m - 1) + 1, T(m)
    idx = np.flatnonzero(IS[lo:hi + 1])
    d = int(idx[0]) + 1
    share = d / m
    tot_share += share; cnt += 1
    if share > worst: worst, wm = share, m
print(f"first prime of each layer, layers 100..20000: on average {tot_share/cnt:.1%} of the way in; worst {worst:.1%} (layer {wm})")
