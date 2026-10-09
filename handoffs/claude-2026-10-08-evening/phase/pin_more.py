"""Follow-ups to pin_test.py:
 (a) every layer 41..391 with only 2 and 3 pinned (the mirror and its 1.5): can the rest still wipe it?
 (b) exact, with a bitset over every phase setting: free all gears up to 17 or 19, pin the bigger ones; any wipe?"""
import math, time
import numpy as np
from pin_test import gears, leftovers, greedy_free, verify, T

rng = np.random.default_rng(5)
bad = []
for m in range(41, 392):
    g = gears(m)
    U = leftovers(m, g[:2])
    a = greedy_free(U, g[2:], rng, 25)
    if a is None or not verify(m, g[:2], a):
        bad.append(m)
print("(a) layers 41-391 that could NOT be wiped with 2 and 3 pinned (greedy):", bad)

def any_wipe_bitset(m, nfree):
    g = gears(m)
    free, pinned = g[:nfree], g[nfree:]
    U = leftovers(m, pinned)
    P = math.prod(free)
    cand = np.ones(P, dtype=bool)
    for x in U:
        mk = np.zeros(P, dtype=bool)
        for p in free:
            mk[int(x) % p::p] = True      # shifts t with t = x (mod p): gear p, turned to t, marks x
        cand &= mk
        if not cand.any():
            return False, len(U)
    return True, len(U)

t0 = time.time()
for m in (61, 101, 151, 201, 251, 301, 351, 390):
    for nf in (7, 8):
        ok, u = any_wipe_bitset(m, nf)
        print(f"(b) layer {m}: free gears up to {gears(m)[nf-1]}, pin the other {len(gears(m))-nf}: leftovers {u}, any wipe: {ok}   [{time.time()-t0:.0f}s]", flush=True)
