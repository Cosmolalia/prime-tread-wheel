#!/usr/bin/env python3
"""
PHASE 20 — morning-relay adjudication probes, 2026-10-14.

Leg A — GLM F5 normalization rescoring (the [G] -> formula fix).
Leg B — all-inert discriminant scan |D| <= 1e6 (GLM F6b / creep precondition).
Leg C — two-shot localization: wheel vs Sacks spokes (GLM's theorem §2,
        hand-anchored instance + C-blocked-depths table).
Leg D — Gemini leave-one-ring-out variance control (GPT audit request #6,
        Theorem Q2 same-layer control).
Leg E — Phi_a phase-space conjugacy orbit-size check (GPT audit request #4).
"""
import math
from math import isqrt

OUT = {}

def primes_upto(n):
    s = bytearray(b"\x01") * (n + 1)
    s[:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if s[p]:
            s[p*p::p] = b"\x00" * ((n - p*p)//p + 1)
    return [p for p in range(2, n + 1) if s[p]]

T = lambda n: n*(n+1)//2

# ---------------- Leg A ----------------
def legA():
    ds = {263: 15, 300: 16, 400: 19, 600: 26, 1000: 37}
    rows = []
    for m, d in ds.items():
        pred_old = m / (4*math.log(m))          # the wrong-log formula
        pred_new = 0.5*m / math.log(T(m))       # GLM F5: 0.5*m/ln T(m)
        rows.append(dict(m=m, d=d, pred_old=round(pred_old,2),
                         pred_new=round(pred_new,2),
                         resid_new=round(d-pred_new,2)))
    OUT["A"] = rows
    print("LEG A — F5 rescoring (d - 0.5*m/ln T(m)):")
    for r in rows:
        print(f"  m={r['m']:>5} d={r['d']:>3} pred_new={r['pred_new']:>7} resid={r['resid_new']:>6}")

# ---------------- Leg B ----------------
def kronecker(a, p):
    """(a|p), p odd prime."""
    a %= p
    if a == 0: return 0
    r = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if p % 8 in (3, 5): r = -r
        a, p = p, a
        if a % 4 == 3 and p % 4 == 3: r = -r
        a %= p
    return r if p > 1 else 0

def legB():
    odd67 = [p for p in primes_upto(67) if p != 2]
    witnesses = []
    for D in range(-10**6, 10**6 + 1):
        if D in (0, 1): continue
        if all(kronecker(D, p) == -1 for p in odd67):
            witnesses.append(D)
            if len(witnesses) >= 20: break
    OUT["B"] = {"odd_primes": odd67, "witnesses": witnesses}
    print(f"LEG B — all-inert D-scan |D|<=1e6 over {len(odd67)} odd primes <=67:")
    print(f"  witnesses found: {witnesses if witnesses else 'NONE'}")

# ---------------- Leg C ----------------
def sacks_value(m, a, b):
    """Sacks: turn m = ticks 1..2m+1, value (m-1)^2 + j, j = a*(2m-1)/b (integer when b|2m-1)."""
    j = a*(2*m - 1)//b
    return (m-1)**2 + j

def wheel_value(m, a, b):
    """Wheel: turn m, tick j = a*m/b (b|m), value T(m-1)+j."""
    return T(m-1) + a*m//b

def legC():
    s = bytearray(b"\x01")*(200000+1)
    s[:2] = b"\x00\x00"
    for p in range(2, isqrt(200000)+1):
        if s[p]: s[p*p::p] = b"\x00"*(((200000-p*p)//p)+1)
    isprime = lambda v: s[v] == 1

    # hand-anchored instance: Sacks spoke 1/3
    b, m0 = 3, 2            # 2*m0 == 1 mod b
    w = (2*m0 - 1)//b
    C = (m0-1)**2 + 1*w
    anchor = []
    for g in range(0, 8):
        m = m0 + g*b
        v = sacks_value(m, 1, b)
        anchor.append(dict(g=g, depth=g+1, m=m, value=v,
                           prime=bool(isprime(v)), g_div_C=(g != 0 and C % g == 0)))
    OUT["C_anchor"] = {"C": C, "anchor": anchor}
    print(f"LEG C — Sacks spoke 1/3: C={C}, N_g=9g^2+8g+2")
    for r in anchor:
        print(f"  g={r['g']} depth={r['depth']} m={r['m']:>3} N={r['value']:>4} "
              f"prime={r['prime']} g|C={r['g_div_C']}")

    # C-blocked-depths table: Sacks spokes a/b, b odd, a<b, gcd(a,b)=1
    table = []
    for b in [3, 5, 7, 9, 11]:
        m0 = next(m for m in range(1, b+1) if (2*m - 1) % b == 0)
        w = (2*m0 - 1)//b
        for a in range(1, b):
            if math.gcd(a, b) != 1: continue
            C = (m0-1)**2 + a*w
            # blocked depths where g|C (g>=1); wheel blocks every depth >=3
            blocked = sorted({g+1 for g in range(1, 200) if C % g == 0})
            live_primes = []
            for g in range(0, 200):
                depth = g+1
                if depth >= 3 and (g == 0 or C % g == 0):
                    continue  # forced composite (g|C) — GLM's criterion
                m = m0 + g*b
                v = sacks_value(m, a, b)
                if v > 200000: break
                if isprime(v):
                    live_primes.append((depth, v))
            table.append(dict(spoke=f"{a}/{b}", C=C, blocked_depths=blocked[:12],
                              max_prime_depth=max((d for d,_ in live_primes), default=None),
                              n_primes_deep=len([1 for d,_ in live_primes if d >= 3])))
    OUT["C_table"] = table
    print("LEG C — C-blocked-depths table (Sacks):")
    for r in table:
        print(f"  spoke {r['spoke']:>4} C={r['C']:>5} blocked_depths={r['blocked_depths']} "
              f"primes at depth>=3: {r['n_primes_deep']} max_prime_depth={r['max_prime_depth']}")

    # wheel contrast: same-shape spokes on the wheel (b|m)
    wtab = []
    for b in [3, 5, 7, 9, 11]:
        for a in range(1, b):
            if math.gcd(a, b) != 1: continue
            deep_primes = 0
            maxd = None
            for g in range(0, 200):
                m = g*b
                if m < 2: continue
                v = wheel_value(m, a, b)
                if v > 200000: break
                if g+1 >= 3 and isprime(v):
                    deep_primes += 1
                    maxd = g+1
            wtab.append(dict(spoke=f"{a}/{b}", deep_primes_ge3=deep_primes, max_prime_depth=maxd))
    OUT["C_wheel"] = wtab
    bad = [r for r in wtab if r["deep_primes_ge3"] > 0]
    print(f"LEG C — wheel spokes: deep primes (depth>=3) found: {sum(r['deep_primes_ge3'] for r in wtab)} "
          f"across {len(wtab)} spokes; violations: {bad if bad else 'NONE'}")

# ---------------- Leg D ----------------
def legD():
    res = []
    for p in [11, 97, 257]:
        m0 = next(m for m in range(2, 5*p) if isqrt(T(m-1)) >= p)
        assert isqrt(T(m0-2)) < p
        base = T(m0-1)
        rings = [q for q in primes_upto(isqrt(base)) ]
        rings_with = rings  # includes p by construction
        rings_without = [q for q in rings if q != p]
        def gaps_var(ringset):
            ks = [k for k in range(1, m0+1)
                  if all((base+k) % q for q in ringset)]
            if len(ks) < 3: return None, ks
            gaps = [b-a for a, b in zip(ks, ks[1:])]
            mean = sum(gaps)/len(gaps)
            var = sum((g-mean)**2 for g in gaps)/len(gaps)
            return var, ks
        vw, ks_w = gaps_var(rings_with)
        vwo, ks_wo = gaps_var(rings_without)
        res.append(dict(p=p, m0=m0, V_with=round(vw,4), V_without=round(vwo,4),
                        Delta=round(vw-vwo,4) if vw is not None and vwo is not None else None,
                        n_holes_with=len(ks_w), n_holes_without=len(ks_wo)))
    OUT["D"] = res
    print("LEG D — leave-one-ring-out gap-variance control (Gemini):")
    for r in res:
        print(f"  p={r['p']:>3} m0={r['m0']:>3} V_with={r['V_with']:>9} V_without={r['V_without']:>9} "
              f"Delta={r['Delta']:>9} holes {r['n_holes_without']}->{r['n_holes_with']}")

# ---------------- Leg E ----------------
def legE():
    def orbit_sizes(a):
        out = {}
        for p in [3, 5, 7, 11, 13, 17]:
            orig = { (m*m - m + 2) % p for m in range(p) }
            scaled = { (a*(m*m - m + 2)) % p for m in range(p) }
            out[p] = (len(orig), len(scaled))
        return out
    res = {a: orbit_sizes(a) for a in [1, 7]}
    OUT["E"] = {str(a): {str(k): list(v) for k, v in d.items()} for a, d in res.items()}
    print("LEG E — Phi_a orbit sizes (orig, scaled) for a=1,7:")
    for a in [1, 7]:
        print(f"  a={a}: " + "  ".join(f"p={p}:{s}" for p, s in res[a].items()))

if __name__ == "__main__":
    legA(); legB(); legC(); legD(); legE()
    import json
    with open("lab/PHASE20_relay_oct14.json", "w") as f:
        json.dump(OUT, f, indent=1)
    print("wrote lab/PHASE20_relay_oct14.json")
