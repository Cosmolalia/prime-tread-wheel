#!/usr/bin/env python3
"""
census.py — the quadratic-real-estate census.

Question: across ratios, which tick-line quadratics are LIVE (non-factorable),
how prime-rich are them, and is Euler's D=-163 class unique to 2:1 or the
local champion of a recurring family?

Wheel conventions (same as every probe): at integer ratio a, lap m has
L[m] = a*m ticks, B[m] = a*m*(m-1)/2, tick k holds N = B[m] + k.
Offset line k(m) = c*m + b  ->  N(m) = (a/2) m^2 + (c - a/2) m + b.
Classification (sieve-free): build the integer form, discriminant D.
  D < 0, or D > 0 non-square  -> irreducible over Q -> LIVE class
  D >= 0 perfect square       -> factors over Q -> dead-candidate
Empirical ground truth either way: count actual primes.

Metrics per form:
  streak = longest run of consecutive prime N starting at the form's first
           valid layer m_start = ceil(b/(a-c))   (the Euler metric)
  density = primes / valid m, over N <= LIMIT

Part 2: seam classes at NON-integer rationals a/b. On m = m0 + b*t the
seam N(t) = B[m]+L[m] is an exact quadratic in t (fit + verified); same
discriminant test on the doubled integer form.

Scope note: offset lines at non-integer ratios are also quadratic on
residue classes (B[m] is), but that enumeration is left as a follow-up;
integer ratios + all seams is the first pass.
"""
import numpy as np
from math import gcd, isqrt, ceil

LIMIT = 5_000_000
HEEGNER = {1, 2, 3, 4, 7, 8, 11, 16, 19, 27, 28, 43, 67, 163}  # |D| with class number 1


def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False; s[4::2] = False
    for p in range(3, int(n ** 0.5) + 1, 2):
        if s[p]: s[p*p::2*p] = False
    return s


S = sieve(LIMIT)


def classify(D):
    """D integer. dead-candidate iff D >= 0 and square. Returns (tag, root)."""
    if D < 0:
        return ("live-neg", None)
    r = isqrt(D)
    return ("dead-sq", r) if r * r == D else ("live-pos", None)


def stats(Nvals):
    """Nvals: 1-D int array of values for consecutive m (may contain <=1 junk)."""
    v = Nvals[(Nvals >= 2) & (Nvals <= LIMIT)]
    if len(v) == 0:
        return 0, 0.0, 0
    pr = S[v]
    # streak from the start
    st = 0
    for x in pr:
        if x: st += 1
        else: break
    return int(st), float(pr.mean()), int(pr.sum())


print("=" * 78)
print("PART 1 — offset lines k(m) = c*m + b at integer ratios a = 1..8")
print("=" * 78)

rows = []
for a in range(1, 9):
    c0 = a // 2
    mmax = int((2 * LIMIT / a) ** 0.5) + 2
    for c in range(0, a):          # c = a is the seam (b=0), handled in part 2
        for b in range(1, 257):
            m_start = max(1, ceil(b / (a - c)))
            m = np.arange(m_start, mmax)
            N = a * m * (m - 1) // 2 + c * m + b
            N = N[(N >= 2) & (N <= LIMIT)]
            if len(N) == 0:
                continue
            # integer form + discriminant
            if a % 2 == 0:
                A, Bq, C = c0, c - c0, b
            else:
                A, Bq, C = a, 2 * c - a, 2 * b
            D = Bq * Bq - 4 * A * C
            tag, _ = classify(D)
            st, dens, tot = stats(N)
            rows.append(dict(a=a, c=c, b=b, A=A, B=Bq, C=C, D=D, tag=tag,
                             streak=st, density=dens, total=tot, n=len(N)))

def form_str(r):
    if r["a"] % 2 == 0:
        return f"{r['A']}m^2+{r['B']}m+{r['C']}"
    return f"({r['A']}m^2+{r['B']}m+{r['C']})/2"

dead_with_primes = [r for r in rows if r["tag"] == "dead-sq" and r["total"] > 0]
print(f"\nforms scanned: {len(rows)}  | dead(square-D) with >0 primes (want 0): {len(dead_with_primes)}")
for r in dead_with_primes[:10]:
    print("  ANOMALY", r)

live = [r for r in rows if r["tag"].startswith("live")]
print(f"live forms: {len(live)}")

