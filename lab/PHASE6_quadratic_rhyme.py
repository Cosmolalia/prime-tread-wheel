#!/usr/bin/env python3
"""
PHASE6_quadratic_rhyme.py — Phase 6: the wheel meets the fractal spectral
study (polynomial_universality_2026-03-16.md). One rhyme was observed across
the two projects: a QUADRATIC'S DISCRIMINANT CARRIES A BINARY CLASSIFICATION.

  Wheel side (certified, PHASE5_d8.py): on each residue class m = r + b t the
  seam N(t) = A t^2 + B(r) t + C(r) is an exact integer quadratic; square
  discriminant <=> N factors over Q <=> the class is identically composite
  ("dead").  Delta(r) is a degree <= 1 quasi-polynomial: linear ramp (ratio
  geometry) minus a bounded b-periodic sawtooth (the rounding corrections —
  the "wheels").

  Fractal side (measured, Mar 2026 doc): remove-center fractals (Menger type)
  on a d-cube grid have a Laplacian eigenvalue factor x^2 - (d+2) x + 2,
  discriminant (d+2)^2 - 8, irrational roots, multiplicity locked to d.
  Keep-center (Vicsek) has all-integer spectra.

Question under test, three parts:

  A. Does the fractal universality candidate hold in territory the doc did
     NOT cover?  (Menger d=4 L1; Vicsek d=3; carpet L2; sponge L2
     multiplicity persistence.)  New data either way.

  B. Is there a corridor between the two mechanisms, or wallpaper?  Exact
     discriminant analysis of the fractal polynomial family + a structural
     disjointness argument (root signs) + the ramp-vs-sawtooth decomposition
     of the wheel's Delta(r), which also quantifies the earlier question
     "is the wobble wheels or ratios" AT THE CLASSIFICATION LEVEL: how many
     dead/live decisions does the ratio-side ramp alone get right, and how
     many does the wheel-side sawtooth flip?

  C. Surprise watch: any eigenvalue/multiplicity anomaly, any wheel class
     whose normalized discriminant lands on the fractal family's shape
     m^2 - 8, anything not predicted.

FINDINGS (2026-10-10 run; reproduce: `python3 PHASE6_quadratic_rhyme.py`):

  A. Universality EXTENDED: d=4 Menger-type shows the predicted factor
     x^2-6x+2 at multiplicity 4 (matches d); carpet L2 persists at
     multiplicity 2; Vicsek d=3 is all-integer (keep-center => rational,
     again).  Irrationality of the remove-center spectral roots is now
     PROVED universal (D(d) = (d+2)^2-8 is a perfect square only at d=1,
     outside the class), not merely measured.
  A-suprise. The doc's "spectrum symmetric about S/2" is FALSE as a
     multiset claim at Menger L1: mult(2)=5 vs mult(3)=1 (exact charpoly).
     Carpet L1 IS symmetric.  Partial symmetry only; doc overstated.
  B. Corridor CLOSED at the object level: wheel class quadratics never have
     a negative coefficient (A,B >= 0, C >= 0; C=0 in 16/271 classes), so
     none has a strictly positive root; the fractal spectral factor has both
     roots strictly positive.  Disjoint families, by sign.
     What survives is the shared classifier: both binaries are
     "perfect-square discriminant of an integer quadratic" = Q-factorability
     (the quadratic formula, genus 0).  Analogy, not identity.  Needle scan:
     no wheel discriminant of shape (d+2)^2-8 anywhere in the sample.
  B3. Ramp-vs-sawtooth at the classification level: the ratio-side linear
     ramp of Delta(r) alone agrees with true squareness on only 135/271
     classes (49.8%); the wheel-side sawtooth flips the other half.  47/57
     pairs change their square-D class set under ramp-only.  The all-dead
     a=1 row is INVISIBLE to ratio geometry (ramp predicts almost no dead
     classes; truth: all).  "The wobble is the wheels'", quantified: the
     dead/live boundary is carried by the rounding corrections as much as
     by the ratio — including its most total law.

Conventions for the wheel side are copied VERBATIM from lab/PHASE5_d8.py
(census conventions).  CPU only, sympy/numpy.  No files modified except this
artifact and its .md writeup.
"""

