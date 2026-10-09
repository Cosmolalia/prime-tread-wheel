"""Hold ring 2 on the evens (where counting from 1 puts it). Then a layer can be wiped only if its odd numbers
can all be covered by the odd rings turned freely. Odd numbers one step of 2 apart behave like a plain run, so
the most odds coverable is j(3*5*...*p) - 1, which should equal h(k)/2 - 1 (Jacobsthal: j(2n) = 2 j(n), n odd)."""
import json, math
import numpy as np
T = lambda m: m * (m + 1) // 2
PR = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
H = json.load(open("margin.json"))["H"]

def jac(mods, chunk=10_000_000):
    """largest gap between integers coprime to prod(mods), by direct scan of one period"""
    N = math.prod(mods); best = 0; last = None; s = 0
    while s < N + chunk:
        e = s + chunk
        mask = np.ones(chunk, dtype=bool)
        for p in mods: mask[(-s) % p::p] = False
        idx = np.flatnonzero(mask) + s
        seq = idx if last is None else np.concatenate(([last], idx))
        if seq.size > 1: best = max(best, int(np.diff(seq).max()))
        last = int(idx[-1]); s = e
        if s > N + 2 * best + 10: break
    return best
for k in range(2, 10):
    jo = jac(PR[1:k])
    print(f"rings 3..{PR[k-1]}: longest run of odds they can cover = {jo-1};  h(k)/2 - 1 = {H[k-1]//2 - 1}  {'ok' if jo == H[k-1]//2 else 'MISMATCH'}")

def kof(m):
    r = math.isqrt(T(m)); return sum(1 for p in PR if p <= r) if r < 100 else None
import sys
sys.path.insert(0, ".")
from primes_util import sieve
P = [int(p) for p in np.nonzero(sieve(400))[0]]
free_ok, pin_ok = [], []
for m in range(2, 392):
    lo, hi = T(m - 1) + 1, T(m)
    k = sum(1 for p in P if p * p <= hi)
    if k == 0: continue
    odds = (hi + 1) // 2 - lo // 2
    if m <= H[k - 1] - 1: free_ok.append(m)
    if k >= 2 and odds <= H[k - 1] // 2 - 1: pin_ok.append(m)
print("wipeable with every ring free, layers 2..391 not in the list:", [m for m in range(2, 392) if m not in free_ok])
print("wipeable with ring 2 held on the evens, layers 2..391 not in the list:", [m for m in range(2, 392) if m not in pin_ok])
print("differences:", sorted(set(free_ok) ^ set(pin_ok)))
