#!/usr/bin/env python3
"""
wipe_dist.py — J1a: the realized turning's distance from wipe turnings.

Wedge (cross-session bridge): wipes exist in abundance among free turnings
(Claude: widths 41..391), the realized turning never wipes (A066888,
verified to layer 2.8B ~ lap 74700), and the realized turning is ONE
quadratic curve o_p(m) = -T(m-1) mod p. The conjecture reads: the curve
never enters the wipe set. Distance from the curve to the set was never
measured. Two obstacles shape this probe:

1. ENTAILMENT: for m <= ~74700 ANY wipe (hence any 1-flip wipe) would
   refute the verified A066888. So a small-m wipe scan cannot return a
   hit without falsifying either the verification or this probe's model.
   Framed honestly: this is a CROSS-VALIDATION of the stagger-arc shadow
   model against the verified prime record (cf. P10's seat-test bug —
   model-level blindness is a real failure class here).
2. PARITY TRAP: realized ring 2 covers one parity class whole, so every
   uncovered tick shares the other class and ONE ADDED phase of ring 2
   (semantics: keep realized arcs, add a phase) trivially "wipes". That
   metric is constant-1, uninformative. Correct semantics: a FLIP MOVES
   the arc (old class uncovered again). Under move-semantics we scan
   distance exactly 1: for every ring p, every phase phi != o_p:
   covered' = (covered & ~class(p, o_p)) | class(p, phi); wipe iff
   covered' == all ticks. O(1) big-int eval per candidate, sum_p p
   candidates per lap.

Outputs per lap: U(m) = ticks uncovered by realized arcs (pattern-side
mouth measure), oneflip = True iff some single move wipes.

Scope: m = 21..400 complete + sparse 450..2000. Prediction (written
first): oneflip empty everywhere; if not, the model or the verification
is wrong and everything downstream freezes. U(m)/m should decay like
the sieve density prod_{p<=m}(1 - 1/p) ~ e^-gamma / ln m (the realized
arcs are a genuine sieve alignment), modulo parabolic-orbit effects.
"""

import math, os, json, time

OUT = os.path.join(os.path.dirname(__file__), "logs", "wipe_dist.jsonl")
GAMMA = 0.5772156649015329
SPARSE = [450, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000]

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * (((n - i*i) // i) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

PRIMES = primes_upto(2000)

def lap_scan(m):
    Tm1 = (m - 1) * m // 2
    full = (1 << m) - 1
    rings = [p for p in PRIMES if p <= m]

    # class(p, phi): bitmask of ticks k in [1, m], k == phi mod p
    cls = {}
    for p in rings:
        bits = [0] * p
        for k in range(1, m + 1):
            bits[k % p] |= 1 << (k - 1)
        cls[p] = bits

    o_real = {p: (-Tm1) % p for p in rings}
    covered = 0
    for p in rings:
        covered |= cls[p][o_real[p]]
    U0 = m - covered.bit_count()
    realized_wipe = covered == full

    # exact distance-1 scan under MOVE semantics
    oneflip = False
    for p in rings:
        bits = cls[p]
        keep = covered & ~bits[o_real[p]]
        for phi in range(p):
            if phi != o_real[p] and (keep | bits[phi]) == full:
                oneflip = True
                break
        if oneflip:
            break

    # sieve-density prediction for U/m
    import functools, operator
    dens = 1.0
    for p in rings:
        dens *= (1 - 1.0 / p)
    return {"m": m, "U0": U0, "U_over_m": U0 / m,
            "sieve_dens": dens, "mertens": math.exp(-GAMMA) / math.log(m),
            "realized_wipe": realized_wipe, "oneflip": oneflip}

if __name__ == "__main__":
    t0 = time.time()
    laps = list(range(21, 401)) + SPARSE
    print(f"J1a: {len(laps)} laps, exact 1-flip wipe scan (move semantics) + U profile", flush=True)
    hits, wipes = [], []
    with open(OUT, "w") as f:
        for m in laps:
            r = lap_scan(m)
            f.write(json.dumps(r) + "\n")
            if r["oneflip"]:
                hits.append(m)
            if r["realized_wipe"]:
                wipes.append(m)
            if (m <= 400 and m % 50 == 0) or m in SPARSE:
                print(f"m={m} ({time.time()-t0:.0f}s) U={r['U0']} "
                      f"U/m={r['U_over_m']:.4f} sieve={r['sieve_dens']:.4f} "
                      f"mertens={r['mertens']:.4f} oneflip={r['oneflip']}", flush=True)
    print(f"\nrealized wipes: {wipes}")
    print(f"ONE-FLIP WIPES: {hits}")
    print("VERDICT:", "MODEL/VERIFICATION CONFLICT — freeze downstream" if (hits or wipes)
          else "consistent: realized turning is >= 2 moves from every wipe turning in scope")
    print("wrote", OUT)
