#!/usr/bin/env python3
"""
stagger_p12b.py — P12b: ABLATION. Where does the quad counter's tail
fattening live: multi-tick arcs or single-tick darts?

stagger_mc (m <= 2e4): quad-counter mouth widths show ~1.5x fatter tail
than an iid-lap null. P12 (this morning): with arcs p <= WMAX only, quad,
iid, and confined-iid arms are indistinguishable at every quantile
(q99.9: 71/72/72). Difference between the two setups: stagger_mc's arc
set runs to p <= isqrt(T(m-1)+KMAX) ~ 14149 at m=2e4, so primes in
(WMAX, 14149] throw SINGLE-TICK DARTS into the window (they mark tick
o_p only, if o_p <= WMAX). P12 dropped them.

Hypothesis (written before running): the fattening is carried entirely
by the dart channel, and specifically by COUNTER coupling — the darts of
different primes are residues of ONE number (-base), so they clump in
the window in a way independent uniform darts do not. Arms, same laps:

  full-quad : arcs p <= isqrt(T(m-1)+WMAX)        [reproduces stagger_mc]
  full-iid  : same arc set, offsets uniform/lap
  cut-quad  : arcs p <= WMAX only                 [reproduces P12]
  cut-iid   : same, uniform

If full-quad tail > full-iid tail AND cut-quad ~ cut-iid: darts carry
the fattening; and since P12 showed confined multi-tick arcs do not,
the mechanism is counter coupling in the single-tick channel: the ONLY
aggregate fingerprint the quadratic counter leaves in cover statistics.
"""

import math, os, random
from array import array

M_LO, M_HI = 100, 20000
WMAX = 2000
R_REPS = 6
QS = [0.5, 0.9, 0.99, 0.999, 1.0]
OUTDIR = os.path.join(os.path.dirname(__file__), "logs")

def primes_upto(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = b"\x00" * (((n - i*i) // i) + 1)
    return [i for i in range(2, n + 1) if sieve[i]]

PR_CUT = primes_upto(WMAX)
PR_FULL = primes_upto(int(math.isqrt(M_HI * (M_HI + 1) // 2 + WMAX)) + 10)
print(f"arc primes: cut {len(PR_CUT)} (p<={PR_CUT[-1]}), full {len(PR_FULL)} (p<={PR_FULL[-1]})")

def w_series(arm, rng):
    full = arm.startswith("full")
    out = array("H", bytes(2 * (M_HI - M_LO + 1)))
    for i, m in enumerate(range(M_LO, M_HI + 1)):
        base = m * (m - 1) // 2
        # PER-LAP sieve limit (stagger_mc's lim): p <= isqrt(T(m-1)+WMAX).
        # Load-bearing: primes in (base, base+WMAX] would "self-mark" their
        # own tick k = p-base (value p is PRIME — must stay open). P12/P12b
        # v1 used one global arc set and quad W hit 1907 at m=157 (true gap 5).
        lim = math.isqrt(base + WMAX)
        PR = PR_FULL if full else PR_CUT
        cov = bytearray(WMAX + 1)
        for p in PR:
            if p > lim:
                break
            o = rng.randrange(p) if arm.endswith("iid") else (-base) % p
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
    res = {}
    for arm in ["full-quad", "full-iid", "cut-quad", "cut-iid"]:
        acc = []
        reps = 1 if arm.endswith("quad") else R_REPS
        for r in range(reps):
            rng = random.Random(9900 + r)
            acc.append(quantiles(w_series(arm, rng)))
        res[arm] = [sum(q[i] for q in acc) / len(acc) for i in range(len(QS))]
        print(f"{arm:8s}: " + "  ".join(f"q{int(q*1000)/10:g}={v:.0f}" for q, v in zip(QS, res[arm]))
              + f"  ({time.time()-t0:.0f}s)", flush=True)
    fq, fi = res["full-quad"][-2], res["full-iid"][-2]
    cq, ci = res["cut-quad"][-2], res["cut-iid"][-2]
    print(f"\nq99.9 tail ratio  full: quad/iid = {fq/fi:.2f}   cut: quad/iid = {cq/max(ci,0.5):.2f}")
    verdict = (fq > 1.2 * fi) and (abs(cq - ci) < 0.1 * fi)
    print("VERDICT:", "DARTS CARRY THE FATTENING (coupling in single-tick channel)" if verdict
          else "hypothesis NOT cleanly supported — inspect table")
    json.dump({"laps": [M_LO, M_HI], "wmax": WMAX, "reps": R_REPS, "quantiles": QS, "result": res},
              open(os.path.join(OUTDIR, "stagger_p12b.json"), "w"), indent=1)
    print("wrote", os.path.join(OUTDIR, "stagger_p12b.json"))
