/-
  MainTheorems — flagship summary for Theorem Day.

  Clean restatements (aliases with full explicit types, proofs delegated to
  the kernel-checked certificates) of the five headline clusters:

    1. Theorem I (three parts): the layer-coordinate bijection, the stagger
       field, and the exact in-layer primality criterion (WHITEPAPER §19.1).
    2. The Three-Primitive Theorem (WHITEPAPER §16.8).
    3. GLM's lock+palindrome characterization (WHITEPAPER §16.8).
    4. The §18.9 exact-integer dual certificate identity.
    5. The §18.12 Erdős covering-necessity condition.

  No Tier-2/Tier-3 lemmas are restated here; see the individual modules and
  FORMALIZATION_STATUS.md for the full 83-theorem ledger.  Every alias below
  was `#print axioms`-checked through the underlying certificate (footprints
  ⊆ [propext, Classical.choice, Quot.sound]).
-/

import Mathlib
import LeanWheel.Defs
import LeanWheel.Bijection
import LeanWheel.RatioSlip
import LeanWheel.Primality
import LeanWheel.ThreePrimitive
import LeanWheel.GLM
import LeanWheel.Dual
import LeanWheel.ErdosFiber

namespace Wheel

/-! ## Theorem I — the layer structure (WHITEPAPER §19.1) -/

/-- **Theorem I, part 1 (paper §19.1.1).** Every positive integer N has a
    unique layer coordinate: there is exactly one pair (m, k) with
    1 ≤ k ≤ m and N = T(m−1) + k.  The map (m, k) ↦ T(m−1) + k is a bijection
    from the triangular domain onto ℤ_{≥1}. -/
theorem theoremI_bijection_headline (N : ℕ) (hN : 1 ≤ N) :
    ∃! mk : ℕ × ℕ, 1 ≤ mk.2 ∧ mk.2 ≤ mk.1 ∧ T (mk.1 - 1) + mk.2 = N :=
  Wheel.theoremI_bijection N hN

/-- **Theorem I, part 2 (paper §19.1.2), the stagger field recurrence.**
    The stagger field o_p(m) = −T(m−1) (in ZMod p) evolves by the exact
    first-order difference equation o_p(m+1) = o_p(m) − m. -/
theorem o_succ_headline (p m : ℕ) :
    o p (m + 1) = o p m - (m : ZMod p) :=
  Wheel.o_succ p m

/-- **Theorem I, part 2 (paper §19.1.2), the divisibility criterion.**
    For p ≥ 1, the wheel prime p divides the layer value N = T(m−1) + k
    if and only if the tick k equals the stagger field: (k : ZMod p) = o_p(m),
    i.e. k ≡ −T(m−1) (mod p). -/
theorem dvd_iff_eq_o_headline (p m k : ℕ) (_hp : 1 ≤ p) :
    p ∣ (T (m - 1) + k) ↔ (k : ZMod p) = o p m :=
  Wheel.dvd_iff_eq_o p m k _hp

/-- **Theorem I, part 3 (paper §19.1.3), the exact primality criterion.**
    Inside layer m, a value N = T(m−1) + k (1 ≤ k ≤ m) exceeding ⌊√(T m)⌋
    is prime if and only if no wheel prime p ≤ ⌊√(T m)⌋ divides it. -/
theorem theoremI_criterion_headline (N : ℕ) {m k : ℕ} (hk : 1 ≤ k) (hkm : k ≤ m)
    (hN : N = T (m - 1) + k) (hbig : Nat.sqrt (T m) < N) :
    N.Prime ↔ ∀ p, p.Prime → p ≤ Nat.sqrt (T m) → ¬ p ∣ N :=
  Wheel.theoremI_criterion N hk hkm hN hbig

/-! ## The Three-Primitive Theorem (WHITEPAPER §16.8) -/

