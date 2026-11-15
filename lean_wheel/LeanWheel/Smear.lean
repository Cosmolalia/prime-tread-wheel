/-
  Theorem IV — the {2,3,5} harmonic LP smear (WHITEPAPER §19.4), the
  arithmetic kernel over ℚ.

  With α₂ = α₃ = 1 and α₅ = 5/6, the per-ring fractional coverage
      (if p ∤ N then α_p / p else 1 − (p−1)·α_p / p)
  sums to ≥ 1 on every tick N (equality exactly when 5 ∤ N), at total LP
  objective cost 11/6.

  This is the faithful kernel the paper's MILP story rests on; the formal
  feasibility-of-an-explicit-LP-point version is noted in the report.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- The smear coefficients: α₂ = α₃ = 1, α₅ = 5/6. -/
def α (p : ℕ) : ℚ := if p = 5 then 5 / 6 else 1

/-- The per-ring fractional coverage contribution at tick N: α_p/p on the
    non-multiples of p, and the home-coverage remainder 1 − (p−1)·α_p/p on the
    multiples. -/
def smearTerm (p : ℕ) (N : ℕ) : ℚ :=
  if p ∣ N then 1 - (p - 1) * (α p : ℚ) / p else (α p : ℚ) / p

/-- Theorem IV (coverage): Σ_{p ∈ {2,3,5}} smearTerm p N ≥ 1 for every N. -/
theorem smear_coverage (N : ℕ) :
    1 ≤ ({2, 3, 5} : Finset ℕ).sum (fun p ↦ smearTerm p N) := by
  by_cases h2 : (2 : ℕ) ∣ N <;> by_cases h3 : (3 : ℕ) ∣ N <;> by_cases h5 : (5 : ℕ) ∣ N <;>
    simp [Finset.sum_insert, Finset.sum_singleton, smearTerm, α, h2, h3, h5] <;>
    norm_num

/-- Theorem IV (coverage, exact): the sum equals 1 exactly when 5 ∤ N. -/
theorem smear_coverage_eq_one_iff (N : ℕ) :
    ({2, 3, 5} : Finset ℕ).sum (fun p ↦ smearTerm p N) = 1 ↔ ¬ (5 : ℕ) ∣ N := by
  constructor
  · intro heq
    by_contra h5
    have h4 : ({2, 3, 5} : Finset ℕ).sum (fun p ↦ smearTerm p N) = 7 / 6 := by
      by_cases h2 : (2 : ℕ) ∣ N <;> by_cases h3 : (3 : ℕ) ∣ N <;>
        simp [Finset.sum_insert, Finset.sum_singleton, smearTerm, α, h2, h3, h5] <;>
        norm_num
    rw [h4] at heq
    norm_num at heq
  · intro h5
    by_cases h2 : (2 : ℕ) ∣ N <;> by_cases h3 : (3 : ℕ) ∣ N <;>
      simp [Finset.sum_insert, Finset.sum_singleton, smearTerm, α, h2, h3, h5] <;>
      norm_num

/-- Theorem IV (cost): (2−1)/2·1 + (3−1)/3·1 + (5−1)/5·(5/6) = 11/6. -/
theorem smear_cost :
    ((2 - 1 : ℚ) / 2 * 1 + (3 - 1) / 3 * 1 + (5 - 1) / 5 * (5 / 6)) = 11 / 6 := by
  norm_num

end Wheel
