#!/usr/bin/env python3
"""
PHASE 18a — P-TRI reading adjudication (GLM's fork, evening relay).

Question: under which anchor reading does an exact-cover engine with
Claude's now-stated conventions (window = ticks 1..m of layer m,
rings = primes p <= isqrt(T(m-1)), one offset per ring,
feasible = every tick hit) reproduce P-TRI's published infeasible set
{19-21,25,29-33,35-39,42-44,52}?

  Reading B (honest confined): allowed offsets o in {-T(i) mod p : i>=0}
  Reading A (triangular anchor +T(m-1)): allowed offsets o in {+T(i) mod p}

GLM predicts: Reading A -> universal feasibility (8T(m-1)+1 = (2m-1)^2 is
a literal square, so every tick passes every ring's QR test); Reading B ->
genuine infeasibility. This probe tests both directly, extends the match
to m <= 80 (new predictions beyond the published m <= 60 range), and also
reports GLM's one-line QR criterion per layer as a cross-check.

Date: 2026-10-13 (night). Artifact: lab/PHASE18_ptri_reading.py
"""

import math
import json
import time

def primes_upto(n):
    s = bytearray([1]) * (n + 1)
    s[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]

T = lambda n: n * (n + 1) // 2

def tri_offsets(p, sign):
    """Allowed offsets under the two readings. T(i) mod p has period p for
    odd p (T(i+p)-T(i) = p(i + (p+1)/2) == 0 mod p) and period 4 for p=2;
    range(4p) is safe for both."""
    return {sign * T(j) % p for j in range(4 * p)}

def feasible(m, sign):
    """Exact cover: one offset per ring, every tick 1..m hit at least once."""
    rings = primes_upto(math.isqrt(T(m - 1)))
    allowed = {p: tri_offsets(p, sign) for p in rings}
    cap = {p: -(-m // p) for p in rings}
    def rec(unc, unused):
        if not unc:
            return True
        if len(unc) > sum(cap[p] for p in unused):
            return False
        k = min(unc)
        for p in unused:
            o = k % p
            if o not in allowed[p]:
                continue
            hit = frozenset(t for t in unc if t % p == o)
            if rec(unc - hit, unused - {p}):
                return True
        return False
    return rec(frozenset(range(1, m + 1)), frozenset(rings))

def qr_union_feasible(m):
    """GLM's one-line per-ticket QR criterion (union relaxation, odd rings):
    tick j coverable by ring p iff 2-(2m-1)^2-8j is QR or 0 mod p.
    Relaxation: layer feasible iff EVERY tick is coverable by SOME ring.
    (Ring 2's offset set {0,1} covers everything, so it is excluded here —
    the union test is over odd rings only, else it is vacuous.)"""
    rings = [p for p in primes_upto(math.isqrt(T(m - 1))) if p != 2]
    if not rings:
        return None
    base = 2 - (2 * m - 1) ** 2
    for j in range(1, m + 1):
        v = base - 8 * j
        if not any(pow(v % p, (p - 1) // 2, p) != p - 1 for p in rings):
            # all p gave Legendre -1  ->  no odd ring can cover tick j
            # (pow == p-1 means non-residue; ==0 or 1 means covered)
            pass
        ok = any(pow(v % p, (p - 1) // 2, p) in (0, 1) for p in rings)
        if not ok:
            return False
    return True

PUBLISHED = [19, 20, 21, 25, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 42, 43, 44, 52]
OCT8 = [18, 19, 20, 24, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 49, 53, 56, 57]

def main():
    M_MAX = 80
    res = {"minus": [], "plus": [], "qr_union": []}
    t0 = time.time()
    for m in range(2, M_MAX + 1):
        if not feasible(m, -1):
            res["minus"].append(m)
        if not feasible(m, +1):
            res["plus"].append(m)
        q = qr_union_feasible(m)
        if q is False:
            res["qr_union"].append(m)
    dt = time.time() - t0

    out = {
        "M_MAX": M_MAX,
        "seconds": round(dt, 1),
        "reading_B_infeasible": res["minus"],
        "reading_A_infeasible": res["plus"],
        "qr_union_infeasible": res["qr_union"],
        "published_PTRI_infeasible_m<=60": PUBLISHED,
        "oct8_confined_unwipeable": OCT8,
        "reading_B_matches_published_m<=60":
            res["minus"] == PUBLISHED,
        "reading_A_is_universal_m>=4":
            all(m in (2, 3) or m not in res["plus"] for m in range(4, M_MAX + 1)),
    }
    with open("lab/PHASE18_ptri_reading.json", "w") as f:
        json.dump(out, f, indent=1)

    print(f"m <= {M_MAX}  ({dt:.1f}s)")
    print("Reading B (-T(i) offsets):", res["minus"])
    print("  matches P-TRI published (m<=60):", out["reading_B_matches_published_m<=60"])
    print("Reading A (+T(i) offsets):", res["plus"])
    print("  universal for m>=4:", out["reading_A_is_universal_m>=4"])
    print("QR-union relaxation    :", res["qr_union"])
    print("P-TRI published        :", PUBLISHED)
    print("Oct-8 list             :", OCT8)

if __name__ == "__main__":
    main()
