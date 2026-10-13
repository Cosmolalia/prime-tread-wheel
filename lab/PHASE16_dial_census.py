#!/usr/bin/env python3
"""
PHASE 16 — dial C-decomposition census over a wide ratio grid.
Date: 2026-10-13. Artifacts: lab/PHASE16_dial_census.py (+ .json).

Question (sharpened by the 2026-10-13 evidence swarm, filed bb89446):
"7/6 is the wheel's modal ratio" was naming [S] — the measured content is
argmax of the live-family singular series C over the PHASE8b 20-ratio b<=8
sweep. That argmax is resolution-dependent (swarm claim: 59/46 wins at
b<=60 with C ~ 6.64, because max-C confounds per-family density with
family count — more lottery tickets at bigger b).

This census MEASURES, over every coprime a/b with 2 <= b <= 60, 1 <= a <= 2b:
  - live families (non-square disc, integer-valued) per ratio, via the exact
    PHASE8b engine, ties-up convention L = (2*a*m+b)//(2*b);
  - per-family C_small = prod over p <= 67 of (1-rho/p)/(1-1/p),
    rho = number of roots of the family mod p;
  - decomposition log C_small = logC2 (2-adic) + logC_bad (odd p | b)
    + logC_rest (p neither 2 nor dividing b);
  - ranking stability: argmax over b-cuts {8,12,20,30,60}, by max-family C
    AND by sum-C over families (tickets x odds).
LEG V validates the C_small ranking against the full brute C (p < 2000,
the PHASE8b sing_series) on the old 20 ratios + observed top ratios.

Frozen BEFORE running:
  D1  at b-cut <= 8, argmax_C_small = 7/6 (reproduces the old sweep);
  D2  at b-cut <= 60, argmax_C_small != 7/6 (resolution-dependence);
  D3  every top-10 ratio at every cut has b even (2-adic x4 mechanism);
  D4  7/6 decomposition: logC2 = log 4 exactly; bad-prime factor at 3
      equals 1.5 (rho = 0 forced);
  D5  on the old-20 ratios, C_small top-5 ranking == C_full top-5.
Status: measured here = [S->measured]; PHASE8b sweep values = [E].
"""
import json
import math
import time
from fractions import Fraction as F
from math import gcd, isqrt, log

from sympy import primerange

PMAX = 67
PLIST = list(primerange(2, PMAX + 1))
OLD20 = [(5, 4), (7, 4), (9, 4), (11, 4), (3, 2), (5, 2), (7, 2), (5, 3),
         (7, 3), (8, 3), (4, 3), (7, 5), (9, 5), (11, 5), (5, 6), (7, 6),
         (5, 8), (7, 8), (9, 8)]


# ------------------------------------------------------- PHASE8b engine core


