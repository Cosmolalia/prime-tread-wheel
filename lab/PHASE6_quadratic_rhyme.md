# PHASE 6 — the quadratic rhyme: wheel deadness engine vs fractal spectral universality

Date: 2026-10-10. Artifact: `lab/PHASE6_quadratic_rhyme.py` (run it to
reproduce every number below; CPU only, sympy/numpy, <2s). Paired writeup.
Wheel-side conventions verbatim from `lab/PHASE5_d8.py`.

## 1. Why this phase exists

Two projects in the corpus independently arrived at the same shape:

> **A quadratic's discriminant carries a binary classification.**

- **Wheel** (certified PHASE 5): per residue class, the seam N(t) is an
  exact quadratic; square discriminant ⟺ factors over ℚ ⟺ class identically
  composite ("dead"). Δ(r) decomposes as linear **ramp** (ratio geometry)
  plus bounded **sawtooth** (rounding corrections — the "wheels").
- **Fractal** (`polynomial_universality_2026-03-16.md`): remove-center
  fractals have Laplacian factor x²−(d+2)x+2, discriminant (d+2)²−8,
  irrational roots, multiplicity locked to d; keep-center all-integer.

Question: corridor or wallpaper?

## 2. Part A — fractal universality in new territory

Reproductions exact (charpoly over ℚ): Menger L1 `lam(lam−5)(lam−4)³(lam−3)(lam−2)⁵(lam−1)³(lam²−5lam+2)³`;
carpet L1 `lam(lam−4)(lam−2)²(lam²−4lam+2)²`; Vicsek L1 (point-contact
junction graph) `lam(lam−5)(lam−1)³`.

**New data:**

| object | result |
|---|---|
| Menger-type **d=4** L1 (48 cells, NEW) | factor x²−6x+2 at mult **4** ✓ (S−P=4) |
| Vicsek **d=3** (NEW) | K₁,₈ star, spectrum 0, 1×7, 9 — all-integer again |
| carpet **L2** (64 cells, NEW) | factor persists at mult **2** ✓ |
| sponge L2 (re-run, 1e-8) | mult 3 ✓ (doc-verified) |

**Proof upgrade [F→E for the irrationality claim]:** D(d) = (d+2)²−8 = k²
⟺ (d+2−k)(d+2+k) = 8; same-parity factor pairs give only d+2=3, k=1, d=1 —
outside the class (d=1 is disconnected under remove-center). Exhaustive
check d = 2..2000: no square. Irrationality of the spectral roots is
**universal and proved** for remove-center d ≥ 2, not just measured.

**Surprise against the doc:** "Spectrum symmetric about S/2" is FALSE as a
multiset claim at Menger L1: mult(2)=5 vs mult(3)=1 (exact charpoly above;
mirror deviation 1.0). Carpet L1 is exactly symmetric (deviation 1.8e-15).
Partial symmetry only — the doc overstated. The doc's `P²·S = cell count`
encoding also fails outside d=3 (d=2: 16≠8; d=4: 24≠48); and the universality
depends on the contact convention (Vicsek pieces touch at points; the
junction graph is the right object there).

## 3. Part B — the corridor test

**B1. Disjointness by root sign [F].** Across all 271 seam classes of the
PHASE5 sample: no coefficient is ever negative (A,B ≥ 0, C ≥ 0; C = 0 in 16
classes — root at 0, never a positive root). The fractal spectral factor
x²−(d+2)x+2 has **both roots strictly positive**. Therefore no wheel seam
class polynomial can be the fractal spectral factor (or any Laplacian factor
with a positive root). The families are disjoint; the object-level corridor
is closed by sign, no computation needed.

**B2. What survives: the shared classifier.** Both binaries reduce to
"is an integer quadratic's discriminant a perfect square" = ℚ-factorability —
the quadratic formula, genus 0. Rhyme level: shared classifier, not shared
mechanism. **Analogy, not identity.** Needle scan: no wheel class has
normalized discriminant of shape (d+2)²−8; the families do not even touch.

**B3. Ramp vs sawtooth — "is the wobble wheels or ratios", answered at the
classification level [E, measured].** Δ(r) = ramp(r) + saw(r). The ratio-side
ramp alone agrees with true squareness on **135/271 classes (49.8%)**; the
wheel-side sawtooth flips the other half. **47/57 pairs** change their
square-D class set under ramp-only. The all-dead a=1 row is *invisible* to
ratio geometry (ramp predicts almost no dead classes; truth: all dead).
The dead/live boundary — including its most total law — is carried by the
rounding corrections as much as by the ratio geometry.

## 4. Status

- Fractal irrationality: measured → **proved** for the polynomial family
  (the *appearance* of the factor at multiplicity d remains a universality
  conjecture, now with d = 2, 3, 4 evidence at L1 and L2 persistence for
  d = 2, 3).
- Doc correction registered: symmetry-about-S/2 overstated; P²S encoding is
  d=3-specific.
- Wheel ↔ fractal corridor: **closed at object level** (root signs), no
  deeper connector found; shared quadratic-formula classifier labeled
  analogy.
- B3 stands as a wheel-internal result independent of the fractal side:
  quantified attribution of the dead/live boundary between ratio geometry
  and the stagger/rounding field.
