#!/usr/bin/env python3
"""
column_law.py — the resonant-column law of the wheel's polar lattice.

Sylvan's observation (2026-10-09, wheel.html close-look at 680 layers):
the wheel's radial columns are rational poles (labels k/m in lowest terms),
"the 2-prime rows bottom out", primes sit in the gaps and "snake between".

Mechanism question: WHICH columns can hold a prime at all, independent of
occlusion? Claim to test, calls written BEFORE running:

C1 [F]: gcd(k, m) >= 2  ==>  N = T(m-1)+k composite,
      EXCEPT the parity escape: gcd = 2 with m ≡ 2 (mod 4) (then N odd).
      Reason: d = gcd(k,m); d odd  ==> d | m(m-1)/2 and d | k  ==> d | N.
      d even >= 4 ==> N ≡ d/2 (mod d) ==> (d/2) | N, d/2 >= 2.
      d = 2: N even iff m(m-1)/2 even iff m ≡ 0 or 1 (mod 4)... precisely
      m ≡ 0 (mod 4): m/2 even -> product even -> N even. m odd: d=2 can't
      divide m. m ≡ 2 (mod 4): m/2 odd, m-1 odd -> product ODD -> N = odd
      + even = odd -> PARITY ESCAPE (e.g. m=6, k=2 -> N=17, prime).
      Expected exceptions: exactly {(m=2, k=2, N=3)}.

C2 [F]: every prime N = T(m-1)+k in laps >= 3 has gcd(k,m) = 1, or
      (gcd = 2 and m ≡ 2 mod 4). (value-side ground truth via sympy;
      the pattern-side equivalence uncovered<=>prime was proved earlier
      today — this is the converse direction as a census.)
      Expected violations: 0.

C3: habitat census — primes by eligibility class, with class sizes, so
    enrichment is measurable.

C4 (measurement, NO sign pre-claimed): relocation — for each prime at
    layer m, does layer m+1 have a prime in the same angular column
    (k' = round(k*(m+1)/m) ± 1)? Rate vs the eligible-tick base rate.

C5 (measurement, NO sign pre-claimed): strip offset — for eligible ticks,
    distance to nearest low-denominator pole (b <= 12) in tick units;
    prime rate near-strip vs far.
"""

import math
from sympy import isprime

M_LO, M_HI = 3, 3000


def T(n):
    return n * (n + 1) // 2


def eligible(k, m):
    """Column can hold a prime at all (algebraic eligibility)."""
    d = math.gcd(k, m)
    if d == 1:
        return True
    return d == 2 and m % 4 == 2


print("=== C1: forced-compositeness audit (no primality test used) ===")
exc = []
for m in range(2, M_HI + 1):
    base = T(m - 1)
    for k in range(1, m + 1):
        d = math.gcd(k, m)
        if d < 2 or eligible(k, m):
            continue
        N = base + k
        ok = (N % d == 0 and N > d) or (N % 2 == 0 and N > 2) or (
            d % 2 == 0 and N % (d // 2) == 0 and N > d // 2)
        if not ok:
            exc.append((m, k, d, N))
print(f"audited m=2..{M_HI}; forced-composite exceptions: {exc}")

print("\n=== C2: prime census by eligibility class (sympy ground truth) ===")
class_primes = {"coprime": 0, "gcd2_m2mod4": 0, "ineligible": 0}
class_sizes = {"coprime": 0, "gcd2_m2mod4": 0}
violations = []
first_examples = []
for m in range(M_LO, M_HI + 1):
    base = T(m - 1)
    for k in range(1, m + 1):
        d = math.gcd(k, m)
        if d == 1:
            class_sizes["coprime"] += 1
        elif d == 2 and m % 4 == 2:
            class_sizes["gcd2_m2mod4"] += 1
        N = base + k
        if isprime(N):
            if d == 1:
                class_primes["coprime"] += 1
                if len(first_examples) < 8:
                    first_examples.append(("coprime", m, k, N))
            elif d == 2 and m % 4 == 2:
                class_primes["gcd2_m2mod4"] += 1
                if len(first_examples) < 16:
                    first_examples.append(("gcd2_m2mod4", m, k, N))
            else:
                class_primes["ineligible"] += 1
                violations.append((m, k, d, N))
tot_p = sum(class_primes.values())
print(f"laps {M_LO}..{M_HI}: total primes found = {tot_p}")
for c in ("coprime", "gcd2_m2mod4", "ineligible"):
    sz = class_sizes.get(c, sum(m for m in range(M_LO, M_HI + 1)) )
    print(f"  {c:14s} primes={class_primes[c]:7d}  "
          f"prime-density-in-class: "
          f"{class_primes[c]/max(1,class_sizes.get(c,1)):.6f} "
          f"(class ticks: {class_sizes.get(c,'?')})")
print(f"  violations (prime in ineligible column): {violations}")

print("\n=== C4: relocation to next layer, same angular column ===")
hits = 0
tot = 0
expected_hits = 0.0
for m in range(M_LO, M_HI):
    base = T(m - 1)
    primes_m = [k for k in range(1, m + 1) if eligible(k, m)
                and isprime(base + k)]
    base1 = T(m)
    eligible_next = [k for k in range(1, m + 2) if eligible(k, m + 1)]
    p_next = sum(1 for k in eligible_next if isprime(base1 + k))
    rate = p_next / max(1, len(eligible_next))
    for k in primes_m:
        kc = k * (m + 1) / m
        window = [kk for kk in range(1, m + 2)
                  if abs(kk - kc) <= 1.0001]
        tot += 1
        expected_hits += rate * len(window)
        if any(isprime(base1 + kk) for kk in window):
            hits += 1
print(f"primes followed: {tot}; same-column prime next layer: {hits} "
      f"({hits/tot:.4f}); random-expectation ~{expected_hits:.1f} "
      f"({expected_hits/tot:.4f})")

print("\n=== C5: prime rate vs distance to nearest low-denominator pole ===")
near_hits = near_tot = far_hits = far_tot = 0
for m in range(M_LO, 1500):
    base = T(m - 1)
    for k in range(1, m + 1):
        if not eligible(k, m):
            continue
        dmin = min(
            min(abs(k * b - a * m) for a in range(0, k * b // m + 2)) / b
            for b in range(2, 13)
        )
        p = isprime(base + k)
        if dmin <= 1.5:
            near_tot += 1
            near_hits += p
        else:
            far_tot += 1
            far_hits += p
print(f"near-strip (<=1.5 ticks from a pole, b<=12): "
      f"{near_hits}/{near_tot} = {near_hits/max(1,near_tot):.6f}")
print(f"far-from-strip: {far_hits}/{far_tot} = "
      f"{far_hits/max(1,far_tot):.6f}")

print("\nexamples:", first_examples)
