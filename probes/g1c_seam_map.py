#!/usr/bin/env python3
"""
g1c_seam_map.py — map seam deadness over ALL coprime a/b (b <= 18, a <= 18)
and factor the dead seams to expose the identity.

Round-2 finding: seam dead (m >= 50) at 1:1, 1:2, 3:8, 1:16, 1:6, 1:14 —
but alive at 5:8, 7:8, 3:16, 5:6, 3:10, 5:12, 2:3, 4:5, 2:7.
Neither numerator, denominator, a/b, nor ab separates the sets.
Map the whole territory, then read the law off the pattern.
"""
import numpy as np
from math import gcd

LIMIT = 5_000_000

def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    s[4::2] = False
    for p in range(3, int(n ** 0.5) + 1, 2):
        if s[p]: s[p*p::2*p] = False
    return s

SIEVE = sieve(LIMIT)
PRIMES = [p for p in range(2, 3000) if SIEVE[p]]

def factor(n):
    f = {}
    for p in PRIMES:
        if p * p > n: break
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def seam_scan(a, b):
    """return (n_seam_primes_m>=50, largest_seam_prime) for ratio a/b"""
    L = [0] * 3; B = 0
    cnt = 0; big = 0
    prevL = 0
    for m in range(1, 100000):
        Lm = int(a * m / b + 0.5)
        if m >= 2:
            B += prevL
            N = B + Lm
            if N > LIMIT: break
            if m >= 50 and SIEVE[N]:
                cnt += 1; big = max(big, N)
        prevL = Lm
    return cnt, big

print("SEAM MAP — coprime a/b, 1 <= a <= 18, 1 <= b <= 18")
print("  . = seam dead (no primes m>=50 within 5M)   P = seam alive")
print("  rows a (numerator), cols b (denominator)")
hdr = "      " + "".join(f"{b:>3}" for b in range(1, 19))
print(hdr)
dead_list = []
for a in range(1, 19):
    row = f"a={a:>2}  "
    for b in range(1, 19):
        if gcd(a, b) != 1:
            row += "  -"
            continue
        cnt, big = seam_scan(a, b)
        if cnt == 0:
            row += "  ."
            dead_list.append((a, b))
        else:
            row += "  P"
    print(row)

print(f"\ndead seams ({len(dead_list)}): {dead_list}")

print("\nFACTORIZATION of dead seams — find the identity:")
for a, b in dead_list[:14]:
    print(f"\n-- {a}:{b} --")
    B = 0; prevL = 0; shown = 0
    for m in range(1, 200):
        Lm = int(a * m / b + 0.5)
        if m >= 2:
            B += prevL
            N = B + Lm
            if 50 <= m and shown < 6:
                f = factor(N)
                fs = " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))
                print(f"   m={m:3}  N={N:7}  L={Lm:3}  B={B:7}  = {fs}")
                shown += 1
        prevL = Lm
print("\nDONE")
