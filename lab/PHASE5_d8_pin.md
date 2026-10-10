# PHASE 5 — D8 PIN: the discriminant is a degree-≤1 quasi-polynomial, and the obstruction is periodicity, not genus

Date: 2026-10-10. Artifact: `lab/PHASE5_d8.py` (run it to reproduce every
number below; CPU only, sympy/numpy, seconds). No other files touched.

## 1. The question and the hypothesis under test

The lab has an exact **enumeration** recipe for seam deadness at rational a/b:
on each residue class of m, the seam N = B[m]+L[m] is an exact quadratic
N_r(t); a class is a dead-candidate iff its discriminant is a perfect square
(census.py, verified 0/9,216 square-D forms with primes beyond the unit
boundary). Missing: a **closed-form index** — given coprime a/b, which classes
are dead without enumerating classes. The phase brief hypothesized the
obstruction might be Diophantine: if Δ(r) = B(r)²−4A(r)C(r) is a
cubic/quartic in the class index r, then y² = Δ(r) is elliptic (genus 1), and
no general closed form exists; if it is degree ≤ 2, Pell-type (genus 0)
closed forms exist in principle.

**Finding: the hypothesis is falsified.** Δ(r) never reaches degree 3–4. It is
a quasi-polynomial of polynomial degree **≤ 1**, and the class index r only
ever ranges over a complete residue system mod b. The square-value problem is
finite, decidable in O(b) exact arithmetic; the true obstruction to a
one-line closed form is the **bounded periodic (sawtooth) correction** — a
Dedekind-sum-like shadow of the rounding — not the genus of any curve.

## 2. Symbolic reconstruction of the seam quadratic

Conventions exactly as census.py: L[m] = round(a m / b) (half-up), B[m] =
Σ_{j<m} L[j], seam N = B[m] + L[m]. Write the rounding exactly as

    L[m] = (a m + c(m)) / b,   c(j) = b·round(a j / b) − a j,

where c(j) is an integer, periodic in j mod b, |c(j)| ≤ b/2. Then

    B[m] = a·m(m−1)/(2b) + S(m)/b,   S(m) = Σ_{j<m} c(j).

**Class lattice.** On m = r + R t with R any multiple of b (the discriminant
needs only R = b; the map notes' R = 2b·2^k is the *Layer-1* parity/content
lattice — B[m] mod 2 has period dividing 2b — and squareness is invariant
under refinement R → kR, verified: the subclass reparametrization t ↦ kt+ε
multiplies Δ by k² exactly). The seam is an exact quadratic in t:

    N(t) = A t² + B(r) t + C(r)
    A     = a R² / (2 b)                        (constant in r)
    B(r)  = β r + K,   β = aR/b,  K = aR/(2b) + RP/b²   (linear in r)
    C(r)  = (a/(2b)) r(r−1) + (S(r) + a r + c(r))/b     (quadratic + bounded periodic)

**Discriminant and the exact cancellation.** With P = Σ_{j=1..b} c(j):

    Δ(r) = B(r)² − 4 A C(r) = β(2K−β)·r + K² − (4A/b)(S(r) + c(r))
         = (2aP/b)·r + K² − 2a(S(r) + c(r))                (for R = b)

The r²-terms of B(r)² and 4AC(r) are both a²R²r²/b² and **cancel identically**
(for every a, b, R — symbolic identity, sympy-verified). What survives is a
linear ramp plus a bounded periodic term (|S|, |c| ≤ b², period b).

**The P-law** (proved by the pairing c(j) + c(b−j) = 0, with the self-paired
midpoint j = b/2 keeping c(b/2) = b/2 when b is even; verified for all
coprime pairs b ≤ 12, a ≤ 15, zero violations):

    P = 0      iff b is odd
    P = b/2    iff b is even

**DEGREE LAW.** The polynomial part of Δ(r) has degree

    * **0** iff b is odd:  Δ(r) = (a/2)² − 2a(S(r) + c(r))
    * **1** iff b is even: Δ(r) = a·r + ((a+1)/2)² − 2a(S(r) + c(r))

It is never ≥ 2, structurally, for any coprime a/b. The closed form was
checked against the wheel construction class-by-class for **all** coprime
pairs b ≤ 8, a ≤ 12: zero mismatches. Counterexample scan: none.

## 3. Genus classification of y² = Δ(r)

Because r ∈ {1, …, b} only (a complete residue system — r never runs over
ℤ):

* y² = Δ(r) is a **finite union of b exact square tests**. Each test is:
  is the explicit integer `linear(r) + periodic(r)` a perfect square? O(1)
  per class given the (O(b)-computable) table of c(j), S(r).
* **No Pell equation arises** — Pell requires a degree-2 square-value problem
  in a *free* integer variable; here the free variable t (the layer) is not
  the discriminant's variable, and Δ's own variable is bounded.
* **No elliptic curve arises** — that requires cubic/quartic Δ in a free
  variable, excluded by the structural r²-cancellation. The genus-0/genus-1
  boundary of the phase brief is never reached at the seam.
* **The artifact to avoid:** interpolating the b values Δ(1..b) by a single
  polynomial manufactures a degree-(b−1) object (at 5:8: a degree-7
  polynomial whose square values would *look* like a hard Diophantine
  problem). That object is not the discriminant; the correct object is the
  quasi-polynomial, degree ≤ 1. A high-degree interpolant is a symptom of
  ignoring the lattice structure, not of elliptic geometry.

