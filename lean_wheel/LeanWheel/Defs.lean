/-
  Prime Tread Wheel — shared definitions.

  T(m) = m(m+1)/2 is the m-th triangular number.  Ticks on layer m are addressed
  (m, k) with 1 ≤ k ≤ m and carry the value N = T(m−1) + k.
  This file fixes the arithmetic backbone used by every certificate below:
  the triangular numbers over ℕ and ℤ, their defining two-fold covers
  (so the divisions are exact and justified), and the one-step recurrences.
-/

import Mathlib

namespace Wheel

/-- The m-th triangular number over ℕ. -/
def T : ℕ → ℕ := fun n ↦ n * (n + 1) / 2

/-- Triangular numbers over ℤ (the divisions below are justified by
    `two_mul_TZ`: the product n(n+1) is always even). -/
def TZ : ℤ → ℤ := fun n ↦ n * (n + 1) / 2

@[simp] lemma T_zero : T 0 = 0 := rfl

@[simp] lemma TZ_zero : TZ 0 = 0 := rfl

/-- Exactness of the division in `T`: 2 · T n = n(n+1). -/
lemma two_mul_T (n : ℕ) : 2 * T n = n * (n + 1) :=
  Nat.two_mul_div_two_of_even (Nat.even_mul_succ_self n)

/-- Exactness of the division in `TZ`: 2 · TZ n = n(n+1) over ℤ. -/
lemma two_mul_TZ (n : ℤ) : 2 * TZ n = n * (n + 1) := by
  rw [TZ, mul_comm, Int.ediv_mul_cancel (even_iff_two_dvd.1 (Int.even_mul_succ_self n))]

/-- One-step recurrence for T over ℕ. -/
lemma T_succ (n : ℕ) : T (n + 1) = T n + (n + 1) := by
  have h1 := two_mul_T (n + 1)
  have h2 : 2 * (T n + (n + 1)) = (n + 1) * (n + 1 + 1) := by
    rw [mul_add, two_mul_T n]
    ring
  omega

/-- For every m ≥ 1, T(m−1) + m = T(m). -/
lemma T_pred (m : ℕ) (hm : 1 ≤ m) : T (m - 1) + m = T m := by
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le hm
  rw [add_comm 1 r, Nat.add_sub_cancel]
  exact (T_succ r).symm

/-- For all m (including 0, where both sides are 0): T m = T (m−1) + m. -/
lemma T_self_sub_add (m : ℕ) : T m = T (m - 1) + m := by
  rcases Nat.eq_zero_or_pos m with rfl | h
  · rfl
  · exact (T_pred m h).symm

/-- One-step recurrence for TZ over ℤ. -/
lemma TZ_succ (n : ℤ) : TZ (n + 1) = TZ n + (n + 1) := by
  have h1 := two_mul_TZ (n + 1)
  have h2 : 2 * (TZ n + (n + 1)) = (n + 1) * (n + 1 + 1) := by
    rw [mul_add, two_mul_TZ n]
    ring
  omega

/-- For every m : ℤ, TZ(m−1) + m = TZ(m). -/
lemma TZ_pred (m : ℤ) : TZ (m - 1) + m = TZ m := by
  have h := TZ_succ (m - 1)
  rw [show m - 1 + 1 = m by ring] at h
  exact h.symm

/-- The lap-palindrome identity used by the Three-Primitive Theorem:
    T(−m) = T(m−1) over ℤ (both equal m(m−1)/2). -/
lemma TZ_neg (m : ℤ) : TZ (-m) = TZ (m - 1) := by
  have h1 := two_mul_TZ (-m)
  have h2 := two_mul_TZ (m - 1)
  have e : 2 * TZ (-m) = 2 * TZ (m - 1) := by rw [h1, h2]; ring
  exact mul_left_cancel₀ two_ne_zero e

/-- T is strictly monotone. -/
lemma T_strictMono : StrictMono T :=
  strictMono_nat_of_lt_succ fun n ↦ by rw [T_succ]; omega

/-- T is monotone. -/
lemma T_mono : Monotone T := T_strictMono.monotone

end Wheel
