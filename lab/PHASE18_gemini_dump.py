#!/usr/bin/env python3
"""
PHASE 18b — Gemini's data dump (evening relay standing queue).

She asked for the exact k-arrays (uncovered tick indices) for the +/-5
layer windows where the primes 11, 97, and 257 first enter the sieve
bound. "Enter the bound": ring p first appears in the ring set at the
first layer m with isqrt(T(m-1)) >= p. "Uncovered": ticks k in 1..m whose
value T(m-1)+k has NO prime factor <= isqrt(T(m-1)) — i.e. the home-phase
translate's surviving primes (the wheel-native uncovered set).

Payload: lab/GEMINI_DUMP_2026-10-13.json — for each of the three entry
primes, for each layer in [m0-5, m0+5], the sorted uncovered-k array.
She computes the spacing-variance discontinuity herself from the raw data.

Date: 2026-10-13 (night). Artifact: lab/PHASE18_gemini_dump.py
"""

import math
import json

def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

T = lambda n: n * (n + 1) // 2

def entry_layer(p):
    m = 2
    while math.isqrt(T(m - 1)) < p:
        m += 1
    return m

def uncovered_array(m):
    base = T(m - 1)
    bound = math.isqrt(base)
    ps = primes_upto(bound)
    comp = bytearray(m + 1)  # comp[k] = 1 if some ring divides base+k
    for p in ps:
        r = (-base) % p
        if r == 0:
            r = p  # tick p (k=p) corresponds to value base+p
        for k in range(r, m + 1, p):
            comp[k] = 1
    return [k for k in range(1, m + 1) if not comp[k]]

def main():
    primes = [11, 97, 257]
    dump = {"conventions": {
        "entry_layer": "first m with isqrt(T(m-1)) >= p",
        "window": "layers m0-5 .. m0+5 inclusive",
        "uncovered_k": "k in 1..m with no prime factor of T(m-1)+k <= isqrt(T(m-1))",
        "note": "values T(m-1)+k that are 1 or prime survive; semiprimes with both "
                "factors above the bound also survive (rare at this scale).",
    }, "windows": {}}
    for p in primes:
        m0 = entry_layer(p)
        w = {}
        for m in range(m0 - 5, m0 + 6):
            arr = uncovered_array(m)
            w[str(m)] = {"uncovered": arr, "count": len(arr),
                         "is_entry_layer": m == m0}
        dump["windows"][str(p)] = {"entry_layer": m0, "layers": w}
        print(f"p={p}: entry layer m0={m0} "
              f"(isqrt(T({m0-1}))={math.isqrt(T(m0-1))}), "
              f"window {m0-5}..{m0+5}, "
              f"counts {[w[str(m)]['count'] for m in range(m0-5, m0+6)]}")

    with open("lab/GEMINI_DUMP_2026-10-13.json", "w") as f:
        json.dump(dump, f, indent=1)
    print("wrote lab/GEMINI_DUMP_2026-10-13.json")

if __name__ == "__main__":
    main()
