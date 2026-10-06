"""
gear_net.py: a network built by hand whose weights ARE the Prime Tread Wheel's gears. No training.

Layer 1  places each number x on one circle per gear p (cos and sin of 2*pi*x/p): its seat on that gear.
Layer 2  one ReLU switch per gear that fires only at seat 0 (that gear's line passes through x).
Output   "prime" if no switch fired.

Prediction: exact up to (largest gear)^2, then it never misses a prime but its "prime" calls get
diluted, because a FIXED set of gears gives a FIXED survivor density while real primes keep thinning.
Change GEAR_LIMIT and watch the exact range move to GEAR_LIMIT^2.
"""
import numpy as np
from primes_util import primes_up_to, is_prime

GEAR_LIMIT = 31
GEARS = np.array(primes_up_to(GEAR_LIMIT), dtype=np.float64)

def net(xs):
    x = np.asarray(xs, dtype=np.float64)
    ang = 2 * np.pi * x[:, None] / GEARS[None, :]
    seat_cos = np.cos(ang)                                   # layer 1 (the sin half isn't needed to detect seat 0)
    fires = np.maximum(seat_cos - np.cos(np.pi / GEARS)[None, :], 0) > 0   # layer 2: fires only at seat 0
    fires &= x[:, None] != GEARS[None, :]                   # a gear never blocks itself
    return ~fires.any(axis=1)                                # output

if __name__ == "__main__":
    print(f"gears: {GEARS.astype(int).tolist()}  -> exact up to {GEAR_LIMIT**2:,}")
    for lo, hi in [(2, GEAR_LIMIT ** 2), (1_000, 11_000), (100_000, 110_000), (10**6, 10**6 + 10_000), (10**9, 10**9 + 10_000)]:
        xs = np.arange(lo, hi)
        pred = net(xs)
        true = np.array([is_prime(int(v)) for v in xs])
        said, right, missed = int(pred.sum()), int((pred & true).sum()), int((true & ~pred).sum())
        print(f"{lo:>14,} .. {hi:<14,} calls prime {said:6d} | truly prime {right:6d} ({right/max(said,1):6.1%}) | missed {missed}")
