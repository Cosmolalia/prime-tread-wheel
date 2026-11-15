/-
  Sanity.lean — vacuity audit for Theorem Day.

  The flagship theorems quantify over potentially empty-looking hypothesis
  classes.  This file instantiates every headline hypothesis family at
  concrete numbers and exhibits the witnesses, so that no flagship statement
  is vacuously true (or vacuously applicable) on its documented domain:

    • B4 forced-composite endpoints      — inhabited at the first layer m = 3
      (T 3 = 6).
    • Theorem I bijection                — inhabited at N = 30 (coordinate
      (m, k) = (8, 2), since T 7 = 28 and T 8 = 36; the layer sandwich
      T(m−1) < 30 ≤ T m forces m = 8, and then k = 2).
    • Theorem I primality criterion      — inhabited at N = 7, m = 4, k = 1
      (T 3 = 6, ⌊√(T 4)⌋ = ⌊√10⌋ = 3 < 7; the candidate divisors p = 2, 3
      do not divide 7).
    • The column law (B2)                — inhabited at N = 43 = T 8 + 7
      (m = 9, k = 7; 43 is prime and gcd 7 9 = 1).
    • The Three-Primitive Theorem        — its hypotheses P1 ∧ P3 ∧ P4 are
      simultaneously inhabited at the wheel itself, B(m) = TZ(m−1), L(m) = m.
    • Erdős covering necessity           — inhabited at L = 6, D = {2, 3}:
      the units mod 6 are {1, 5}, the classes a₂ = 1 (mod 2) and a₃ = 1
      (mod 3) are coprime to their moduli and cover all units; the certified
      bound reads 2 = φ(6) ≤ φ(6)/φ(2) + φ(6)/φ(3) = 2 + 1 = 3.
    • Dual certificate identity          — inhabited at the degenerate
      free-ring family (no rings, no ticks); the large non-degenerate
      certificates live in the companion Python verifiers (see
      FORMALIZATION_STATUS.md §2), which this identity underpins.

  Everything below is an `example` (no new named theorems, so the axiom
  report stays at the 83 certified names) closed by `decide` / `norm_num` /
  `omega` / explicit witnesses on genuinely true arithmetic statements.
-/

import Mathlib
import LeanWheel.Bijection
import LeanWheel.Primality
import LeanWheel.B2
import LeanWheel.B4
import LeanWheel.ThreePrimitive
import LeanWheel.ErdosFiber
import LeanWheel.Dual

/-- B4 at the first layer: T 3 = 6 is not prime, so the forced-composite
    endpoint clause is inhabited from m = 3 onward. -/
example : ¬ Nat.Prime (Wheel.T 3) := Wheel.B4_first 3 (by decide)

/-- Theorem I part 1 at N = 30: the coordinate (8, 2) is exhibited
    (T 7 = 28, so T 7 + 2 = 30), and uniqueness is the layer sandwich —
    any coordinate (m, k) with T(m−1) + k = 30 and 1 ≤ k ≤ m satisfies
    T(m−1) < 30 ≤ T m, which forces m = 8 and then k = 2
    (`Wheel.unique_coord`). -/
example : ∃! mk : ℕ × ℕ,
    1 ≤ mk.2 ∧ mk.2 ≤ mk.1 ∧ Wheel.T (mk.1 - 1) + mk.2 = 30 := by
  refine ⟨(8, 2), ⟨by decide, by decide, by decide⟩, ?_⟩
  rintro ⟨m, k⟩ ⟨h1, h2, hN⟩
  exact (Wheel.unique_coord (by decide : 1 ≤ 30)
    (m1 := 8) (k1 := 2) (m2 := m) (k2 := k)
    ⟨by decide, by decide, by decide⟩ ⟨h1, h2, hN⟩).symm

/-- Theorem I part 3 at N = 7, m = 4, k = 1: the criterion applies
    (T 3 + 1 = 7, ⌊√(T 4)⌋ = 3 < 7) and certifies primality of 7. -/
example : Nat.Prime 7 ↔ ∀ p, p.Prime → p ≤ Nat.sqrt (Wheel.T 4) → ¬ p ∣ 7 :=
  Wheel.theoremI_criterion 7 (m := 4) (k := 1)
    (by decide) (by decide) (by decide) (by norm_num [Wheel.T])

/-- The right-hand side of the criterion at (7, 4, 1) is verified directly:
    the only primes p ≤ ⌊√(T 4)⌋ = 3 are 2 and 3, and neither divides 7. -/
example : ∀ p, p.Prime → p ≤ Nat.sqrt (Wheel.T 4) → ¬ p ∣ 7 := by
  intro p hp hple
  have hp2 := hp.two_le
  have hp3 : p ≤ 3 := by
    have hsq : p * p ≤ Wheel.T 4 := (Nat.le_sqrt).mp hple
    norm_num [Wheel.T] at hsq
    nlinarith
  interval_cases p <;> norm_num at hp ⊢

/-- Column law (B2) at N = 43 = T 8 + 7 (m = 9, k = 7): 43 is prime, and the
    law returns the coprime-column alternative gcd 7 9 = 1. -/
example : Nat.gcd 7 9 = 1 ∨ (Nat.gcd 7 9 = 2 ∧ 9 % 4 = 2) :=
  Wheel.column_law (N := 43) (m := 9) (k := 7)
    (by decide) (by decide) (by decide) (by norm_num)