/-- **Three-Primitive Theorem, P4 route (paper §16.8).** Among discrete
    spirals with lap-start B and lap-length L (P1: origin & contiguity;
    P3: unit step; P4: odd-divisor seam lock), the primitives are unique:
    L 1 − 1 = 0 and B m = T(m−1) for every m ≥ 1 — i.e. the spiral is the
    wheel. -/
theorem three_primitive_P4_headline {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L)
    (h4 : P4 B) :
    L 1 - 1 = 0 ∧ ∀ m : ℕ, 1 ≤ m → B m = TZ ((m : ℤ) - 1) :=
  Wheel.three_primitive_P4 h1 h3 h4

/-- **Three-Primitive Theorem, P5 route (paper §16.8).** The same uniqueness
    conclusion (L 1 − 1 = 0 and B m = T(m−1) for all m ≥ 1) follows from
    P1 ∧ P3 ∧ P5, where P5 is the lap-palindrome condition on the polynomial
    extension: B̂(m) = B̂(1−m) for all m : ℤ. -/
theorem three_primitive_P5_headline {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L)
    (h5 : P5 L) :
    L 1 - 1 = 0 ∧ ∀ m : ℕ, 1 ≤ m → B m = TZ ((m : ℤ) - 1) :=
  Wheel.three_primitive_P5 h1 h3 h5

/-- **Three-Primitive Theorem, equivalence (paper §16.8).** Given P1 ∧ P3,
    the seam lock P4 and the lap palindrome P5 are equivalent conditions. -/
theorem P4_iff_P5_headline {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L) :
    P4 B ↔ P5 L :=
  Wheel.P4_iff_P5_of_P1_P3 h1 h3

/-! ## GLM characterization (WHITEPAPER §16.8) -/

/-- **GLM uniqueness (paper §16.8).** Any quadratic count B (carried exactly
    as 2·B(m) = αm² + βm + γ) that (i) locks at the seam (every positive
    divisor of every odd m divides B m), (ii) is a lap palindrome
    (B m = B(1−m)), and (iii) turns 1:1 (B(m+1) − B m = m) is forced to be
    the wheel: α = 1, β = −1, γ = 0 and B(m) = T(m−1) for all m : ℤ. -/
theorem glm_unique_headline (B : ℤ → ℤ) (α β γ : ℤ) (hq : IsQuadCount B α β γ)
    (hlock : ∀ m : ℤ, Odd m → ∀ q : ℤ, 0 < q → q ∣ m → q ∣ B m)
    (hpal : ∀ m : ℤ, B m = B (1 - m))
    (hturn : ∀ m : ℤ, B (m + 1) - B m = m) :
    α = 1 ∧ β = -1 ∧ γ = 0 ∧ ∀ m : ℤ, B m = TZ (m - 1) :=
  Wheel.glm_unique B α β γ hq hlock hpal hturn

/-- **The wheel model (paper §16.8).** The witness exhibiting that GLM's
    three conditions are simultaneously satisfiable: the wheel count
    B(m) = T(m−1) is a quadratic count with (α, β, γ) = (1, −1, 0)
    (see `wheel_model_lock`, `wheel_model_palindrome`, `wheel_model_turn`
    in `LeanWheel/GLM.lean` for the three conditions). -/
theorem wheel_model_headline : IsQuadCount (fun m ↦ TZ (m - 1)) 1 (-1) 0 :=
  Wheel.wheel_model

/-! ## Dual certificate identity (WHITEPAPER §18.9) -/

/-- **Exact-Integer Dual Certificate Identity (paper §18.9).** For any finite
    free-ring residue structure, any non-negative integer tick weights, any
    integer scale D > 0, and every valid integer phase cover (every
    positively weighted tick is covered by some ring; y_p ∈ {0,1} is the
    rotation indicator of phase c_p):

    D·(F + Σ_p y_p) ≥ TotalNum

    with TotalNum = D·F + Σ_k (1−f(k))·u_k − Σ_p max(0, M_p − W_p(0) − D).
    This is the pure algebra behind the solver-free Python verifiers
    (`verify_dual.py`, the CBB leaf certificates). -/
