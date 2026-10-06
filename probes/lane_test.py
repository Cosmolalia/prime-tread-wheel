"""
lane_test.py: the two lanes at the wheel's junction at 1.

Closing tick of layer L holds L(L+1)/2: always composite except 3 (dead lane).
First tick of each new layer holds L(L+1)/2 + 1: a quadratic that wheels 3, 5, 13 never block.
The seat count (product over gears of (1 - blocked/p)/(1 - 1/p)) predicts its prime rate.

Result to check: up to layer 100,000 it lands on a prime 9,863 times; seats predict 9,836; a random
number that size would give about 4,986. Twice as rich as chance.
"""
import math
from primes_util import is_prime, primes_up_to

N = 100_000
f = lambda L: L * (L - 1) // 2 + 1        # first number on layer L  (= (L^2 - L + 2)/2)
count = sum(1 for L in range(2, N + 1) if is_prime(f(L)))
C = 1.0
for p in primes_up_to(2_000_000)[1:]:     # odd gears; gear 2 contributes a factor of 1
    if p == 7: w = 1
    else: w = 1 + (1 if pow((-7) % p, (p - 1) // 2, p) == 1 else -1)   # seats where L^2 - L + 2 = 0 mod p
    C *= (1 - w / p) / (1 - 1 / p)
naive = sum(1 / math.log(f(L)) for L in range(2, N + 1))
print(f"first-tick lane up to layer {N:,}: primes {count:,} | seats predict {C*naive:,.0f} | chance {naive:,.0f} | boost {C:.3f}x")
for p in (3, 5, 7, 11, 13):
    print(f"  gear {p:>2} blocks seats: {sorted({L % p for L in range(p) if f(L) % p == 0})}")
