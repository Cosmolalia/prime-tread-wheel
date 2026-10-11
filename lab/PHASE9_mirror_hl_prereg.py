#!/usr/bin/env python3
"""
PHASE 9 — pre-registered Hardy-Littlewood test of the B7 mirror-pair count.

The B7 mirror lift [F] plus measurement: even-m mirror pairs are Goldbach
representations of m^2 inside the layer window. Observed (2026-10-10 session,
script not archived): 11,085 pairs over even m < 3000. GLM froze the
prediction formula and decision rule in chat 2026-10-11; this artifact
executes them. Nothing in this file is tuned to make the ratio land in band.

CONVENTIONS (frozen before running):
  - m even, 2 <= m < 3000.
  - Pair (p, q): p + q = m^2, p <= q, both prime, T(m-1) < p.
    (T(m-1) < p together with p <= q is exactly "both summands in the layer
    window": q = m^2 - p < m^2 - T(m-1) = T(m).)
  - Unordered single count; the m = 2 self-pair (2,2) IS included.
  - Prediction per GLM, verbatim:
      E = sum_{m even < 3000} 2*C2 * prod_{p|m, p odd} (p-1)/(p-2)
              * sum_{p prime, T(m-1) < p <= m^2/2} 1/(ln p * ln(m^2 - p))
    C2 = 0.6601618 (twin-prime constant).
  - DECISION RULE (frozen): E/observed in [0.8, 1.25] -> [E] "sieve
    furniture", B7 closes with a quantitative match. Outside -> convention
    audit FIRST (window edges, m=2 inclusion, unordered counting), only then
    flag as signal. Log either way.
"""

from math import log
from sympy import primerange

C2 = 0.6601618
MMAX = 3000

def T(m):
    return m * (m + 1) // 2

# sieve primes up to (MMAX-1)^2
LIM = (MMAX - 1) ** 2
sieve = bytearray(b"\x01") * (LIM + 1)
sieve[0:2] = b"\x00\x00"
for i in range(2, int(LIM ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = b"\x00" * len(sieve[i * i::i])
is_p = sieve

def primes_in(lo, hi):
    return [x for x in range(max(2, lo), hi + 1) if is_p[x]]

# --- measurement: recount pairs under the frozen convention ---
obs_total = 0
obs_no2 = 0
for m in range(2, MMAX, 2):
    n = m * m
    for p in primes_in(T(m - 1) + 1, n // 2):
        if is_p[n - p]:
            obs_total += 1
            if m > 2:
                obs_no2 += 1

# --- prediction: GLM's frozen formula ---
E_total = 0.0
E_no2 = 0.0
for m in range(2, MMAX, 2):
    n = m * m
    sing = 1.0
    mm = m
    for p in primerange(3, m + 1):
        if mm % p == 0:
            sing *= (p - 1) / (p - 2)
            while mm % p == 0:
                mm //= p
    w = sum(1.0 / (log(p) * log(n - p))
            for p in primes_in(T(m - 1) + 1, n // 2))
    e = 2 * C2 * sing * w
    E_total += e
    if m > 2:
        E_no2 += e

print(f"observed (frozen convention, m=2 incl): {obs_total}")
print(f"observed (m=2 excl):                    {obs_no2}")
print(f"reference count from 2026-10-10:        11085")
print(f"E (GLM formula, m=2 incl):              {E_total:.1f}")
print(f"E (GLM formula, m=2 excl):              {E_no2:.1f}")
for obs, E, tag in ((obs_total, E_total, "m=2 incl"),
                    (obs_no2, E_no2, "m=2 excl")):
    r = E / obs
    verdict = "IN BAND [0.8, 1.25] -> [E] sieve furniture" if 0.8 <= r <= 1.25 \
        else "OUT OF BAND -> convention audit first"
    print(f"ratio E/obs ({tag}): {r:.4f}  {verdict}")
