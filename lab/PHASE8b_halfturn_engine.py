#!/usr/bin/env python3
"""PHASE 8b — the exact half-turn engine at general coprime a/b.

Tests, per ratio, which structure is generic and which is ratio-specific:
  1. Closed form H(m) = (a m^2 + 2 S(m) + c(m)) / (2b),
     c(j) = b L(j) - a j, S(m) = sum_{j<m} c(j)   [symbolic identity, exact]
  2. Existence lattice: L[m] even is periodic mod 2b (which classes?)
  3. Fine lock: parity of n = B[m] + L[m]/2 -- period 2b or 4b?
  4. Per eligible class mod 4b: H_r(t) exact quadratic, discriminant Delta;
     square Delta -> algebraically dead; non-square -> live family.
  5. Dial sweep: singular series (brute, p<2000) of every live family.
     High C anywhere = the 5:4 phenomenon is generic, not special.

CPU only, Fraction exact arithmetic. Reproduces every number.
"""
from fractions import Fraction as F
from math import isqrt, log
from sympy import primerange

def make_wheel(a, b):
    def L(m): return max(1, (2*a*m + b)//(2*b))
    return L

def analyze(a, b, M=None, psweep=2000):
    L = make_wheel(a, b)
    if M is None: M = 64*b
    # cumulative B and S
    c = [0]*(M+2); S = [0]*(M+2); Bv = [0]*(M+2)
    for j in range(1, M+2):
        c[j] = b*L(j) - a*j
    for j in range(1, M+2):
        S[j+1 if j+1 <= M+1 else M+1] = 0  # placeholder
    S[1] = 0; Bv[1] = 0
    for m in range(1, M+1):
        S[m+1] = S[m] + c[m]
        Bv[m+1] = Bv[m] + L(m)

    # 1) closed form on even-L layers
    bad = 0
    for m in range(1, M+1):
        if L(m) % 2 == 0:
            H = Bv[m] + L(m)//2
            Hcf = F(a*m*m + 2*S[m] + c[m], 2*b)
            if Hcf.denominator != 1 or Hcf.numerator != H:
                bad += 1
                if bad <= 3: print(f"    closed-form FAIL a/b={a}/{b} m={m}: {H} vs {Hcf}")
    cf_ok = bad == 0

    # 2) existence classes mod 2b (m >= b to skip the max(1,) floor)
    even_cls = sorted({m % (2*b) for m in range(b, M+1) if L(m) % 2 == 0})

    # 3) fine lock: parity of n over even-L classes; lift to mod 4b
    par2 = {}
    for m in range(b, M+1):
        if L(m) % 2 == 0:
            par2.setdefault(m % (2*b), set()).add((Bv[m] + L(m)//2) % 2)
    split = {r: v for r, v in par2.items() if len(v) == 2}   # needs mod 4b
    elig2 = sorted(r for r, v in par2.items() if v == {1})   # n odd throughout
    elig4 = sorted({m % (4*b) for m in range(b, M+1)
                    if L(m) % 2 == 0 and (Bv[m] + L(m)//2) % 2 == 1})
    n2 = [(m, Bv[m]+L(m)//2) for m in range(1, 4*b+1)
          if L(m) % 2 == 0 and Bv[m]+L(m)//2 == 2]

    # 4) per eligible mod-4b class: exact quadratic + discriminant
    def quad_on_class(r, mod):
        pts = []
        t = 0
        while r + mod*t <= M and len(pts) < 5:
            m = r + mod*t
            if L(m) % 2 == 0:
                pts.append((F(t), F(Bv[m] + L(m)//2)))
            t += 1
        if len(pts) < 3: return None
        (x1,y1),(x2,y2),(x3,y3),(x4,y4),(x5,y5) = pts
        # fit A,B,C from first three, verify rest
        A = ( (y2-y1)*(x1-x3) - (y3-y1)*(x1-x2) ) / ( (x2*x2-x1*x1)*(x1-x3) - (x3*x3-x1*x1)*(x1-x2) )
        Bb = (y2-y1 - A*(x2*x2-x1*x1)) / (x2-x1)
        Cc = y1 - A*x1*x1 - Bb*x1
        ok = all(A*x*x+Bb*x+Cc == y for x, y in pts)
        D = Bb*Bb - 4*A*Cc
        Di = D.numerator//D.denominator if D.denominator == 1 else None
        isq = Di is not None and Di >= 0 and isqrt(Di)**2 == Di
        return (A, Bb, Cc, D, ok)

    families = []
    for r4 in elig4:
        q = quad_on_class(r4, 4*b)
        if q is None: continue
        A, Bb, Cc, D, ok = q
        families.append((r4, A, Bb, Cc, D, ok))

    # 5) singular series for live (non-square-D) families
    def sing_series(A, Bb, Cc):
        C = 1.0
        for p in primerange(2, psweep):
            rho = 0
            Av, Bv2, Cv = A.numerator, Bb.numerator, Cc.numerator
            den = A.denominator * Bb.denominator * Cc.denominator
            if den != 1: return None   # non-integer-valued family; skip
            for t in range(p):
                if (Av*t*t + Bv2*t + Cv) % p == 0: rho += 1
            C *= (1 - rho/p)/(1 - 1/p)
        return C

    live = []
    for r4, A, Bb, Cc, D, ok in families:
        Di = D.numerator if D.denominator == 1 else -1
        isq = Di >= 0 and isqrt(Di)**2 == Di if Di >= 0 else False
        if isq: continue
        C = sing_series(A, Bb, Cc)
        live.append((r4, Di, C))

    return dict(cf_ok=cf_ok, even_cls=even_cls, split=sorted(split),
                elig4=elig4, n2=n2, families=families, live=live)

RATIOS = [(5,4),(7,4),(9,4),(11,4),(3,2),(5,2),(7,2),(5,3),(7,3),(8,3),
          (4,3),(5,3),(7,5),(9,5),(11,5),(5,6),(7,6),(5,8),(7,8),(9,8)]

if __name__ == "__main__":
    print(f"{'a/b':>6} | cf | even-L mod 2b | split mod 2b | elig mod 4b | n=2 | live families (r4, D, C)")
    for a, b in RATIOS:
        r = analyze(a, b)
        live_s = ", ".join(f"({r4},{D},{C:.2f})" if C else f"({r4},{D},?)"
                           for r4, D, C in r["live"])
        print(f"{a}/{b:>2} | {'OK' if r['cf_ok'] else 'XX'} | {r['even_cls']} | {r['split']} | "
              f"{r['elig4']} | {r['n2']} | {live_s}")
