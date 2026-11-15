# lean_wheel

Formalization repository for the "Prime Tread Wheel" layer sieve. This
repository contains machine-checked proofs of 83 theorems formalized in
Lean 4 against mathlib. Every theorem is kernel-checked with no `sorry` and
no additional axioms; axiom footprints are restricted to the standard mathlib
trio `[propext, Classical.choice, Quot.sound]`.

What is formalized (exact statements, with module-level pointers):

- **Theorem I** (`LeanWheel/Bijection.lean`, `LeanWheel/RatioSlip.lean`,
  `LeanWheel/Primality.lean`, paper §19.1): the map `(m, k) ↦ T(m−1) + k`
  with `1 ≤ k ≤ m` is a bijection onto the positive integers
  (`Wheel.theoremI_bijection`); the stagger field `o_p(m) = −T(m−1)` in
  `ZMod p` satisfies `o_p(m+1) = o_p(m) − m` and detects divisibility
  exactly, `p ∣ T(m−1)+k ↔ (k : ZMod p) = o_p(m)`
  (`Wheel.o_succ`, `Wheel.dvd_iff_eq_o`); and inside a layer, a value
  `N = T(m−1)+k > ⌊√(T m)⌋` is prime iff no prime `p ≤ ⌊√(T m)⌋` divides it
  (`Wheel.theoremI_criterion`).
- **The Three-Primitive Theorem** (`LeanWheel/ThreePrimitive.lean`, paper
  §16.8): among discrete spirals satisfying the primitives P1 (origin &
  contiguity) and P3 (unit step), the seam lock P4 (odd divisors of odd `m`
  divide `B m`) or equivalently the lap palindrome P5 forces `L 1 − 1 = 0`
  and `B m = T(m−1)` for all `m ≥ 1` (`Wheel.three_primitive_P4`,
  `Wheel.three_primitive_P5`, `Wheel.P4_iff_P5_of_P1_P3`), with independence
  witnesses for the individual primitives.
- **GLM characterization** (`LeanWheel/GLM.lean`, paper §16.8): a quadratic
  count `2·B(m) = αm² + βm + γ` that locks at the seam, is a lap palindrome,
  and turns 1:1 is the wheel: `α = 1, β = −1, γ = 0, B = T(·−1)`
  (`Wheel.glm_unique`), witnessed by the wheel model
  (`Wheel.wheel_model`).
- **Dual certificate identity** (`LeanWheel/Dual.lean`, paper §18.9): for any
  finite free-ring residue structure, non-negative integer tick weights, and
  every valid phase cover, `D·(F + Σ_p y_p) ≥ TotalNum`
  (`Wheel.dual_certificate_identity`), with the exact ceiling-division solver
  form (`Wheel.dual_certificate_lb_floor`) used by the companion
  verifiers.
- **Erdős covering necessity** (`LeanWheel/ErdosFiber.lean`, paper §18.12):
  coprime residue classes over a family of moduli dividing `L` that cover all
  units mod `L` satisfy `Σ φ(L)/φ(m) ≥ φ(L)`, i.e. the `S(L) ≥ 1` necessary
  condition (`Wheel.erdos_fiber_coprime`, `Wheel.erdos_covering_necessary`).

The full ledger of all 83 theorems, statements, axiom footprints, and the
disposition of the unformalized remainder of the paper is
[`FORMALIZATION_STATUS.md`](FORMALIZATION_STATUS.md).

## Build

```sh
lake build                                    # kernel-checks the whole library
lake env lean PrintAxioms.lean                # axiom footprint report
```

Toolchain: Lean 4.35.0 (`leanprover/lean4:v4.35.0`), mathlib `v4.35.0`
(precompiled cache; not built from source). The library root is
`LeanWheel.lean`, which imports every module below.

## Modules

| Module | Contents |
|---|---|
| `LeanWheel/Defs.lean` | Triangular numbers `T`/`TZ` over ℕ/ℤ, exactness of the divisions (`two_mul_T`, `two_mul_TZ`), one-step recurrences, `TZ_neg` (palindrome) |
| `LeanWheel/B7.lean` | B7 mirror lift: interior value pairing, endpoint exchange, the tick involution on `ZMod m`, no odd-layer mirror prime pair |
| `LeanWheel/B3.lean` | B3 triangular-offset: the exact doubled factorization `2·(TZ(m−1)+m−c) = (m−j)(m+j+1) ↔ 2c = j(j+1)` over ℤ |
| `LeanWheel/B4.lean` | B4 forced-composite endpoints: `m ≥ 3 → ¬(T m).Prime`, `m ≥ 4 → ¬(T m − 1).Prime` |
| `LeanWheel/B1.lean` | B1: the visible set is exactly the primes; the layer floor `√(T m) < m` |
| `LeanWheel/B2.lean` | B2 column law and B5 seat-zero: prime values force `gcd k m = 1` (or `= 2` with `m ≡ 2 mod 4`) |
| `LeanWheel/Bijection.lean` | Theorem I part 1: existence, uniqueness, and the `∃!` coordinate bijection |
| `LeanWheel/RatioSlip.lean` | Theorem I part 2: the stagger field `o`, its recurrence, exact divisibility |
| `LeanWheel/Primality.lean` | Theorem I part 3: the in-layer exact primality criterion and the `√N` bridge |
| `LeanWheel/ThreePrimitive.lean` | The Three-Primitive Theorem (P4/P5 routes, equivalence) and the independence witnesses |
| `LeanWheel/GLM.lean` | GLM lock+palindrome lemma: the `γ = 0` / `α + β = 0` iff's, uniqueness, the wheel model |
| `LeanWheel/Orphan.lean` | Theorem II part 1: the orphan characterization over layers |
| `LeanWheel/PhaseTransition.lean` | Theorem II part 3: the `T(m)^{1/4}` phase transition with the exact threshold |
| `LeanWheel/Conservation.lean` | Theorem III: disjoint-union conservation over the strata of a layer |
| `LeanWheel/Capacity.lean` | Theorem III part 2: covering-capacity (stripe) inequalities |
| `LeanWheel/Smear.lean` | Theorem IV: the LP smear arithmetic over ℚ |
| `LeanWheel/LP.lean` | Theorem IV part 2: the explicit feasible point of the LP relaxation |
| `LeanWheel/BreakEven.lean` | break-even algebra over ℝ (conditional; excluded from paper claims) |
| `LeanWheel/Dual.lean` | §18.9: the exact-integer dual certificate identity and its solver form |
| `LeanWheel/Rotor.lean` | §18.11: the Schwinger rotor tuning and the wheel-spectrum glue |
| `LeanWheel/ErdosFiber.lean` | §18.12: the equal-fiber CRT count and covering necessity |
| `LeanWheel/MainTheorems.lean` | Flagship summary: restatements (aliases) of the five headline clusters with docstrings |
| `LeanWheel/Sanity.lean` | Vacuity audit: concrete non-vacuous instantiations of the flagship hypotheses |

## Flagship theorems

[`LeanWheel/MainTheorems.lean`](LeanWheel/MainTheorems.lean) restates the
five headline clusters above as a single summary file with plain-English
docstrings and full explicit types; the proofs are aliases of the
kernel-checked certificates in the individual modules.

## Scope

Measured statistics, computational certificates, and open conjectures
associated with the wheel construction are not claimed in this repository;
they live in the companion paper repository and are documented in
`FORMALIZATION_STATUS.md` §2–§3.
