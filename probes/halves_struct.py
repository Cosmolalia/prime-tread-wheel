#!/usr/bin/env python3
"""
halves_struct.py — BRIDGE 2: does the halves-claim have ANY width-based
(structural) support, or does it ride entirely on the walk?

Cross-session probe (Kimi x Claude handoff, Oct 8 evening). His BRIDGE 2:
for half-layer windows, where the first covered run of that length sits
beyond the layer, the halves claim holds by structure alone.

SETUP. Layer m, window = left half ticks 1..floor(m/2) (values
T(m-1)+1 .. T(m-1)+floor(m/2)); same for the right half. A turning of the
rings (phases free; ring 2 NOT held here — see below) covers the half if
every value in the window is marked. Width-only obstruction: the longest
run coverable by k rings anywhere is h(k)-1 (A048670, ring 2 held; with
ring 2 free the adversary is stronger, so h-1 is a LOWER bound on capacity).
Parity (his layer-parity rule): covered stretches start and end on evens,
so a window starting on an even value needs a run >= its width H; starting
on odd, H+1 starting one in.

Ring 2 convention deviation (documented): his free-phase tests hold ring 2
on the evens (no even past 2 is prime). Here ring 2 is left FREE, which
only strengthens the adversary — so "capacity permits / cover exists"
conclusions are conservative for the claim, and an uncoverability verdict
would be even stronger. We expect to find only the former.

PRE-REGISTERED CALLS (written before running):
(a) For every m = 21..270 (range of the A048670 table: pi(270)=57 rings):
    required run R(m,half) < capacity C(m) = A048670[pi(m)] - 1 for both
    halves. I.e. width NEVER obstructs a half-cover. (Expect: holds easily;
    h grows superlinearly, R ~ m/2.)
(b) Greedy existence: for m = 21..60, greedily construct an explicit
    free-phase turning covering the LEFT half. Expect: exists for all
    m >= 21 (half-covers are far easier than the full wipes, which free
    rings achieve from m=41 per the Jacobsthal list). Greedy failure would
    NOT prove uncoverability (greedy is not exhaustive) — report as
    "not found by greedy" only.
(c) Record capacity/requirement ratio trend across the table range.
"""

import math

# A048670 (Jacobsthal of primorials), 58 terms, fetched from OEIS 2026-10-08.
A048670 = [2,4,6,10,14,22,26,34,40,46,58,66,74,90,100,106,118,132,152,174,
           190,200,216,234,258,264,282,300,312,330,354,378,388,414,432,450,
           476,492,510,538,550,574,600,616,642,660,686,718,742,762,798,810,
           834,858,876,908,926,954]

def T(m): return m*(m+1)//2

def primes_upto(n):
    out, x = [], 2
    while x <= n:
        if all(x % q for q in out): out.append(x)
        x += 1
    return out

def required(m, left=True):
    """Required covered-run length for a half-window of layer m."""
    H = m // 2
    k0 = 1 if left else (m - H + 1)          # first tick of window
    v1 = T(m-1) + k0
    return H if v1 % 2 == 0 else H + 1

def capacity(m):
    k = len(primes_upto(m))
    return A048670[k-1] - 1, k

def greedy_half_cover(m, left=True, seed=1):
    """Greedy: repeatedly add the (ring, phase) covering most uncovered
    ticks of the window. Returns (covered_bool_list, n_rings_used) or None."""
    H = m // 2
    k0 = 1 if left else (m - H + 1)
    ticks = list(range(k0, k0 + H))
    rings = primes_upto(m)
    uncovered = set(ticks)
    phases = {}
    while uncovered:
        best = None
        for p in rings:
            if p in phases: continue
            # best phase for this ring: mode of (-v) mod p over uncovered v
            from collections import Counter
            c = Counter((-(T(m-1) + k)) % p for k in uncovered)
            phi, n = c.most_common(1)[0]
            if best is None or n > best[0]:
                best = (n, p, phi)
        if best is None or best[0] == 0:
            return None, len(phases)
        _, p, phi = best
        phases[p] = phi
        base = T(m-1)
        uncovered = {k for k in uncovered if (base + k) % p != phi}
    return ticks, len(phases)

if __name__ == "__main__":
    print("=== (a)+(c) capacity vs requirement, m = 21..270 ===")
    worst = None
    shortfall = []
    for m in range(21, 271):
        C, k = capacity(m)
        for half in ("L", "R"):
            R = required(m, left=(half == "L"))
            if R >= C:
                shortfall.append((m, half, R, C))
            ratio = C / R
            if worst is None or ratio < worst[0]:
                worst = (ratio, m, half, R, C, k)
    print(f"windows where requirement >= capacity (width obstruction): {shortfall}")
    print(f"minimum capacity/requirement ratio: {worst[0]:.1f}x at m={worst[1]} "
          f"({worst[2]} half, R={worst[3]}, C={worst[4]}, k={worst[5]} rings)")
    print(f"ratio at m=270: {capacity(270)[0]/required(270, True):.1f}x")

    print("\n=== (b) greedy left-half cover, m = 21..60 ===")
    not_found = []
    for m in range(21, 61):
        ticks, nused = greedy_half_cover(m, left=True)
        if ticks is None:
            not_found.append(m)
            print(f"  m={m}: NOT FOUND by greedy (used {nused} rings)")
        else:
            print(f"  m={m}: covered left half (H={m//2}) with {nused} rings")
    print(f"greedy failures: {not_found} (not proof of uncoverability)")
