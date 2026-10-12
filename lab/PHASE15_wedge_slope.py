#!/usr/bin/env python3
"""
PHASE 15 — wedge slope: why d ~ m/13.5?  (part 1: mechanism test, no MILP)

Context: the object-A d-curve (PHASE14_objA_dcurve.json, 244 finite layers
14..257) fits d ~ 0.0747*m + 0.54. The object-C (prime-layer) curve fits
~0.0737*m + 0.64. The open question from the 10-12 handback queue is: why
that slope? GPT's frame: CRT Hamming distance. Candidate mechanism [S->test]:

  A tick j whose VALUE T(m-1)+j is prime > 97 cannot be covered by any ring
  at home phase (home covers exactly the values divisible by p). Covering it
  requires a ring p with p | (T+j), hence p = T+j (prime > 97 => its only
  prime factor is itself) at phase (j+T) % p = 0... wait: p = T+j > T+m for
  m < p is impossible; see below. More precisely: since T+j is prime and the
  ring primes are <= 97, NO ring can cover tick j at any phase unless the
  ring p equals T+j. Rings are fixed <= 97, and T+j > 97 always. Therefore
  prime-valued ticks are UNCOVERABLE -- they force d = None?!

  That cannot be right, because d was finite everywhere 14..257. RESOLUTION
  to check: 'all' object ticks are j in 1..m; value = T + j. For m <= 257,
  T(256) = 32640; T+j up to ~32897, which HAS prime factors > 97, but the
  covering ring only needs p <= 97 dividing the value. A prime value > 97
  has no such factor => that tick is uncoverable by ANY phase choice =>
  d = None. Since A2 measured finite d everywhere <= 257, it must be that
  no layer 14..257 contains a prime value in (T, T+m]... which is exactly
  the claim "no prime in the short interval (T(m-1), T(m-1)+m]" -- FALSE
  in general (e.g. m=5, T=10, interval (10,15], 11,13 prime!). Check m=5:
  PHASE14 measured d(5)=0 (home-cover, smooth(11)? 11 <= 97 => smooth True).
  AH: smooth(n,B) returns True for n <= B. So values <= 97 are "covered"
  by convention. Prime values in (T, T+m] that are > 97: e.g. m=14, T=91,
  values 92..105: 97 is prime, 97 <= 97 => smooth. m=20, T=190, values
  191..210: 191,193,197 prime > 97 => those ticks uncoverable?!

  But PHASE14 measured d(20) = 3 (finite). CONTRADICTION? No -- solve_layer
  returns None only if MILP infeasible; but if tick 1 (value 191) is
  uncoverable, MILP must be infeasible... unless T+j for j=1 is 191 and no
  ring divides 191, so row for j=1 has all-zero coefficients => infeasible
  => None. Measured d(20)=3. So my value formula must be off, OR ticks with
  prime value > 97 simply don't occur because T+j in that range is never
  prime... no, 191 exists.

  => [G] flagged BEFORE running: reconcile "every tick 1..m coverable at
  some phase" with "prime value > 97 exists in layer". Resolution path: the
  MILP covers tick j by ring p iff c == (j+T) % p. For p not dividing T+j,
  phase (j+T)%p still EXISTS as a choice of c -- choosing ring p at phase
  c=(j+T)%p means ring p covers the class of ticks j' with j'+T == c mod p,
  i.e. j' == j mod p. It covers tick j REGARDLESS of whether p | T+j!
  Covering is about TICK congruence, not value divisibility. The connection:
  at home c=0, ring p covers ticks j == -T mod p, i.e. values T+j == 0 mod p.
  So any ring at the right phase covers any single tick. Prime-valued ticks
  are just not coverable AT HOME. FINE -- no contradiction. The candidate
  mechanism survives: prime-valued ticks are exactly the ticks NOT covered
  at home; each needs some ring displaced onto its class; one displaced ring
  p at phase c covers ~m/p ticks but destroys home coverage of the class
  j == -T mod p (whose values are the p-multiples).

FROZEN PREDICTIONS (before running):
  H1: d_A(m) correlates with P(m) = #{j in 1..m : T+j prime} (prime-value
      tick count) with r >= 0.98 over the 244 finite layers.
  H2: d_A(m) = kappa * P(m) + b with kappa in [0.7, 1.1] (one ring can
      harvest several prime ticks if they collide mod p; overlap costs
      home coverage, so kappa <= 1 expected).
  H3: d_A(m)/m is NOT constant; it tracks 1/(2 ln m) * kappa -- i.e. the
      apparent constant slope 0.0747 is the windowed average of a slowly
      declining ratio. Fit residual comparison: linear-in-m vs linear-in-P.
  H4 (object C): d_C(m) tracks P_C(m) = #{eligible j : T+j prime} the same
      way on odd prime layers (m in J1C_spectrum_v2 'prime' with finite d).
  H5: m=55 (GLM's integrality-gap specimen) is NOT an outlier under the
      P(m) model (the gap is in the integer program, not the counting).
"""
import json
import numpy as np
from math import isqrt

