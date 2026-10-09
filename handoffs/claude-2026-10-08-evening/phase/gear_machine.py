"""A prime machine with no division, no multiplication, no testing of candidates: only counting forward and comparing.
Every gear advances one tooth per number and wraps at its size. A number that lands on no switched-on gear's seam
is prime, and becomes a new gear on the spot. A gear switches on when its seam count reaches its tooth count
(that happens exactly at its square: the wheel's square-root rule, done mechanically)."""
import time
from primes_util import sieve

def machine(N):
    gears = []                       # each: [teeth, position, seam visits, switched on]
    built = []
    for x in range(2, N + 1):
        hit = False
        for g in gears:
            g[1] += 1
            if g[1] == g[0]:
                g[1] = 0
                g[2] += 1
                if g[2] == g[0]:
                    g[3] = True
            if g[1] == 0 and g[3]:
                hit = True
        if not hit:
            built.append(x)
            gears.append([x, 0, 1, x == 2 and False])   # planted on its own seam: first visit
    return built

t = time.time()
N = 20000
b = machine(N)
truth = [int(p) for p in sieve(N).nonzero()[0]]
print(f"built {len(b)} primes up to {N} in {time.time()-t:.0f}s; identical to the primes: {b == truth}")