theorem dual_certificate_identity_headline {ι κ : Type*} [Fintype ι]
    [Fintype κ] (n : ι → ℕ) [∀ p, NeZero (n p)]
    (hn : ∀ p, 2 ≤ n p)
    (r : ∀ p, κ → ZMod (n p)) (u : κ → ℤ) (hu : ∀ k, 0 ≤ u k)
    (D : ℤ) (hD : 0 < D) (c : ∀ p, ZMod (n p)) (y : ι → ℤ)
    (hl : ∀ p, (y p = 0 ∧ c p = 0) ∨ (y p = 1 ∧ c p ≠ 0))
    (hcover : ∀ k, 0 < u k → ∃ p, c p = r p k) (F : ℤ) :
    D * (F + ∑ p, y p) ≥ dualTotalNum n u r hn D F :=
  Wheel.dual_certificate_identity n hn r u hu D hD c y hl hcover F

/-- **Solver form of the dual identity (paper §18.9).** For every valid
    cover, the exact ceiling division of the Python verifiers,
    (TotalNum + D − 1) / D, is a certified lower bound on the rotation count
    F + Σ_p y_p. -/
theorem dual_certificate_lb_floor_headline {ι κ : Type*} [Fintype ι]
    [Fintype κ] (n : ι → ℕ) [∀ p, NeZero (n p)]
    (hn : ∀ p, 2 ≤ n p)
    (r : ∀ p, κ → ZMod (n p)) (u : κ → ℤ) (hu : ∀ k, 0 ≤ u k)
    (D : ℤ) (hD : 0 < D) (c : ∀ p, ZMod (n p)) (y : ι → ℤ)
    (hl : ∀ p, (y p = 0 ∧ c p = 0) ∨ (y p = 1 ∧ c p ≠ 0))
    (hcover : ∀ k, 0 < u k → ∃ p, c p = r p k) (F : ℤ) :
    (dualTotalNum n u r hn D F + D - 1) / D ≤ F + ∑ p, y p :=
  Wheel.dual_certificate_lb_floor n hn r u hu D hD c y hl hcover F

/-! ## Erdős covering necessity (WHITEPAPER §18.12) -/

/-- **Equal-fiber CRT count (paper §18.12).** If m ∣ L and a is a unit mod m,
    the units mod L reducing to a number exactly φ(L)/φ(m):
    fiber · φ(m) = φ(L).  (Reduction on unit groups is surjective; each
    nonempty fiber is a coset of the kernel, pinned by Lagrange.) -/
theorem erdos_fiber_coprime_headline {L m : ℕ} [NeZero L] (hm : m ∣ L)
    {a : ZMod m} (ha : IsUnit a) :
    Fintype.card {x : (ZMod L)ˣ // (ZMod.castHom hm (ZMod m) (x : ZMod L)) = a}
      * m.totient = L.totient :=
  Wheel.erdos_fiber_coprime hm ha

/-- **Covering necessity (paper §18.12), the S(L) ≥ 1 condition.** If a family
    of moduli D (all dividing L), each equipped with a residue class a_m
    coprime to its modulus, covers every unit modulo L, then
    Σ_{m ∈ D} φ(L)/φ(m) ≥ φ(L) — dividing out φ(L), the sum of reciprocal
    totients is at least 1.  This is the necessary condition for a
    distinct-odd covering system. -/
theorem erdos_covering_necessary_headline {L : ℕ} [NeZero L] {D : Finset ℕ}
    (hD : ∀ m ∈ D, m ∣ L)
    (a : ∀ m : ↥D, ZMod m.1) (ha : ∀ m : ↥D, IsUnit (a m))
    (hcover : ∀ x : (ZMod L)ˣ, ∃ m : ↥D,
      (ZMod.castHom (hD m.1 m.2) (ZMod m.1)) (x : ZMod L) = a m) :
    L.totient ≤ ∑ m : ↥D, L.totient / m.1.totient :=
  Wheel.erdos_covering_necessary hD a ha hcover

end Wheel
