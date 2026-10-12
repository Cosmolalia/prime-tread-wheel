#!/usr/bin/env python3
"""
PHASE 11 — calm-slope derivation. Frozen pre-registration: Claude,
HANDOFF_CLAUDE_2026-10-11c.md (this file implements that spec verbatim).

Mechanism (all pieces from the handoff):
  Lane value   N(t) = (t^2 - t)/2 + c,   D = 1 - 8c,   rho(p) = 1 + (D|p)
  Pair density F[d] = G * prod_{p|d} (ap) * prod_{p: d^2 == D (p)} (bp)
    with generic base per odd prime  C_p = (1 - 2 rho/p) / (1 - rho/p)^2
    G = prod C_p over odd primes (p=2 handled by exact t-mod-4 count)
    p | d :   ap = (1 - rho/p)/(1 - 2 rho/p)   ("live or die together")
    p ∤ d, d^2 == D (p) :  bp = (1 - (2 rho - 1)/p)/(1 - 2 rho/p)
  (Claude's phi_p(d) = (1 - (2 rho - c_d)/p)/(1 - rho/p)^2; our ap, bp are
   the same factors re-based against C_p so the per-d sieve is O(W loglog W).)

FROZEN CONVENTIONS (stated before running, house rule):
  C1. p = 2 by EXACT count over t mod 4: phi_2(d) = 2 if 4|d, 1 if d odd,
      0 if d == 2 mod 4  (independent of c; "neutral on start columns").
      Derived by direct enumeration: N(t) mod 2 has pattern [c,c,c+1,c+1].
  C2. Odd p with rho(p) = 0 (inert): factor 1, skipped entirely.
  C3. p = 3 with D == 1 mod 3 (rho = 2 = p): generic base C_3 = -3 is not a
      valid density; EXCLUDED from G. Every d != 0 mod 3 is a common-root
      class (bp = 0) and d == 0 mod 3 gets A_3 = p/(p-rho) = 3 directly.
  C4. Common-root (pm-delta) terms applied for split primes p <= B2 = 1e5;
      primes p > B2 contribute ln factor <= omega(d^2-D)/p < 2e-4, neglected
      (bounded, stated). p|d factor ap applied EXACTLY for all p <= Wmax.
  C5. G computed over odd primes <= PG = 1e7 in float64; tail beyond 1e7 is
      O(sum rho^2/p^2) ~ 3e-8, neglected.
  C6. S(W) = 2 * sum_{0<d<W} (1 - d/W)(F[d] - 1)   [two-sided |d|, per handoff]
      slope per tenfold = difference quotient of S across adjacent decades.
      PREREG (a): |mean slope - (-2.565)| <= 0.171   (== 0.075 +/- 0.005 at
      pbar = 1/34.2; we report in these convention-free Delta-S units).
  C7. PREREG (b): variant with common-root terms OFF (bp = 1 for p >= 5;
      the forced p = 3, D == 1 mod 3 term is unremovable — those lanes are
      reported but flagged; count would go negative without it).
  C8. Sanity: f(t) = t (twin-prime series 2*C2*prod_{p|d}(p-1)/(p-2), phi_2 =
      2 on even d / 0 on odd) must give slope -ln(10) = -2.302585 per tenfold.
  C9. GLM ceiling: same machinery with all prime cut at P = 1000
      (G_trunc, ap, bp only from p <= 1000); r_trunc(W) = 1 + S_trunc/34.2
      compared to GLM's schedule cut-off curve; plateau = value where
      S_trunc stops growing.
"""

import json
import math
import os
import sys
import time

import numpy as np
from sympy import primerange

C2_TWIN = 0.6601618158468696
DECADES = [10**2, 10**3, 10**4, 10**5, 10**6, 10**7]
B2 = 10**5
PG = 10**7

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "lab", "PHASE11_calm_slope.json")


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# ---------------------------------------------------------------- Kronecker

