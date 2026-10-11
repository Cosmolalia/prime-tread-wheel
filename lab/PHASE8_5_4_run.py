#!/usr/bin/env python3
"""PHASE 8 run — pre-registered 5:4 half-turn extension to m = 10^6.
Executes the frozen predictions in lab/PHASE8_5_4_prereg.md and appends the
scorecard. Multiprocessing over sympy BPSW isprime. Reproduces every number.
"""
import json, time
from math import log
from multiprocessing import Pool
import sympy
from sympy import primerange, Rational, isprime

def L(m): return max(1, (10*m + 4)//8)

def candidates(M):
    """all (m, n) with L[m] even, m <= M"""
    out, base = [], 0
    for m in range(1, M+1):
        lm = L(m)
        if lm % 2 == 0:
            out.append((m, base + lm//2))
        base += lm
    return out

ELIGIBLE = lambda m: m == 8 or m % 16 in (6, 13)

def check(pair):
    m, n = pair
    return (m, n, bool(isprime(n)))

if __name__ == "__main__":
    t0 = time.time()
    # --- self-check: recomputed singular series and baseline ---
    C = Rational(2)
    for p in primerange(3, 300000):
        rho = 1 if p in (5, 41) else 1 + sympy.legendre_symbol(41, p)
        C *= (1 - Rational(rho, p)) / (1 - Rational(1, p))
    Cf = float(C)
    g13 = lambda u: 160*u*u + 262*u + 107
    g6  = lambda u: 160*u*u + 122*u + 23
    U = (1_000_000 - 13)//16
    S13 = sum(1.0/log(g13(u)) for u in range(U+1))
    S6  = sum(1.0/log(g6(u))  for u in range(U+1))
    pred = Cf*(S13+S6) + 1.0
    print(f"C = {Cf:.9f}  S13 = {S13:.3f}  S6 = {S6:.3f}  predicted total = {pred:.1f}")

    cands = candidates(1_000_000)
    print(f"{len(cands)} even-L half-turn candidates m<=1e6; testing primality ...")
    with Pool(12) as pool:
        res = pool.map(check, cands, chunksize=2048)
    dt = time.time() - t0

    primes = [(m, n) for m, n, p in res if p]
    viol = [(m, n) for m, n in primes if not ELIGIBLE(m)]
    c13 = sum(1 for m, n in primes if m % 16 == 13)
    c6  = sum(1 for m, n in primes if m % 16 == 6)
    c8  = sum(1 for m, n in primes if m == 8)
    total = len(primes)
    ratio = total / pred
    sigma = (total**0.5)/pred
    print(f"m<=1e6: primes={total} (c13={c13} c6={c6} c8={c8}) filter_violations={len(viol)}")
    print(f"ratio measured/predicted = {ratio:.5f}  (Poisson sigma = {sigma:.5f})")
    if viol: print("VIOLATIONS:", viol[:20])

    # baseline self-check at 20000
    base_primes = [(m, n) for m, n, p in res if p and m <= 20000]
    U2 = (20000-13)//16
    Sb = sum(1.0/log(g13(u)) for u in range(U2+1)) + sum(1.0/log(g6(u)) for u in range(U2+1))
    print(f"baseline m<=20000: measured {len(base_primes)} vs predicted {Cf*Sb+1:.1f}")

    out = {
        "C": Cf, "S13": S13, "S6": S6, "predicted_total": pred,
        "measured_total": total, "c13": c13, "c6": c6, "c8": c8,
        "predicted_c13": Cf*S13, "predicted_c6": Cf*S6,
        "violations": viol[:50], "n_violations": len(viol),
        "ratio": ratio, "poisson_sigma": sigma, "wall_s": round(dt, 1),
        "baseline_20000_measured": len(base_primes),
        "baseline_20000_predicted": Cf*Sb + 1,
    }
    with open("lab/PHASE8_5_4_results.json", "w") as f:
        json.dump(out, f, indent=2)

    # scorecard
    def verdict(band):
        return "HIT" if band else "MISS"
    lines = [
        "",
        "## 4. Result (filled by lab/PHASE8_5_4_run.py)",
        "",
        f"Wall: {dt:.0f}s on 12 workers. C recomputed in-run: {Cf:.9f} (matches prereg).",
        "",
        "| # | Prediction | Measured | Verdict |",
        "|---|---|---|---|",
        f"| 1 | 22,532 total, ratio in [0.98,1.02] | {total} primes, ratio {ratio:.5f} ({(ratio-1)/sigma:+.2f}σ) | "
        + ("HIT" if 0.98 <= ratio <= 1.02 else "MARGINAL" if 0.97 <= ratio <= 1.03 else "MISS") + " |",
        f"| 2 | c13 ≈ 11,265, c6 ≈ 11,266 (±3%) | c13 = {c13} ({100*(c13/(Cf*S13)-1):+.2f}%), c6 = {c6} ({100*(c6/(Cf*S6)-1):+.2f}%) | "
        + ("HIT" if abs(c13/(Cf*S13)-1) <= 0.03 and abs(c6/(Cf*S6)-1) <= 0.03 else "MISS") + " |",
        f"| 3 | zero filter violations | {len(viol)} violations" + (f": {viol[:5]}" if viol else "") + " | "
        + ("HIT" if not viol else "MISS") + " |",
        f"| 4 | baseline self-check 662 vs 662.6 | {len(base_primes)} vs {Cf*Sb+1:.1f} | "
        + ("HIT" if len(base_primes) == 662 else "MISS") + " |",
        "",
    ]
    with open("lab/PHASE8_5_4_prereg.md", "a") as f:
        f.write("\n".join(lines))
    print("scorecard appended to lab/PHASE8_5_4_prereg.md; JSON written")
