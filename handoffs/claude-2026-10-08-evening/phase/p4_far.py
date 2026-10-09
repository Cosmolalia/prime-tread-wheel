"""P4 further out: greedy only (a found cover proves a wipe-out exists; a miss proves nothing by itself).
For each scale, 12 consecutive even numbers. Also report the real number of Goldbach pairs and how many
candidates survive a random turning, to see whether the rings can still aim."""
import json, math, time, sys
import numpy as np
from p4_goldbach import setup, greedy
from primes_util import sieve
ISP = sieve(2_100_000)
rng = np.random.default_rng(9)
res = {}
t0 = time.time()
for base in (1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000):
    wins, tot, pairs = 0, 0, []
    tries = 12 if base <= 8000 else 4
    for N2 in range(base, base + 24, 2):
        n, y, rings, seams, X = setup(N2)
        ok = greedy(X, rings, seams, rng, tries=tries)
        wins += ok; tot += 1
        pairs.append(sum(1 for x in X if ISP[x] and ISP[N2 - x]))
    res[base] = {"wiped": wins, "of": tot, "mean_real_pairs": float(np.mean(pairs)), "candidates": int(X.size), "rings": len(rings)}
    print(f"2n near {base}: greedy wiped {wins}/{tot}; real pairs ~{np.mean(pairs):.0f}; candidates {X.size}; rings {len(rings)}  [{time.time()-t0:.0f}s]", flush=True)
json.dump(res, open("p4_far.json", "w"), indent=1)
