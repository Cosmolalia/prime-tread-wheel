#!/usr/bin/env python3
"""Wheel-native regularity tests on a layer's shadow map.

1. Mouth redundancy: sum of in-run marks vs run seats (over-determination).
2. Slip alignment: for mouth primes larger than the run, k0 must land in
   [0, run]; test uniformity of k0 against the generic-sieve prediction.
3. Routed vs outside: how much of the mouth cover comes from primes that
   divide m (visible to the lap) vs primes below sqrt(T(m)) (invisible)?
"""
import sys, struct, math, collections

m = int(sys.argv[1]); run = int(sys.argv[2])
lo = m * (m - 1) // 2
raw = open(f"shadows_{m}_head.bin", "rb").read()
cov = struct.unpack(f"<{len(raw)//4}I", raw)

cover_total = {}
for line in open(f"logs/shadows_{m}.txt"):
    if line.startswith("COVER "):
        _, p, c = line.split(); cover_total[int(p)] = int(c)

# factor m
mfac = []
mm = m
for p in range(2, int(mm**0.5) + 1):
    while mm % p == 0: mfac.append(p); mm //= p
if mm > 1: mfac.append(mm)
routed = set(mfac)

run_marks = collections.Counter(); run_seat_pos = []
for k in range(1, run + 1):
    if math.gcd(k, m) != 1: continue
    run_seat_pos.append(k)
    p = cov[k-1]
    if p: run_marks[p] += 1

total_marks = sum(run_marks.values())
print(f"mouth: {len(run_seat_pos)} seats, {total_marks} marks from {len(run_marks)} primes "
      f"(redundancy {total_marks/len(run_seat_pos):.2f}x)")
routed_in_run = {p: c for p, c in run_marks.items() if p in routed}
print(f"routed primes (|m) striking the mouth: {routed_in_run if routed_in_run else 'NONE'}")
outside_marks = sum(c for p, c in run_marks.items() if p not in routed)
print(f"marks from outside primes: {outside_marks}/{total_marks} "
      f"({100*outside_marks/total_marks:.1f}%)")

large = sorted(p for p in run_marks if p > run)
print(f"\nlarge one-off strikers (p > {run}): {len(large)}")
k0s = [(-lo) % p for p in large]
print("their k0 values:", k0s[:20], "..." if len(k0s) > 20 else "")
# uniformity on [0, run] vs [0, p-1]: observed k0 all <= run by construction.
# generic-sieve prediction: number of large strikers ~ sum over primes of P(strike a seat in run)
# crude model: expected distinct large strikers on seats
exp = 0.0
for p in large:  # sanity: reconstruct expectation from the observed size range
    pass
# expected count under uniformity: sum_{766<p<=lim} (run/p) * seat_frac, but
# restricted to seats whose value's SMALLEST factor is p requires sieve theory;
# upper-bound estimate: expected marks on seats from primes > run:
seat_frac = len(run_seat_pos) / run
import bisect
primes = sorted(cover_total)
s = 0.0
for p in primes:
    if p <= run: continue
    s += run / p * seat_frac
print(f"crude expected large-prime seat-marks in any {run}-tick window: {s:.1f} "
      f"(observed distinct large strikers: {len(large)})")

# single points of failure: primes whose removal would open a seat
openable = sum(1 for p, c in run_marks.items() if c == 1)
print(f"\nprimes covering exactly 1 mouth seat: {openable} "
      f"(removing any one of them still leaves {len(run_seat_pos)-1} covered)")