def kronecker_table(D):
    """chi[a] = (D|a) for a mod 4|D|, 0 on non-units."""
    M = 4 * abs(D)
    chi = np.zeros(M, dtype=np.int64)
    chi[1 % M] = 1
    for a in range(2, M):
        if math.gcd(a, M) != 1:
            continue
        x, s = a, 1
        q = 2
        while x > 1:
            if x % q == 0:
                e = 0
                while x % q == 0:
                    x //= q
                    e += 1
                if q == 2:
                    if D % 2 == 0:
                        s = 0
                    elif e % 2 == 1:
                        s *= 1 if D % 8 in (1, 7) else -1
                elif e % 2 == 1:
                    L = pow(D % q, (q - 1) // 2, q)
                    s *= -1 if L == q - 1 else 1
            q += 1
        chi[a] = s
    return chi


def tonelli(n, p):
    """sqrt(n) mod p, p odd prime, n a QR mod p."""
    n, p = int(n % p), int(p)
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q, s = p - 1, 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m, c, t, r = s, pow(z, q, p), pow(n, q, p), pow(n, (q + 1) // 2, p)
    while t != 1:
        i, u = 1, t * t % p
        while u != 1:
            u = u * u % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m, c, t, r = i, b * b % p, t * b * b % p, r * b % p
    return r


# ---------------------------------------------------------------- core build

def build_F(c, Wmax, primes_odd, trunc=None, no_cd=False):
    """Pair-density array F[d], d = 0..Wmax (F[0] unused)."""
    D = 1 - 8 * c
    M = 4 * abs(D)
    chi = kronecker_table(D)
    special3 = (D % 3 == 1)

    plim = min(trunc, Wmax) if trunc else Wmax
    po = primes_odd[primes_odd <= plim]
    rho = 1 + chi[po % M]

    # --- G (generic-base product over odd primes <= plim) -----------------
    sel = rho > 0
    if special3:
        sel &= po != 3                      # C3: C_3 invalid when rho(3) = 2
    pp, rp = po[sel], rho[sel]
    lnC = np.log1p(-2.0 * rp / pp) - 2.0 * np.log1p(-rp / pp)
    G = float(np.exp(lnC.sum()))

    F = np.full(Wmax + 1, G)
    F[2::4] = 0.0                            # C1: d == 2 mod 4
    F[4::4] *= 2.0                           # C1: 4 | d

    sp = po[rho == 2]                        # split primes
    for p in sp:                             # p | d factor
        if p == 3:                           # C3
            F[3::3] *= 3.0
        else:
            F[p::p] *= (p - 2) / (p - 4)
    for p in po[rho == 1]:                   # p | D (rho = 1)
        F[p::p] *= (p - 1) / (p - 2)

    if not no_cd or special3:                # common-root classes pm delta
        for p in sp:
            if p > B2:
                break
            if no_cd and p >= 5:             # C7: bp off for p >= 5
                continue
            dl = tonelli(D, p)
            bp = (p - 3) / (p - 4)           # = 0 for p = 3
            F[dl::p] *= bp
            F[p - dl::p] *= bp
    return F


def S_curve(F, decades=DECADES):
    """S(W) = 2 * sum_{0<d<W} (1 - d/W)(F[d]-1) at each decade."""
    Wmax = len(F) - 1
    d = np.arange(1, Wmax)
    x = F[1:Wmax] - 1.0
    X = np.cumsum(x)
    DX = np.cumsum(d * x)
    out = {}
    for W in decades:
        if W > Wmax:
            continue
        out[str(W)] = float(2.0 * (X[W - 2] - DX[W - 2] / W))
    return out


def slopes(S):
    ds = sorted(int(w) for w in S)
    return {f"{a}->{b}": (S[str(b)] - S[str(a)]) for a, b in zip(ds, ds[1:])}


# ---------------------------------------------------------------- sanity

def sanity_linear(Wmax, primes_odd):
    """f(t) = t: twin-prime pair series. Must slope -ln10 per tenfold."""
    F = np.zeros(Wmax + 1)
    F[2::2] = 2 * C2_TWIN
    for p in primes_odd:
        if p > Wmax:
            break
        F[p::p] *= (p - 1) / (p - 2)
    return F


# ---------------------------------------------------------------- main

def main():
    t0 = time.time()
    smoke = os.environ.get("PHASE11_SMOKE") == "1"
    Wmax = 10**5 if smoke else 10**7
    lanes = [14, 39] if smoke else [14 + 25 * k for k in range(12)]
    quick_lanes = [] if smoke else [14 + 5 * k for k in range(60)]

    log(f"start  Wmax={Wmax}  lanes={lanes}")
    primes_odd = np.array(list(primerange(3, Wmax + 1)), dtype=np.int64)
    log(f"primes to {Wmax}: {len(primes_odd)}")

    res = {"conventions": "C1-C9 frozen in script header", "Wmax": Wmax}

    F = sanity_linear(Wmax, primes_odd)
    S = S_curve(F)
    sl = slopes(S)
    res["sanity_linear"] = {"S": S, "slopes": sl,
                            "mean_slope": float(np.mean(list(sl.values())))}
    log(f"sanity f(t)=t: S(1e2)={S.get('100'):.4f} slopes={ {k: round(v,4) for k,v in sl.items()} }")

    lane_res = {}
    for c in lanes:
        for tag, kw in [("full", {}), ("no_cd", {"no_cd": True})]:
            F = build_F(c, Wmax, primes_odd, **kw)
            S = S_curve(F)
            sl = slopes(S)
            lane_res.setdefault(str(c), {})[tag] = {
                "S": S, "slopes": sl,
                "mean_slope": float(np.mean(list(sl.values()))),
                "forced_p3": (1 - 8 * c) % 3 == 1,
            }
        log(f"lane c={c} done ({time.time()-t0:.0f}s)")
        res["lanes"] = lane_res
        tmp = OUT + ".tmp"
        json.dump(res, open(tmp, "w"), indent=1)
        os.replace(tmp, OUT)

    if quick_lanes:
        qres = {}
        for c in quick_lanes:
            r = {}
            for tag, kw in [("full", {}), ("no_cd", {"no_cd": True})]:
                F = build_F(c, 10**6, primes_odd, **kw)
                S = S_curve(F, [10**2, 10**3, 10**4, 10**5, 10**6])
                sl = slopes(S)
                r[tag] = {"mean_slope": float(np.mean(list(sl.values()))),
                          "forced_p3": (1 - 8 * c) % 3 == 1}
            qres[str(c)] = r
        res["quick_60_lanes_W1e6"] = qres
        json.dump(res, open(OUT, "w"), indent=1)
        ms = [v["full"]["mean_slope"] for v in qres.values()]
        log(f"60-lane dispersion: mean={np.mean(ms):.4f} sd={np.std(ms):.4f} "
            f"min={min(ms):.4f} max={max(ms):.4f}")

    # GLM ceiling: truncate all prime structure at P = 1000
    F = build_F(14, Wmax, primes_odd, trunc=1000)
    S = S_curve(F)
    res["glm_trunc_1000_lane14"] = {
        "S": S,
        "r_pbar34.2": {w: 1 + s / 34.2 for w, s in S.items()},
        "r_pbar29.2": {w: 1 + s / 29.2 for w, s in S.items()},
        "growth_1e6_to_1e7": (S.get("10000000", 0) - S.get("1000000", 0)) or None,
    }
    json.dump(res, open(OUT, "w"), indent=1)
    log(f"GLM trunc: { {w: round(1+s/34.2,4) for w,s in S.items()} }")
    log(f"done in {time.time()-t0:.0f}s -> {OUT}")


if __name__ == "__main__":
    main()
