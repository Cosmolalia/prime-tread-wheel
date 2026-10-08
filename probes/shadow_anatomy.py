#!/usr/bin/env python3
"""Anatomy of a near-miss layer's leading shadow run, wheel-natively.

Reads shadows_<m>_head.bin (u32 covering prime per tick) + the COVER table,
and reports: which primes hold the mouth shut, their sizes vs the run length,
their slip alignment k0 = (-T(m-1)) mod p, and whether the run looks like a
generic sieve accident or a wheel-visible arrangement.
"""
import sys, struct, collections

m = int(sys.argv[1])
run = int(sys.argv[2])                      # leading run length to dissect
cover_total = {}
for line in open(f"logs/shadows_{m}.txt"):
    if line.startswith("COVER "):
        _, p, c = line.split()
        cover_total[int(p)] = int(c)

m_ = m
lo = m_ * (m_ - 1) // 2                     # T(m-1)
raw = open(f"shadows_{m_}_head.bin", "rb").read()
cov = struct.unpack(f"<{len(raw)//4}I", raw)

def is_seat(k):
    import math
    return math.gcd(k, m_) == 1

run_primes = collections.Counter()
run_seats = 0
for k in range(1, run + 1):
    if not is_seat(k):
        continue
    run_seats += 1
    p = cov[k-1]
    if p:
        run_primes[p] += 1

print(f"layer {m_}: leading {run} ticks contain {run_seats} seats")
print(f"{'p':>10} {'in_run':>7} {'layer_total':>12} {'run_share':>10} {'k0=(-lo)%p':>12} {'p<=run?':>8}")
for p, c in run_primes.most_common(25):
    k0 = (-lo) % p
    print(f"{p:>10} {c:>7} {cover_total.get(p,0):>12} "
          f"{c/max(1,cover_total.get(p,1)):>10.4f} {k0:>12} {'YES' if p<=run else '':>8}")
print(f"distinct primes holding the mouth: {len(run_primes)}")
big = [p for p in run_primes if p > run]
print(f"primes larger than the run that still strike inside it: {len(big)} "
      f"(each can strike at most once; largest: {max(big) if big else '-'})")