print("\n-- CHAMPIONSHIP by streak (top 20) --")
for r in sorted(live, key=lambda r: (-r["streak"], -r["density"]))[:20]:
    heeg = " *HEEGNER*" if abs(r["D"]) in HEEGNER else ""
    print(f"  a={r['a']} c={r['c']} b={r['b']:3}  N={form_str(r):24} D={r['D']:6} "
          f"streak={r['streak']:3} density={r['density']:.3f} n={r['n']}{heeg}")

print("\n-- CHAMPIONSHIP by density (n>=200, top 15) --")
for r in sorted([r for r in live if r["n"] >= 200], key=lambda r: -r["density"])[:15]:
    heeg = " *HEEGNER*" if abs(r["D"]) in HEEGNER else ""
    print(f"  a={r['a']} c={r['c']} b={r['b']:3}  N={form_str(r):24} D={r['D']:6} "
          f"density={r['density']:.3f} streak={r['streak']:3} n={r['n']}{heeg}")

print("\n-- HEEGNER real estate: every form with |D| in the class-number-1 set --")
hg = sorted([r for r in live if abs(r["D"]) in HEEGNER], key=lambda r: (abs(r["D"]), r["a"]))
for r in hg:
    print(f"  |D|={abs(r['D']):3} a={r['a']} c={r['c']} b={r['b']:3}  N={form_str(r):24} "
          f"streak={r['streak']:3} density={r['density']:.3f}")
print(f"  (total Heegner forms: {len(hg)}; distinct |D| present: {sorted(set(abs(r['D']) for r in hg))})")

print("\n" + "=" * 78)
print("PART 2 — seam classes at NON-integer rationals a/b (b = 2..8, a <= 8, coprime)")
print("=" * 78)

seam_rows = []
for b in range(2, 9):
    for a in range(1, 9):
        if gcd(a, b) != 1:
            continue
        mmax = int((2 * b * LIMIT / a) ** 0.5) + 2
        # walk m, accumulate B; bucket seam N by m mod b
        samples = {m0: [] for m0 in range(1, b + 1)}
        B = 0
        prevL = 0
        for m in range(1, mmax + 1):
            Lm = int(a * m / b + 0.5)
            if m >= 2:
                B += prevL
                N = B + Lm
                if N > LIMIT:
                    break
                samples[((m - 1) % b) + 1].append(N)
            prevL = Lm
        for m0, vals in samples.items():
            if len(vals) < 6:
                continue
            t = np.arange(len(vals))
            A2, B2, C2 = np.polyfit(t, vals, 2)
            A2, B2, C2 = round(2 * A2), round(2 * B2), round(2 * C2)   # doubled integer form
            check = (A2 * t * t + B2 * t + C2) // 2
            if not np.array_equal(check, vals):
                print(f"  FIT-FAIL at {a}:{b} class m0={m0} — skipping (would be [G])")
                continue
            D = B2 * B2 - 4 * A2 * C2
            tag, _ = classify(D)
            st, dens, tot = stats(np.array(vals))
            seam_rows.append(dict(a=a, b=b, m0=m0, A=A2, B=B2, C=C2, D=D, tag=tag,
                                  streak=st, density=dens, total=tot, n=len(vals)))

def seam_str(r):
    return f"({r['A']}t^2+{r['B']}t+{r['C']})/2"

dead2 = [r for r in seam_rows if r["tag"] == "dead-sq" and r["total"] > 0]
print(f"\nseam classes: {len(seam_rows)} | dead(square-D) with >0 primes (want 0): {len(dead2)}")
for r in dead2[:10]:
    print("  ANOMALY", r)
live2 = [r for r in seam_rows if r["tag"].startswith("live")]
print(f"live seam classes: {len(live2)}")
print("\n-- seam CHAMPIONS by streak (top 15) --")
for r in sorted(live2, key=lambda r: (-r["streak"], -r["density"]))[:15]:
    heeg = " *HEEGNER*" if abs(r["D"]) in HEEGNER else ""
    print(f"  {r['a']}:{r['b']} class m0={r['m0']:2}  N={seam_str(r):26} D={r['D']:6} "
          f"streak={r['streak']:3} density={r['density']:.3f} n={r['n']}{heeg}")
hg2 = sorted([r for r in live2 if abs(r["D"]) in HEEGNER], key=lambda r: (abs(r["D"]), r["a"], r["b"]))
print(f"\n-- seam HEEGNER hits: {len(hg2)}; distinct |D|: {sorted(set(abs(r['D']) for r in hg2))} --")
for r in hg2[:20]:
    print(f"  |D|={abs(r['D']):3} at {r['a']}:{r['b']} class m0={r['m0']}  streak={r['streak']} density={r['density']:.3f}")

print("\nDONE")
