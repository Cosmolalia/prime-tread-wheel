/-
  Theorem V — the exact harmonic smear threshold p − 1 < L (WHITEPAPER §19.5),
  the break-even algebra over ℝ.

  Both the first-order and the second-order fractional smears are profitable
  exactly when p − 1 < L:

      (L − (p−1)) / p       > 0  ↔  p − 1 < L     (p > 1)
      (L − (p−1)) / (p−1)   > 0  ↔  p − 1 < L     (p > 1)

  The paper's warrant for the underlying savings formulas is a heuristic
  (equidistribution of the dual weight); only the conditional algebra is
  formalized — see the report.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- First-order smear break-even. -/
theorem break_even_first (L p : ℝ) (hp : 1 < p) :
    0 < (L - (p - 1)) / p ↔ p - 1 < L := by
  have h2 : (0 : ℝ) < p := by linarith
  rw [div_pos_iff]
  constructor
  · rintro (⟨h1, _⟩ | ⟨h1, _⟩) <;> linarith
  · intro h1
    refine Or.inl ⟨?_, h2⟩
    linarith

/-- Second-order smear break-even. -/
theorem break_even_second (L p : ℝ) (hp : 1 < p) :
    0 < (L - (p - 1)) / (p - 1) ↔ p - 1 < L := by
  have h2 : (0 : ℝ) < p - 1 := by linarith
  rw [div_pos_iff]
  constructor
  · rintro (⟨h1, _⟩ | ⟨_, h1⟩) <;> linarith
  · intro h1
    refine Or.inl ⟨?_, h2⟩
    linarith

end Wheel
