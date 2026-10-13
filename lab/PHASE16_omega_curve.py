#!/usr/bin/env python3
"""
PHASE 16 — omega-degradation curve: the wedge slope as arithmetic, MILP-free.
Date: 2026-10-13. Artifacts: lab/PHASE16_omega_curve.py (+ .json, .log).

Frame (GLM CRT-shift collapse, audited STANDS 2026-10-13,
lab/GLM_COLLAPSE_AUDIT_2026-10-13.md):
  d(m) = |P| - max |S|, S = primes dividing the covering translate a.
So the measured wedge slope IS the omega-degradation rate of the optimal
translate, and "slope universality" + "why m/13.5" are the same question
at different ring bounds B (primes <= B).

This probe measures the curve at three ring bounds, no MILP:
  LEG A [E]  B=97: omega(m) = 25 - d(m) from the existing PHASE14 objA
             d-curve (MILP-measured, 244 layers 14..257). Zero new compute;
             the reference curve.
  LEG B      B=53 (16 primes, j(53#)=106): d(m) by the collapsed exact
             cover (copied verbatim from GLM_COLLAPSE_AUDIT LEG 3, which
             reproduced the HiGHS values to the unit).
  LEG C      B=31 (11 primes, j(31#)=58): same.
  LEG D      B=97 spot check at m=60: collapsed DFS vs the JSON d-curve
             (binds the two instruments at 25 rings).
  LEG E [E]  native schedule (rings = primes <= sqrt(T(m-1))): existing
             points m=263 (d=15, 42 rings, PHASE15_dynrings.md) and
             m=1000 (incumbent d=38, bound 32, PHASE15_sparse_m1000.log);
             native-schedule law d ~ 0.5*m/(2 ln m) check. m=300/400 are
             fired separately as sparse MILPs (lab/PHASE16_sparse_m*.log).
Per-B linear fit d ~ k_B * m + c_B; omega = |P| - d.

Frozen BEFORE running:
  F1  k_53 in [0.070, 0.090] and k_31 in [0.070, 0.095] (mechanism band
      0.215*e^-gamma/ln B + 0.051 gives 0.081 / 0.086; LEG S showed
      measured ABOVE prediction at small B, so bands are wide);
  F2  measured k_B >= 0.215*e^-gamma/ln B + 0.051 - 0.02 for B in
      {31, 53} (LEG S +2.2 offset direction);
  F3  LEG D: collapsed d(60; B=97) == JSON d-curve d(60) (instrument bind);
  F4  omega endpoints at B=97: omega(14) = 24, omega(257) = 3 (GLM's
      numbers, arithmetic from the JSON: 25 - d).
  F5  no monotone d claim (A4 froze scatter; only the fit is reported).
"""
import json
import math
import time
from itertools import combinations

E_GAMMA = 0.5614594835668851  # e^-gamma


def primes_upto(n):
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = [False] * len(sieve[i * i::i])
    return [i for i, v in enumerate(sieve) if v]


# ---- collapsed exact cover, verbatim from GLM_COLLAPSE_AUDIT_2026-10-13 ----


def cover_dfs(window, primes_free, uncovered):
    if not uncovered:
        return True, {}
    if not primes_free:
        return False, {}
    cap = 0
    for p in primes_free:
        cnt = {}
        for i in uncovered:
            cnt[window[i] % p] = cnt.get(window[i] % p, 0) + 1
        cap += max(cnt.values())
    if cap < len(uncovered):
        return False, {}
    p = primes_free[0]
    rest = primes_free[1:]
    scores = []
    for r in range(p):
        hit = frozenset(i for i in uncovered if window[i] % p == r)
        scores.append((len(hit), r, hit))
    scores.sort(reverse=True)
    for _, r, hit in scores:
        if not hit:
            continue
        ok, assign = cover_dfs(window, rest, uncovered - hit)
        if ok:
            assign[p] = r
            return True, assign
    return False, {}


class _Timeout(Exception):
    pass


def d_collapsed(m, prs, deadline=None):
    Q_note = "Q unused; feasibility checked externally via j(Q)"
    del Q_note
    T = (m - 1) * m // 2
    window = list(range(T + 1, T + 1 + m))
    n = len(prs)
    for s in range(n, -1, -1):
        for S in combinations(prs, s):
            if deadline and time.time() > deadline:
                raise _Timeout(f"m={m} s={s}")
            sset = set(S)
            home = frozenset(i for i in range(m)
                             if any(window[i] % p == 0 for p in sset))
            U = frozenset(set(range(m)) - set(home))
            free = [p for p in prs if p not in sset]
            ok, _ = cover_dfs(window, tuple(free), U)
            if ok:
                return n - s
    return None


def linfit(xs, ys):
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    k = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    c = (sy - k * sx) / n
    resid = max(abs(y - (k * x + c)) for x, y in zip(xs, ys))
    return k, c, resid


def mechanism_k(B):
    return 0.215 * E_GAMMA / math.log(B) + 0.051


