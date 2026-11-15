#!/usr/bin/env python3
"""Independent tick-by-tick verification of the banked 47-rotation witness (best47_argon.json).

Recomputes the wheel model from scratch (no highspy): m=1500, T=m(m-1)/2,
primes <= isqrt(T), one phase per prime, tick k covered iff
(T+k) % p == phase_p for some prime p. Verifies:
  1. every phase in [0, p)
  2. cost = number of nonzero phases == 47
  3. every tick k in [1, m] covered (uncovered == 0), checked individually
"""
import json, math, sys, os

def primes_to(n):
    a = bytearray(b'\x01') * (n + 1); a[:2] = b'\x00\x00'
    for p in range(2, math.isqrt(n) + 1):
        if a[p]:
            a[p*p::p] = b'\x00' * ((n - p*p)//p + 1)
    return [i for i in range(n + 1) if a[i]]

m = 1500
T = m * (m - 1) // 2
B = math.isqrt(T)
primes = primes_to(B)

default_path = os.path.join(os.path.dirname(__file__), "best47_argon.json")
doc = json.load(open(sys.argv[1] if len(sys.argv) > 1 else default_path))
phases = doc["phases"] if isinstance(doc, dict) else doc

assert len(phases) == len(primes), (len(phases), len(primes))
for ph, p in zip(phases, primes):
    assert 0 <= ph < p, (ph, p)

cost = sum(1 for ph in phases if ph != 0)

uncovered = []
for k in range(1, m + 1):
    if not any((T + k) % p == ph for p, ph in zip(primes, phases)):
        uncovered.append(k)

print(json.dumps({
    "m": m, "T": T, "B": B, "rings": len(primes),
    "cost_nonzero_phases": cost,
    "uncovered_count": len(uncovered),
    "uncovered_first10": uncovered[:10],
    "VERDICT": "PASS" if cost <= 47 and not uncovered else "FAIL",
}, indent=1))