def wheel_tables(a, b, M):
    def L(m):
        return max(1, (2 * a * m + b) // (2 * b))

    c = [0] * (M + 2)
    S = [0] * (M + 2)
    Bv = [0] * (M + 2)
    for j in range(1, M + 1):
        c[j] = b * L(j) - a * j
    for m in range(1, M + 1):
        S[m + 1] = S[m] + c[m]
        Bv[m + 1] = Bv[m] + L(m)
    return L, Bv


def quad_on_class(Bv, L, r, mod, M):
    pts = []
    t = 0
    while r + mod * t <= M and len(pts) < 5:
        m = r + mod * t
        if L(m) % 2 == 0:
            pts.append((F(t), F(Bv[m] + L(m) // 2)))
        t += 1
    if len(pts) < 3:
        return None
    (x1, y1), (x2, y2), (x3, y3) = pts[:3]
    A = ((y2 - y1) * (x1 - x3) - (y3 - y1) * (x1 - x2)) / (
        (x2 * x2 - x1 * x1) * (x1 - x3) - (x3 * x3 - x1 * x1) * (x1 - x2))
    Bb = (y2 - y1 - A * (x2 * x2 - x1 * x1)) / (x2 - x1)
    Cc = y1 - A * x1 * x1 - Bb * x1
    if not all(A * x * x + Bb * x + Cc == y for x, y in pts):
        return None
    D = Bb * Bb - 4 * A * Cc
    return A, Bb, Cc, D


def live_families(a, b):
    """Live (non-square-D, integer-valued) eligible-class quadratics.
    Same predicates as PHASE8b analyze() steps 2-4."""
    M = 64 * b
    L, Bv = wheel_tables(a, b, M)
    elig4 = set()
    for m in range(b, M + 1):
        if L(m) % 2 == 0 and (Bv[m] + L(m) // 2) % 2 == 1:
            elig4.add(m % (4 * b))
    out = []
    for r4 in sorted(elig4):
        q = quad_on_class(Bv, L, r4, 4 * b, M)
        if q is None:
            continue
        A, Bb, Cc, D = q
        Di = D.numerator if D.denominator == 1 else -1
        if Di >= 0 and isqrt(Di) ** 2 == Di:
            continue  # square disc -> algebraically dead
        if A.denominator * Bb.denominator * Cc.denominator != 1:
            continue  # non-integer-valued family
        out.append((A.numerator, Bb.numerator, Cc.numerator, Di))
    return out


# ------------------------------------------------------------- measurements


def local_factors(Av, Bv2, Cv):
    """C_small and per-prime factors over p <= PMAX.
    Degenerate family: rho = p at some prime (p divides every coefficient,
    so every value is p-divisible -> arithmetically dead for large u,
    singular factor exactly 0). Flagged, not logged."""
    facs = {}
    C = 1.0
    degenerate = False
    for p in PLIST:
        rho = 0
        for t in range(p):
            if (Av * t * t + Bv2 * t + Cv) % p == 0:
                rho += 1
        f = (1 - rho / p) / (1 - 1 / p)
        if f <= 0:
            degenerate = True
        facs[p] = f
        C *= f
    return facs, C, degenerate


def decompose(facs, b):
    logC2 = log(facs[2])
    log_bad = sum(log(f) for p, f in facs.items() if p != 2 and b % p == 0)
    log_rest = sum(log(f) for p, f in facs.items()
                   if p != 2 and b % p != 0)
    return logC2, log_bad, log_rest


def full_C(Av, Bv2, Cv, psweep=2000):
    """PHASE8b sing_series verbatim (brute over primes < psweep)."""
    C = 1.0
    for p in primerange(2, psweep):
        rho = 0
        for t in range(p):
            if (Av * t * t + Bv2 * t + Cv) % p == 0:
                rho += 1
        C *= (1 - rho / p) / (1 - 1 / p)
    return C


def ratio_record(a, b):
    fams = live_families(a, b)
    if not fams:
        return {"a": a, "b": b, "n": 0, "ndeg": 0, "bestC": None,
                "sumC": 0.0}
    best = None
    sumC = 0.0
    ndeg = 0
    for Av, Bv2, Cv, Di in fams:
        facs, C, degenerate = local_factors(Av, Bv2, Cv)
        if degenerate:
            ndeg += 1
            continue
        sumC += C
        if best is None or C > best[0]:
            l2, lb, lr = decompose(facs, b)
            best = (C, Di, l2, lb, lr)
    if best is None:
        return {"a": a, "b": b, "n": 0, "ndeg": ndeg, "bestC": None,
                "sumC": 0.0}
    C, Di, l2, lb, lr = best
    return {"a": a, "b": b, "n": len(fams) - ndeg, "ndeg": ndeg,
            "bestC": round(C, 6), "sumC": round(sumC, 6), "bestD": Di,
            "logC2": round(l2, 6), "logCbad": round(lb, 6),
            "logCrest": round(lr, 6)}


def main():
    t0 = time.time()
    grid = []
    for b in range(2, 61):
        for a in range(1, 2 * b + 1):
            if gcd(a, b) == 1:
                grid.append((a, b))
    print(f"grid: {len(grid)} coprime ratios, b <= 60, 1 <= a <= 2b",
          flush=True)

    recs = []
    for i, (a, b) in enumerate(grid):
        recs.append(ratio_record(a, b))
        if (i + 1) % 300 == 0:
            print(f"  {i + 1}/{len(grid)} ({time.time() - t0:.0f}s)",
                flush=True)

    live = [r for r in recs if r["bestC"] is not None]

    # ranking stability per b-cut
    cuts = {}
    for cut in (8, 12, 20, 30, 60):
        sub = [r for r in live if r["b"] <= cut]
        by_best = sorted(sub, key=lambda r: -r["bestC"])[:10]
        by_sum = sorted(sub, key=lambda r: -r["sumC"])[:10]
        cuts[cut] = {
            "argmax_bestC": f"{by_best[0]['a']}/{by_best[0]['b']}",
            "top10_bestC": [f"{r['a']}/{r['b']}" for r in by_best],
            "top10_bestC_evenb": all(r["b"] % 2 == 0 for r in by_best),
            "argmax_sumC": f"{by_sum[0]['a']}/{by_sum[0]['b']}",
            "top10_sumC": [f"{r['a']}/{r['b']}" for r in by_sum],
        }

    def row(key):
        a, b = (int(x) for x in key.split("/"))
        for r in recs:
            if r["a"] == a and r["b"] == b:
                return r
        return None

    keyrows = {}
    for key in ["7/6", "59/46"]:
        r = row(key)
        if r:
            keyrows[key] = r

    # LEG V: C_small vs C_full on old-20 + the C_small top ratios
    val_targets = list(dict.fromkeys(
        OLD20 + [tuple(map(int, k.split("/")))
                 for k in cuts[60]["top10_bestC"][:5]]))
    val = []
    for a, b in val_targets:
        fams = live_families(a, b)
        if not fams:
            continue
        rated = []
        for Av, Bv2, Cv, Di in fams:
            _, Cs, deg = local_factors(Av, Bv2, Cv)
            if deg:
                continue
            rated.append((Cs, full_C(Av, Bv2, Cv), Di))
        rated.sort(reverse=True)
        val.append({
            "ratio": f"{a}/{b}",
            "famCs_small": [round(x[0], 4) for x in rated],
            "famCs_full": [round(x[1], 4) for x in rated],
            "best_small_vs_full": round(rated[0][0] / rated[0][1], 4),
        })
        print(f"LEG V {a}/{b}: " + ", ".join(
            f"{s:.3f}/{f:.3f}" for s, f, _ in rated[:3]), flush=True)

    small_rank = sorted(val, key=lambda v: -max(v["famCs_small"]))
    full_rank = sorted(val, key=lambda v: -max(v["famCs_full"]))
    top5_small = [v["ratio"] for v in small_rank[:5]]
    top5_full = [v["ratio"] for v in full_rank[:5]]

    verdict = {
        "D1_argmax_le8_is_7_6": cuts[8]["argmax_bestC"] == "7/6",
        "D2_argmax_le60_not_7_6": cuts[60]["argmax_bestC"] != "7/6",
        "D3_top10_even_b_all_cuts": all(c["top10_bestC_evenb"]
                                        for c in cuts.values()),
        "D4_7_6_decomp": None,  # filled below
        "D5_top5_rank_agreement": top5_small == top5_full,
    }
    r76 = keyrows.get("7/6")
    if r76:
        verdict["D4_7_6_decomp"] = (
            abs(r76["logC2"] - log(4)) < 1e-9
            and abs(r76["logCbad"] - log(1.5)) < 1e-6)

    out = {
        "frozen": {"D1": cuts[8]["argmax_bestC"] == "7/6",
                   "D2": cuts[60]["argmax_bestC"] != "7/6"},
        "cuts": cuts,
        "keyrows": keyrows,
        "legV": val,
        "top5_small": top5_small,
        "top5_full": top5_full,
        "n_grid": len(grid),
        "n_live_ratios": len(live),
        "seconds": round(time.time() - t0, 1),
        "verdict": verdict,
    }
    with open("lab/PHASE16_dial_census.json", "w") as f:
        json.dump(out, f, indent=1)
    # compact full grid for downstream re-analysis
    with open("lab/PHASE16_dial_census_grid.json", "w") as f:
        json.dump(recs, f)
    print(json.dumps({"cuts": cuts, "keyrows": keyrows,
                      "verdict": verdict, "seconds": out["seconds"]},
                     indent=1), flush=True)


if __name__ == "__main__":
    main()
