#!/usr/bin/env python3
"""Q4 follow-up — is the BH underprediction a small-N density artifact?
Bucket double-prime spokes by b; observed/pred ratio should -> 1 as b grows
if the miss lives in the 1/ln N approximation for small N."""
import json
import math
from math import gcd, isqrt, log

BMAX = 2000
top = 2 * ((BMAX * BMAX - BMAX) // 2 + BMAX) + BMAX * BMAX + 4
comp = bytearray(top + 1)
comp[0] = comp[1] = 1
for p in range(2, isqrt(top) + 1):
    if not comp[p]:
        comp[p * p::p] = b'\x01' * (((top - p * p) // p) + 1)
C2 = 0.6601618158468696
PR = [p for p in range(2, BMAX + 1) if not comp[p]]


def ss(b):
    s = 2.0 * C2
    for l in PR:
        if l > b:
            break
        if b % l == 0:
            s *= (l - 1) / (l - 2)
    return s


buckets = {}
for b in range(3, BMAX + 1, 2):
    s = ss(b)
    for a in range(1, b):
        if gcd(a, b) != 1:
            continue
        n1 = (b * b - b) // 2 + a
        n2 = 2 * n1 + b * b
        w = 1.0 / (log(n1) * log(n2))
        key = b // 200
        e = buckets.setdefault(key, [0, 0.0, 0.0])
        e[1] += w
        e[2] += s * w
        if not comp[n1] and not comp[n2]:
            e[0] += 1
out = {}
print("b-range      observed  pred_naive  pred_BH   obs/pred_BH")
for k in sorted(buckets):
    o, pn, pb = buckets[k]
    r = o / pb if pb else 0
    out[f"{k*200}-{k*200+199}"] = {"obs": o, "pred_naive": pn, "pred_bh": pb, "ratio": r}
    print(f"{k*200:>4}-{k*200+199:<4} {o:>8} {pn:>10.0f} {pb:>9.0f} {r:>10.3f}")
with open("lab/ARCHIVE_Q4b_buckets.json", "w") as f:
    json.dump(out, f, indent=1)