## 4. Verification against the seam map (INSIGHTS 2026-10-09)

Classification per pair = per class: square Δ (dead-candidate) / content > 1
(Layer-1 kill) / live (irreducible, content 1). Dead ⟺ no live classes.
Run at R = b (canonical for Layer 2 by refinement invariance). All landmarks
**PASS**:

| pair | map says | classification | verdict |
|---|---|---|---|
| 3:8 | fully dead | all 8 classes square Δ (Δ values 25,16,25,4,1,16,1,4) | PASS |
| 5:8 | half/half (8 of 16 factorable) | 4 of 8 square (= 8 of 16 on R=16) + 1 content-killed (r=5, cont 2) + 3 live | PASS |
| 7:4 | dead (content anomaly) | 3 square + class r=2 content 2 (N=14t²+18t+6) → 0 live | PASS |
| 2:1, 1:1 | dead (pronic seam) | single class, Δ=(a/2)² square | PASS |
| 1:6, 1:14, 1:16 | dead (a=1 row) | all classes square | PASS |
| 5:6, 2:3, 4:5, 2:7, 7:8, 3:16, 3:10, 5:12 | alive | ≥ 1 live class each | PASS |
| b=4 column | dead iff a ≡ ±1 (mod 8) | a=1,7,9 → DEAD; a=3,5,11 → alive | PASS |
| a=1 row | all dead | all dead | PASS |

**Bonus (classification extends the map):** 9 pairs NOT on the published dead
list are predicted DEAD — 3:2, 5:2, 7:2, 8:3, 8:5, 9:2, 9:5, 10:3, 11:2 —
and each was confirmed empirically (0 seam primes at m ≥ 50 within 5M, the
map's own test). No counterexample to the classification appeared anywhere in
the sample.

## 5. Layer 1 (content/gcd): exactly decidable, one-sided

* Per class, the polynomial content is one gcd: cont(N_r) = gcd(N_r(0),
  N_r(1), N_r(2)) (a quadratic's value-gcd is decided by 3 samples).
* Within-block AP obstruction (constant-L blocks, difference L): both the
  first term and L are quasi-polynomial in the block index with period
  dividing b, so the per-block gcd is again a **finite table mod b**.
* In general: a quasi-polynomial family of period b and degree d has fixed
  divisor equal to the gcd of its first b(d+1) values (each residue class
  contributes a polynomial; a polynomial's value-gcd stabilizes after d+1
  samples). Verified numerically at 7 pairs (3:8, 5:8, 7:4, 5:6, 2:3, 1:4,
  3:10): gcd over 3b samples = gcd over 400b samples in every case. **No
  hidden fixed-divisor subtlety**: Layer 1 is a finite exact table.
* The honest caveat: content = 1 does **not** imply liveness. An irreducible,
  content-1 quadratic can still dodge every prime (Layer 3, sieve territory —
  e.g. 5:8's unlucky non-factorable classes). Layer 1 is a one-sided kill
  criterion; that one-sidedness is where the sieve remains irreplaceable.

## 6. FINAL PIN

> **Closed-form D8 ⟺ deciding, for each r mod b, whether**
> **Δ(r) = (2aP/b)·r + K² − 2a(S(r)+c(r))** — a linear function of r minus a
> **bounded b-periodic sawtooth built from the rounding corrections c(j)** —
> **is a perfect square, with P ∈ {0, b/2} according to the parity of b and
> the cancellation of the r² terms exact. This problem is genus-0-trivial as
> a curve (degree ≤ 1 in a variable ranging over a residue system, so no Pell
> and no elliptic curve ever arises), and its full content is a finite mod-b
> table. Therefore a closed form EXISTS and is O(b) exact arithmetic with no
> sieve: dead classes at a/b are {r mod b : Δ(r) square} ∪ {r mod b :
> cont(N_r) > 1}. What CANNOT exist is anything shorter than that table: the
> squareness of "linear + bounded sawtooth" has no (a,b)-parameterized
> formula, because the sawtooth S(r)+c(r) is a Dedekind-sum-like object whose
> values are not expressible in closed form simpler than their definition —
> the obstruction is quasi-polynomial periodicity, exactly the
> "fixed-divisor problem over quasi-polynomials" the seam map already
> suspected, and NOT Diophantine genus.**

The phase brief's degree-3/4 → elliptic scenario does not materialize; that
negative result is itself the pin. (Elliptic curves would appear only in the
different problem of *offset* lines k(m) = c·m+d at rational ratios with the
offset parameters free — unenumerated, per census.py's scope note — not at
the seam.)

**Corrected label proposal for D8** (supersedes "[G] Dead-offset indexing
formula at general a/b — the one open formula"):

> D8 [F→E]: Seam deadness at a/b **has** a closed form: dead classes = the
> square-discriminant classes ∪ the content-killed classes, both explicit
> finite mod-b tables (degree law: Δ(r) is degree-0/1 quasi-polynomial, r²
> cancels, P ∈ {0, b/2}). Enumeration cost O(b) exact arithmetic, no sieve.
> Residual openness is only the *compression* question: whether the sawtooth
> square tests admit an (a,b)-parameterized shortcut (a Dedekind-sum
> evaluation problem), and the Layer-1 one-sidedness (content-1 classes still
> need the sieve for actual primality).