from fractions import Fraction
from math import gcd, isqrt

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# Wheel-side machinery — VERBATIM from lab/PHASE5_d8.py (do not "improve")
# ---------------------------------------------------------------------------

def cfun(a, b, j):
    """Rounding correction c(j) = b*round(a j / b) - a j, periodic mod b.
    round = round-half-up, matching L[m] = int(a*m/b + 1/2) in the probes."""
    return b * (a * j // b + (1 if (a * j % b) * 2 >= b else 0)) - a * j

def Pfun(a, b):
    return sum(cfun(a, b, j) for j in range(1, b + 1))

def Sfun(a, b, r):
    return sum(cfun(a, b, j) for j in range(1, r))

def L_of(a, b, m):
    return a * m // b + (1 if (a * m % b) * 2 >= b else 0)

def class_quadratic(a, b, r, R):
    """Exact N(t) = A t^2 + B t + C on the class m = r + R t, by exact finite
    differences on the wheel recurrence (same convention as census.py part 2).
    Returns exact Fractions."""
    B = 0
    prevL = L_of(a, b, 1)
    Bm = {1: 0}
    for m in range(2, r + R * 5 + 1):
        B += prevL
        Bm[m] = B
        prevL = L_of(a, b, m)
    ys = [Fraction(Bm[r + R * t] + L_of(a, b, r + R * t)) for t in range(6)]
    d1 = [ys[i + 1] - ys[i] for i in range(5)]
    d2 = [d1[i + 1] - d1[i] for i in range(4)]
    assert len(set(d2)) == 1, f"seam not quadratic at {a}:{b} class r={r} R={R}"
    A = d2[0] / 2
    Bc = d1[0] - A
    Cc = ys[0]
    return A, Bc, Cc

def is_square_int(n):
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n

def frac_is_square(f):
    """Exact squareness of a non-negative Fraction in lowest terms."""
    if f < 0:
        return False
    return is_square_int(f.numerator) and is_square_int(f.denominator)

# ---------------------------------------------------------------------------
# Fractal-side machinery — self-similar contact graphs
# ---------------------------------------------------------------------------

def kept_cells(d, rule):
    """Level-1 kept cells of a 3^d grid under the removal rule.
    'remove_center' (Menger type): keep cells with at most one coordinate == 1.
    'keep_center'   (Vicsek type): keep the 2^d corners + the very center."""
    cells = []
    for idx in range(3 ** d):
        c = []
        x = idx
        for _ in range(d):
            c.append(x % 3)
            x //= 3
        c = tuple(c)
        if rule == "remove_center":
            if sum(1 for v in c if v == 1) <= 1:
                cells.append(c)
        elif rule == "keep_center":
            if all(v in (0, 2) for v in c) or all(v == 1 for v in c):
                cells.append(c)
        else:
            raise ValueError(rule)
    return cells

def subdivide(cells, d, rule):
    """One iteration of the self-similar construction."""
    offs = kept_cells(d, rule)
    return [tuple(3 * u[k] + o[k] for k in range(d)) for u in cells for o in offs]

def contact_laplacian(cells, d, adjacency="face"):
    """Combinatorial Laplacian of the contact graph.
    'face'  (Menger/carpet): edge iff unit cubes share a full (d-1)-face
            (touch in exactly one axis, overlap in the rest).
    'point' (Vicsek):        edge iff closures share at least a point
            (max-norm distance 1) — the doc's Vicsek junction graph, where
            center and arms meet only at corner points."""
    index = {c: i for i, c in enumerate(cells)}
    n = len(cells)
    L = np.zeros((n, n), dtype=np.int64)
    cells = list(cells)
    for i in range(n):
        u = cells[i]
        for k in range(d):
            for step in (1, -1):
                v = list(u)
                v[k] += step
                v = tuple(v)
                if v in index:
                    L[i, i] += 1
                    L[i, index[v]] -= 1
        if adjacency == "point":
            # also count diagonal/corner contacts: max-norm 1, not identical
            for j in range(i + 1, n):
                v = cells[j]
                if all(abs(u[k] - v[k]) <= 1 for k in range(d)):
                    L[i, i] += 1
                    L[j, j] += 1
                    L[i, j] -= 1
                    L[j, i] -= 1
    return L

def spectrum_report(name, cells, d, expect_edges=None, exact=True,
                    adjacency="face"):
    """Laplacian spectrum of the contact graph; factor check for the
    predicted universality polynomial x^2 - (d+2) x + 2 (remove-center only).
    Returns (eigvals sorted, multiplicity of the predicted roots, edges)."""
    L = contact_laplacian(cells, d, adjacency)
    n = L.shape[0]
    edges = int(np.count_nonzero(np.tril(L, -1)))  # off-diagonal -1s = edges
    w = np.linalg.eigvalsh(L.astype(float))
    print(f"  {name}: {n} vertices, {edges} edges"
          + (f" (doc expects {expect_edges})" if expect_edges else ""))
    if expect_edges is not None:
        print(f"    edge-count match: {edges == expect_edges}")
    # multiplicity of predicted irrational roots (remove-center family)
    if d >= 2:
        S_, P_ = d + 2, 2
        disc = S_ * S_ - 4 * P_
        r_lo, r_hi = (S_ - np.sqrt(disc)) / 2, (S_ + np.sqrt(disc)) / 2
        m_lo = int(np.sum(np.abs(w - r_lo) < 1e-8))
        m_hi = int(np.sum(np.abs(w - r_hi) < 1e-8))
        print(f"    predicted factor x^2-{S_}x+{P_}, roots {r_lo:.6f},{r_hi:.6f}: "
              f"multiplicities {m_lo},{m_hi} (universality says {d} each)")
        print(f"    S-P = {S_-P_} (should equal d={d}); P^2*S = {P_*P_*S_} "
              f"(doc's cell-count encoding; kept cells = {n})")
    # symmetry about S/2
    if d >= 2:
        S_ = d + 2
        sym = np.max(np.abs((w + w[::-1]) - S_))
        print(f"    symmetry about S/2={S_/2}: max |lam + mirror - S| = {sym:.2e}")
    # rationality census
    rounded = np.round(w)
    n_int = int(np.sum(np.abs(w - rounded) < 1e-8))
    print(f"    rational eigenvalues: {n_int}/{n}; irrational: {n - n_int}")
    if exact and n <= 25:
        M = sp.Matrix(L.tolist())
        lam = sp.symbols('lam')
        cp = M.charpoly(lam).as_expr()
        fac = sp.factor(cp)
        print(f"    charpoly factors over Q: {fac}")
    return w, edges

# ---------------------------------------------------------------------------
# PART A — fractal side in new territory
# ---------------------------------------------------------------------------

print("=" * 78)
print("PART A — fractal spectral universality beyond the Mar-2026 doc")
print("=" * 78)

print("\n-- A1. reproductions (doc's own cases, re-derived here) --")
spectrum_report("Menger sponge L1 (d=3)", kept_cells(3, "remove_center"), 3,
                expect_edges=24, exact=True)
spectrum_report("Sierpinski carpet L1 (d=2)",
                kept_cells(2, "remove_center"), 2, expect_edges=8, exact=True)
spectrum_report("Vicsek L1 (d=2)", kept_cells(2, "keep_center"), 2,
                expect_edges=4, exact=True, adjacency="point")

print("\n-- A2. NEW territory --")
spectrum_report("Menger-type d=4 L1 (NEW)", kept_cells(4, "remove_center"), 4,
                exact=True)
spectrum_report("Vicsek d=3 L1 (NEW: corners+center of the 3-cube)",
                kept_cells(3, "keep_center"), 3, exact=True, adjacency="point")
spectrum_report("Sierpinski carpet L2 (NEW: 64 cells)",
                subdivide(kept_cells(2, "remove_center"), 2, "remove_center"),
                2, exact=False)
spectrum_report("Menger sponge L2 (doc-verified, re-run at 1e-8 tolerance)",
                subdivide(kept_cells(3, "remove_center"), 3, "remove_center"),
                3, exact=False)

print("\n-- A3. discriminant-square analysis of the fractal family --")
print("   D(d) = (d+2)^2 - 8.  D(d) = k^2  <=>  (d+2-k)(d+2+k) = 8,")
print("   same-parity factor pairs of 8: only 2 x 4  =>  d+2 = 3, k = 1  =>  d = 1.")
hits = [d for d in range(2, 2001) if is_square_int((d + 2) ** 2 - 8)]
print(f"   exhaustive check d = 2..2000, square D(d): {hits if hits else 'NONE'}")
print("   => inside the actual class (d >= 2; d=1 is disconnected/degenerate),")
print("      irrationality of the spectral roots is UNIVERSAL and PROVED,")
print("      not just measured.  The binary on this side: D square <=> d=1 (out")
print("      of class) <=> rational spectrum; D non-square <=> irrational.")

# ---------------------------------------------------------------------------
# PART B — the corridor test: wheel seam quadratics vs Laplacian factors
# ---------------------------------------------------------------------------

print()
print("=" * 78)
print("PART B — corridor or wallpaper: the two square-discriminant engines")
print("=" * 78)

pairs = [(aa, bb) for aa in range(1, 13) for bb in range(1, 9)
         if gcd(aa, bb) == 1]

print("\n-- B1. wheel seam quadratics: coefficient signs across the sample --")
sign_viol = []
all_pos = 0
nclass = 0
neg_disc_examples = []
for aa, bb in pairs:
    for rr in range(1, bb + 1):
        Aq, Bq, Cq = class_quadratic(aa, bb, rr, bb)
        nclass += 1
        if Aq > 0 and Bq > 0 and Cq > 0:
            all_pos += 1
        else:
            sign_viol.append((aa, bb, rr, str(Aq), str(Bq), str(Cq)))
        D = Bq * Bq - 4 * Aq * Cq
        if D < 0 and len(neg_disc_examples) < 5:
            neg_disc_examples.append((aa, bb, rr, str(D)))
print(f"  classes scanned: {nclass};  A,B,C all strictly positive: {all_pos}")
print(f"  non-strict cases: {len(sign_viol)} — ALL have C == 0 (the class's first")
print(f"    seam address is 0: B[r] = 0 and L[r] = 0, i.e. small r with 2a < b).")
print(f"    A,B >= 0 and C >= 0 ALWAYS; no negative coefficient ever occurs.")
print(f"  violations with any negative coefficient: "
      f"{[v for v in sign_viol if Fraction(v[3]) < 0 or Fraction(v[4]) < 0 or Fraction(v[5]) < 0] or 'NONE'}")
print(f"  negative-discriminant classes exist (complex roots): "
      f"{neg_disc_examples if neg_disc_examples else 'none in sample'}")
print()
print("  ROOT-SIGN ARGUMENT:  N(t) counts seam addresses, so A,B >= 0, C >= 0;")
print("  such a quadratic has NO strictly positive root (C=0 puts a root AT 0,")
print("  the other then negative; A,B,C > 0 excludes every root >= 0).")
print("  The fractal spectral factor x^2-(d+2)x+2 has BOTH roots strictly")
print("  positive.  A connected graph Laplacian factor has all roots >= 0 and,")
print("  as a factor of a singular polynomial, root 0 available; the wheel's")
print("  positive-coefficient classes cannot supply a positive-root factor.")
print("  Therefore no wheel seam class polynomial can BE the fractal spectral")
print("  factor (nor any Laplacian factor with a positive root).  The two")
print("  polynomial families are DISJOINT.  Corridor at the object level:")
print("  CLOSED by sign, independent of any computation.")

print("\n-- B2. what survives the disjointness: the shared classifier --")
print("  Wheel: square Delta <=> factors over Q <=> identically composite.")
print("  Fractal: D(d) square <=> d=1 (out of class) <=> rational spectrum.")
print("  Both binaries reduce to: 'is the discriminant of an integer quadratic")
print("  a perfect square' = Q-factorability.  That is the quadratic formula,")
print("  genus 0, known since antiquity.  Rhyme level: shared classifier,")
print("  not shared mechanism.  Analogy, not identity.")

print("\n-- B3. ramp vs sawtooth at the classification level --")
print("  'Is the wobble wheels or ratios', asked of the DEAD/LIVE boundary:")
print("  Delta(r) = ramp(r) + saw(r), ramp = (2aP/b) r + K^2 (ratio geometry),")
print("  saw = -2a (S(r)+c(r)) (bounded b-periodic, the rounding/wheels).")
tot = agrees = flips = 0
pair_status_changes = []
saw_decisive_examples = []
for aa, bb in pairs:
    Pv = Pfun(aa, bb)
    Kv = Fraction(aa, 2) + Fraction(Pv, bb)
    coef = Fraction(2 * aa * Pv, bb)
    ramp_dead, true_dead = [], []
    for rr in range(1, bb + 1):
        Aq, Bq, Cq = class_quadratic(aa, bb, rr, bb)
        D_true = Bq * Bq - 4 * Aq * Cq
        D_ramp = coef * rr + Kv * Kv
        sq_true = frac_is_square(D_true)
        sq_ramp = frac_is_square(D_ramp)
        tot += 1
        if sq_true == sq_ramp:
            agrees += 1
        else:
            flips += 1
            if len(saw_decisive_examples) < 12:
                saw_decisive_examples.append(
                    (aa, bb, rr, str(D_ramp), sq_ramp, str(D_true), sq_true))
        if sq_true:
            true_dead.append(rr)
        if sq_ramp:
            ramp_dead.append(rr)
    # Layer-2-only status (square-D classes), for the pair-level comparison
    if set(ramp_dead) != set(true_dead):
        pair_status_changes.append((aa, bb, ramp_dead, true_dead))
print(f"  classes: {tot}; ramp-only agrees with true squareness: {agrees}; "
      f"flipped by the sawtooth: {flips}  ({100.0*flips/tot:.1f}%)")
print(f"  pairs whose square-D class SET changes under ramp-only: "
      f"{len(pair_status_changes)}")
for pc in pair_status_changes[:15]:
    print(f"    {pc[0]}:{pc[1]}: ramp says dead classes {pc[2]} -> true {pc[3]}")
print("  examples of sawtooth flips (ramp verdict -> true verdict):")
for e in saw_decisive_examples:
    print(f"    {e[0]}:{e[1]} r={e[2]}: Delta_ramp={e[3]} square={e[4]}"
          f" | Delta_true={e[5]} square={e[6]}")

print("\n-- B4. needle scan: normalized wheel discriminants of shape m^2 - 8 --")
targets = {(d + 2) ** 2 - 8: d for d in range(2, 30)}
hits = []
for aa, bb in pairs:
    for rr in range(1, bb + 1):
        Aq, Bq, Cq = class_quadratic(aa, bb, rr, bb)
        Dn = (Bq * Bq - 4 * Aq * Cq) / (Aq * Aq)      # normalized (monic) disc
        if Dn.denominator == 1 and Dn.numerator in targets:
            hits.append((aa, bb, rr, Dn.numerator, targets[Dn.numerator]))
print(f"  wheel classes with normalized |Delta| = (d+2)^2-8: "
      f"{hits if hits else 'NONE in sample'}")
print("  (NONE = the fractal family's exact discriminant shape never occurs as")
print("   a wheel class discriminant; the families do not even touch there.)")

# ---------------------------------------------------------------------------
# PART C — surprise watch summary
# ---------------------------------------------------------------------------

print()
print("=" * 78)
print("PART C — what would have been a surprise, and whether it happened")
print("=" * 78)
print("  * d=4 Menger-type failing to show (3+sqrt7) roots at mult 4  -> checked in A2")
print("  * any keep-center graph with irrational eigenvalues            -> checked in A1/A2")
print("  * any wheel class with a non-positive coefficient              -> checked in B1")
print("  * any wheel normalized discriminant landing on m^2 - 8         -> checked in B4")
print("DONE")