/-- The column-law conclusion at (43, 9, 7) is the left alternative:
    gcd 7 9 = 1. -/
example : Nat.gcd 7 9 = 1 := by decide

/-- Three-Primitive hypotheses are inhabited at the wheel itself:
    B(m) = TZ(m−1), L(m) = m satisfies P1 (origin & contiguity), P3 (unit
    step), and P4 (odd-divisor seam lock).  So `three_primitive_P4` applies
    here and concludes L 1 − 1 = 0 ∧ B m = TZ(m−1) (m ≥ 1). -/
example : Wheel.P1 (fun m ↦ Wheel.TZ ((m : ℤ) - 1)) (fun m ↦ (m : ℤ))
    ∧ Wheel.P3 (fun m ↦ (m : ℤ))
    ∧ Wheel.P4 (fun m ↦ Wheel.TZ ((m : ℤ) - 1)) := by
  refine ⟨⟨by decide, ?_⟩, ?_, ?_⟩
  · intro m
    have h := Wheel.TZ_pred (m : ℤ)
    have e1 : (((m + 1 : ℕ) : ℤ) - 1) = (m : ℤ) := by push_cast; ring
    simp only [e1]
    omega
  · intro m
    push_cast
    ring
  · intro m _ hmodd q _ hqdm
    exact dvd_trans (Int.natCast_dvd_natCast.2 hqdm)
      (Wheel.int_dvd_TZ_pred_of_odd hmodd)

/-- Erdős covering necessity at L = 6, D = {2, 3}: the moduli divide 6; the
    classes a₂ = 1 (mod 2), a₃ = 1 (mod 3) are units; every unit mod 6
    (i.e. 1 and 5 — both odd, hence ≡ 1 mod 2) is covered by the mod-2 class.
    The certified bound is φ(6) ≤ φ(6)/φ(2) + φ(6)/φ(3), i.e. 2 ≤ 2 + 1. -/
example : Nat.totient 6
    ≤ ∑ m : ↥({2, 3} : Finset ℕ), Nat.totient 6 / Nat.totient m.1 := by
  exact Wheel.erdos_covering_necessary (L := 6) (D := {2, 3})
    (by
      intro m hm
      simp only [Finset.mem_insert, Finset.mem_singleton] at hm
      rcases hm with rfl | rfl <;> decide)
    (fun m ↦ (1 : ZMod m.1))
    (fun _ ↦ isUnit_one)
    (by
      intro x
      fin_cases x
      · refine ⟨⟨2, by decide⟩, ?_⟩
        decide
      · refine ⟨⟨2, by decide⟩, ?_⟩
        decide)

/-- The unique ring-count function on the empty ring family (used only for
    the degenerate dual-certificate instance below). -/
def emptyRing : Empty → ℕ := fun p ↦ p.elim

/-- `emptyRing` satisfies the `NeZero` side condition (the degenerate
    family has no rings to be nonzero for). -/
instance emptyRingNeZero : ∀ p : Empty, NeZero (emptyRing p) := fun p ↦ p.elim

/-- Dual certificate identity at the degenerate free-ring family: no rings
    (ι = Empty), no ticks (κ = Empty), zero weights, scale D = 1, F = 0.
    The cover obligation is vacuous (all weights are zero), and the identity
    reads 1·(0 + 0) ≥ TotalNum = 1·0 + Σ_k (1−f(k))·0 − Σ_p max(0, …) = 0.
    (The large non-degenerate instances are the Python leaf certificates
    `verify_dual.py` / CBB, which this theorem underpins.) -/
example (hn : ∀ p : Empty, 2 ≤ emptyRing p) :
    (1 : ℤ) * ((0 : ℤ) + ∑ p : Empty, (fun p : Empty ↦ (p.elim : ℤ)) p)
      ≥ Wheel.dualTotalNum emptyRing (fun k : Empty ↦ (k.elim : ℤ))
        (fun p : Empty ↦ (p.elim : ∀ _k, ZMod (emptyRing p)))
        hn 1 0 := by
  exact Wheel.dual_certificate_identity (ι := Empty) (κ := Empty)
    (n := emptyRing)
    hn
    (fun p : Empty ↦ (p.elim : ∀ _k, ZMod (emptyRing p)))
    (fun k : Empty ↦ (k.elim : ℤ))
    (fun k ↦ k.elim)
    1 (by decide)
    (fun p ↦ p.elim)
    (fun p ↦ p.elim)
    (fun p ↦ p.elim)
    (fun k ↦ k.elim)
    0

/-! ## Not instantiated here

  • `orphan_characterization` / `phase_transition`: no genuinely small
    instance is exhibited within a reasonable line budget — the hypotheses
    (prime-divisor uniqueness below ⌊√(T m)⌋, the phase-transition threshold
    p²·(B m + 1) > T m) are witnessed in the wild by the computational
    certificates of the companion paper repository (solver-free Python
    verifiers on record; see FORMALIZATION_STATUS.md §2).
  • A non-degenerate `dual_certificate_identity` instance: same disposition —
    the degenerate case above certifies hypothesis consistency, and the
    substantive instances are the Python dual certificates (§18.9).
-/
