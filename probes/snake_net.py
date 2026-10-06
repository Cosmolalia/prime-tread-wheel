"""
snake_net.py: the snake that eats its own tail. A network that starts with ZERO weights and plants
every prime it outputs back into itself as a new gear (a new circle in layer 1).

A gear is planted the moment its prime is found, but only switches on when the snake reaches p*p
(the same rule as the wheel: each layer is decided by gears from earlier layers up to the square root).

Result to check: exact forever (no wrong calls, no misses), but it never stops growing.
The working part grows like sqrt(x); the memory grows with every prime.
"""
import time
import numpy as np
from primes_util import sieve

def run(N=300_000, report=(100, 1_000, 10_000, 100_000, 300_000)):
    gears = np.zeros(0)        # the weights: circle sizes
    active = 0                 # gears switched on (those with p*p <= x)
    found = []
    for x in range(2, N + 1):
        while active < len(gears) and gears[active] ** 2 <= x:
            active += 1
        g = gears[:active]
        fired = bool((np.cos(2 * np.pi * x / g) > np.cos(np.pi / g)).any()) if active else False
        if not fired:
            found.append(x)
            gears = np.append(gears, x)          # output becomes a weight
        if x in report:
            print(f"at {x:>9,}: gears planted {len(gears):>7,} | switched on {active:>4}")
    return found

if __name__ == "__main__":
    N = 300_000
    t = time.time()
    found = run(N)
    truth = np.nonzero(sieve(N))[0].tolist()
    wrong = len(set(found) - set(truth)); missed = len(set(truth) - set(found))
    print(f"primes found {len(found):,} | wrong {wrong} | missed {missed} | {time.time()-t:.1f}s")