def legA():
    d = json.load(open("lab/PHASE14_objA_dcurve.json"))["d"]
    pts = sorted((int(m), v) for m, v in d.items()
                 if v is not None and 14 <= int(m) <= 257)
    ms = [m for m, _ in pts]
    ds = [v for _, v in pts]
    om = [25 - v for v in ds]
    k, c, resid = linfit([float(m) for m in ms], [float(v) for v in ds])
    k_om, c_om, _ = linfit([float(m) for m in ms], [float(v) for v in om])
    return {"n": len(pts), "k_d": round(k, 5), "c_d": round(c, 3),
            "max_resid": round(resid, 2),
            "k_omega": round(k_om, 5), "omega0": round(c_om, 3),
            "omega14": 25 - d["14"], "omega257": 25 - d["257"]}


def run_bound(B, m_list, per_point_budget=900):
    prs = primes_upto(B)
    assert prs[-1] == B
    rows = {}
    for m in m_list:
        t0 = time.time()
        try:
            d = d_collapsed(m, prs, deadline=t0 + per_point_budget)
            status = "exact"
        except _Timeout:
            d, status = None, "timeout"
        rows[m] = {"d": d, "omega": (len(prs) - d) if d is not None else None,
                   "seconds": round(time.time() - t0, 1),
                   "status": status}
        print(f"  B={B} m={m}: d={d} ({status}, "
              f"{rows[m]['seconds']}s)", flush=True)
    ok = [(m, r["d"]) for m, r in rows.items() if r["d"] is not None]
    out = {"B": B, "nrings": len(prs), "rows": rows}
    if len(ok) >= 3:
        k, c, resid = linfit([float(m) for m, _ in ok],
                             [float(v) for _, v in ok])
        out.update({"k_d": round(k, 5), "c_d": round(c, 3),
                    "max_resid": round(resid, 2),
                    "k_mechanism_pred": round(mechanism_k(B), 5)})
    return out


def legD():
    d = json.load(open("lab/PHASE14_objA_dcurve.json"))["d"]
    prs = primes_upto(97)
    t0 = time.time()
    try:
        got = d_collapsed(60, prs, deadline=t0 + 1200)
    except _Timeout:
        got = "timeout"
    return {"json_d60": d["60"], "collapsed_d60": got,
            "bind": got == d["60"], "seconds": round(time.time() - t0, 1)}


def legE():
    pts = [{"m": 263, "d": 15, "nrings": 42, "src": "PHASE15_dynrings.md"},
           {"m": 1000, "d": 38, "nrings": 127, "status": "incumbent-bound32",
            "src": "PHASE15_sparse_m1000.log"}]
    for p in pts:
        p["law_pred"] = round(0.5 * p["m"] / (2 * math.log(p["m"])), 2)
        p["omega"] = p["nrings"] - p["d"]
        p["d_over_pred"] = round(p["d"] / p["law_pred"], 3)
    return pts


def main():
    t0 = time.time()
    print("LEG A — B=97 reference curve from JSON (no compute)", flush=True)
    A = legA()
    print(json.dumps(A), flush=True)

    print("LEG B — B=53 collapsed curve", flush=True)
    B53 = run_bound(53, [14, 20, 28, 36, 44, 52, 60, 72, 84, 96, 105])
    print("LEG C — B=31 collapsed curve", flush=True)
    B31 = run_bound(31, [14, 20, 28, 36, 44, 52, 57])

    print("LEG D — B=97 instrument bind at m=60", flush=True)
    D = legD()
    print(json.dumps(D), flush=True)

    E = legE()

    k97 = A["k_d"]
    verdict = {
        "F1_k53_in_band": (B53.get("k_d") is not None
                           and 0.070 <= B53["k_d"] <= 0.090),
        "F1_k31_in_band": (B31.get("k_d") is not None
                           and 0.070 <= B31["k_d"] <= 0.095),
        "F2_above_mechanism": all(
            B.get("k_d") is None or B["k_d"] >= B["k_mechanism_pred"] - 0.02
            for B in (B53, B31)),
        "F3_legD_bind": D["bind"] if isinstance(D["bind"], bool) else False,
        "F4_endpoints": A["omega14"] == 24 and A["omega257"] == 3,
    }
    out = {"legA_B97": A, "legB_B53": B53, "legC_B31": B31,
           "legD_bind": D, "legE_native": E,
           "slope_table": {
               "B31": B31.get("k_d"), "B53": B53.get("k_d"),
               "B97": k97,
               "mech_pred_B31": round(mechanism_k(31), 5),
               "mech_pred_B53": round(mechanism_k(53), 5),
               "mech_pred_B97": round(mechanism_k(97), 5)},
           "seconds": round(time.time() - t0, 1),
           "verdict": verdict}
    with open("lab/PHASE16_omega_curve.json", "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({"slope_table": out["slope_table"],
                      "verdict": verdict, "seconds": out["seconds"]},
                     indent=1), flush=True)


if __name__ == "__main__":
    main()
