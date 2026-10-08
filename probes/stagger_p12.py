#!/usr/bin/env python3
"""
stagger_p12.py — P12: WHAT in the quadratic counter fattens the mouth tail?

stagger_mc found: quad-counter mouth widths match an iid-lap null in the body
but run ~1.5x fatter in the tail (m <= 2e4), mechanism unpinned. Two candidate
mechanisms, both properties of the real counter only:

  (A) ORBIT CONFINEMENT: each o_p lives on the triangular-image set
      {T(j) mod p}, size (p+1)/2 — never all p phases. Even with NO
      cross-lap memory, confinement alone changes the per-lap cover law
      (smaller effective primes -> sparser covers -> fatter W tail).
  (B) COUNTER COUPLING: all rings share the ONE walk s(m) = T(m-1), so
      phases across rings within a lap are correlated residues of one
      number, and across laps they co-move.

Deconfound: run a CONFINED-IID arm — per lap, per ring, draw o_p uniformly
from the triangular image (independent across laps AND rings, so coupling
is destroyed) but keep the confinement. Compare all three arms' W-tails on
identical laps. If confined-iid tail ~ quad tail -> (A) confinement. If
confined-iid tail ~ plain-iid tail -> (B) coupling. If in between, both.

Prediction (written before running): (A). Rationale: tail-W laps are those
where small rings happen to leave early ticks open; confinement halves ring
p's hit rate on its forbidden set unevenly, and the sieve-limit arcs p > W
never matter for W. Confined-iid destroys the lap-to-lap structure that the
body ACF showed is invisible anyway (P10 NULL), so the tail should survive
destruction of coupling.
"""

import math, os, random
from array import array

M_LO, M_HI = 100, 20000
WMAX = 2000
PSTRIKE = 5000
R_REPS = 6
QS = [0.5, 0.75, 0.9, 0.95, 0.99, 0.999, 1.0]

OUTDIR = os.path.join(os.path.dirname(__file__), "logs")

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * (((n - i*i) // i) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

PRIMES = [p for p in primes_upto(PSTRIKE) if p <= WMAX]

def tri_image(p):
    """distinct values of -T(j) mod p, j = 0..p-1  (the REAL orbit's reachable
    set: o_p = -T(m-1) mod p, so the image under negated triangular numbers)"""
    return sorted({(-(j * (j + 1) // 2)) % p for j in range(p)})

TRI = {p: tri_image(p) for p in PRIMES}

def w_series(arm, rng):
    """arm in {'quad','iid','confined'} -> W(m) array for m in [M_LO, M_HI]"""
    out = array("H", bytes(2 * (M_HI - M_LO + 1)))
    for i, m in enumerate(range(M_LO, M_HI + 1)):
        base = m * (m - 1) // 2
        cov = bytearray(WMAX + 1)
        for p in PRIMES:
            if arm == "quad":
                o = (-base) % p
            elif arm == "iid":
                o = rng.randrange(p)
            else:
                img = TRI[p]
                o = img[rng.randrange(len(img))]
            q = o if o else p
            while q <= WMAX:
                cov[q] = 1
                q += p
        w = 0
        for k in range(1, WMAX + 1):
            if not cov[k]:
                w = k
                break
        out[i] = w
    return out

def quantiles(ws):
    s = sorted(ws)
    n = len(s)
    return [s[min(n - 1, int(q * n))] for q in QS]

if __name__ == "__main__":
    import json, time
    t0 = time.time()
    print(f"P12: laps {M_LO}..{M_HI}  strikers {len(PRIMES)} (p<={PSTRIKE},<=WMAX)  WMAX={WMAX}  reps={R_REPS}")
    print("check confinement sizes: p=5 ->", len(TRI[5]), "of 5; p=11 ->", len(TRI[11]), "of 11")
    res = {}
    for arm in ["quad", "iid", "confined"]:
        acc = []
        reps = 1 if arm == "quad" else R_REPS
        for r in range(reps):
            rng = random.Random(1200 + r)
            s = w_series(arm, rng)
            acc.append(quantiles(s))
            print(f"  {arm} rep {r+1}/{reps} done ({time.time()-t0:.0f}s)", flush=True)
        # average quantiles across reps
        res[arm] = [sum(q[i] for q in acc) / len(acc) for i in range(len(QS))]
        print(f"  {arm}: " + "  ".join(f"q{int(q*1000)/10:g}={v:.0f}" for q, v in zip(QS, res[arm])), flush=True)

    print("\narm       " + "  ".join(f"q{int(q*1000)/10:g}" for q in QS))
    for arm in ["quad", "iid", "confined"]:
        print(f"{arm:9s} " + "  ".join(f"{v:5.0f}" for v in res[arm]))
    tail = res["quad"][-1] / max(1.0, res["iid"][-1])
    print(f"\ntail ratio quad/iid at q99.9: {tail:.2f}")
    json.dump({"laps": [M_LO, M_HI], "wmax": WMAX, "pstrike": PSTRIKE, "reps": R_REPS,
               "quantiles": QS, "result": res}, open(os.path.join(OUTDIR, "stagger_p12.json"), "w"), indent=1)
    print("wrote", os.path.join(OUTDIR, "stagger_p12.json"))