LIMIT = 391 * 392 // 2 + 8
comp = bytearray(LIMIT)
comp[0] = comp[1] = 1
for p in range(2, isqrt(LIMIT) + 1):
    if not comp[p]:
        comp[p * p::p] = b'\x01' * (((LIMIT - 1 - p * p) // p) + 1)


def is_prime(n):
    return n >= 2 and not comp[n]


def T(m):
    return m * (m - 1) // 2


def main():
    dA = json.load(open('lab/PHASE14_objA_dcurve.json'))['d']
    rows = []
    for ms, dv in dA.items():
        m, d = int(ms), dv
        if d is None or m < 14:
            continue
        P = sum(1 for j in range(1, m + 1) if is_prime(T(m) + j))
        rows.append((m, d, P))
    m = np.array([r[0] for r in rows], float)
    d = np.array([r[1] for r in rows], float)
    P = np.array([r[2] for r in rows], float)

    r_dP = np.corrcoef(d, P)[0, 1]
    A = np.vstack([P, np.ones_like(P)]).T
    kappa, b = np.linalg.lstsq(A, d, rcond=None)[0]
    pred = kappa * P + b
    resid_P = d - pred
    ss_res_P = float((resid_P ** 2).sum())
    ss_tot = float(((d - d.mean()) ** 2).sum())

    # H6: rough-count model. U(m) = #{j : T+j has NO prime factor <= 97}
    # (the 97-rough values: primes > 97 and semiprimes with both factors >
    # 97). These are exactly the ticks not covered at home phase.
    PR97 = [p for p in range(2, 98) if all(p % q for q in range(2, isqrt(p) + 1))]

    def home_covered(n):
        """True iff some prime <= 97 divides n (or n <= 97). This is the
        correct home-cover predicate: ring p at home phase c=0 covers exactly
        the ticks whose value is divisible by p. (An earlier version tested
        97-SMOOTHNESS -- all factors <= 97 -- which miscounts e.g. 2*500021
        as 'rough'; caught by the density sanity check, ~0.89 vs the true
        97-rough density e^{-gamma}/ln 97 ~ 0.123.)"""
        if n <= 97:
            return True
        for p in PR97:
            if n % p == 0:
                return True
        return False
    U = np.array([sum(1 for j in range(1, int(mm) + 1)
                      if not home_covered(T(int(mm)) + j)) for mm in m], float)
    r_dU = np.corrcoef(d, U)[0, 1]
    kU, bU = np.linalg.lstsq(np.vstack([U, np.ones_like(U)]).T, d, rcond=None)[0]
    predU = kU * U + bU
    ss_res_U = float(((d - predU) ** 2).sum())

    A2 = np.vstack([m, np.ones_like(m)]).T
    s_lin, b_lin = np.linalg.lstsq(A2, d, rcond=None)[0]
    resid_m = d - (s_lin * m + b_lin)
    ss_res_m = float((resid_m ** 2).sum())

    print(f"H6 rough-count U: r(d,U) = {r_dU:.5f} kappa_U = {kU:.4f} "
          f"b_U = {bU:.3f} R^2 = {1 - ss_res_U/ss_tot:.5f} -> "
          f"{'PASS (beats m-linear)' if ss_res_U < ss_res_m else 'FAIL vs m-linear'}")
    # combined model d ~ a*U + c*m
    Ac = np.vstack([U, m, np.ones_like(m)]).T
    coef, *_ = np.linalg.lstsq(Ac, d, rcond=None)
    ss_res_c = float(((d - Ac @ coef) ** 2).sum())
    print(f"    combined d ~ {coef[0]:.4f}*U + {coef[1]:.5f}*m + {coef[2]:.3f}"
          f"  R^2 = {1 - ss_res_c/ss_tot:.5f}")

    ratio = d / np.maximum(P, 1)
    print(f"layers: {len(rows)}")
    print(f"H1 r(d,P) = {r_dP:.5f}  -> {'PASS' if r_dP >= 0.98 else 'FAIL'}")
    print(f"H2 kappa = {kappa:.4f}  b = {b:.3f} -> "
          f"{'PASS' if 0.7 <= kappa <= 1.1 else 'FAIL'}")
    print(f"H3 R^2(P-model) = {1 - ss_res_P/ss_tot:.5f}  "
          f"R^2(m-linear) = {1 - ss_res_m/ss_tot:.5f} -> "
          f"{'PASS' if ss_res_P < ss_res_m else 'FAIL'}")
    print(f"    slope-in-m fit: d = {s_lin:.5f}*m + {b_lin:.3f}")
    print(f"    d/P: min {ratio.min():.3f} max {ratio.max():.3f} "
          f"mean {ratio.mean():.3f}")
    for mm in (50, 100, 150, 200, 250):
        sel = np.abs(m - mm) <= 10
        if sel.any():
            print(f"    m~{mm}: mean d/P = {ratio[sel].mean():.3f} "
                  f"(1/(2 ln m) = {1/(2*np.log(mm)):.3f})")
    r55 = [r for r in rows if r[0] == 55]
    if r55:
        m55, d55, P55 = r55[0]
        print(f"H5 m=55: d={d55} P={P55} d/P={d55/P55:.3f} "
              f"model pred={kappa*P55+b:.2f} resid={d55-(kappa*P55+b):+.2f}")

    # H4: object C from J1C v2
    v2 = json.load(open('lab/J1C_spectrum_v2.json'))
    pc = v2.get('prime')
    if isinstance(pc, dict):
        rowsC = []
        for ms, dv in pc.items():
            m, d = int(ms), dv
            if d is None:
                continue
            Pc = 0
            for j in range(1, m + 1):
                import math
                g = math.gcd(j, m)
                if g == 1 and is_prime(T(m) + j):
                    Pc += 1
            rowsC.append((m, d, Pc))
        if len(rowsC) >= 10:
            mC = np.array([r[0] for r in rowsC], float)
            dC = np.array([r[1] for r in rowsC], float)
            PC = np.array([r[2] for r in rowsC], float)
            rC = np.corrcoef(dC, PC)[0, 1]
            kC, bC = np.linalg.lstsq(
                np.vstack([PC, np.ones_like(PC)]).T, dC, rcond=None)[0]
            print(f"H4 object C: n={len(rowsC)} r(d,P_C)={rC:.5f} "
                  f"kappa_C={kC:.4f} -> "
                  f"{'PASS' if rC >= 0.95 else 'FAIL'}")

    out = {'H1_r_dP': float(r_dP), 'H2_kappa': float(kappa),
           'H2_b': float(b), 'R2_P': 1 - ss_res_P/ss_tot,
           'R2_mlinear': 1 - ss_res_m/ss_tot,
           'slope_in_m': float(s_lin), 'rows': rows}
    with open('lab/PHASE15_wedge_slope.json', 'w') as f:
        json.dump(out, f, indent=1)


if __name__ == '__main__':
    main()
