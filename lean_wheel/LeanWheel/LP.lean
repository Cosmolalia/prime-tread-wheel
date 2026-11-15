/-
  Theorem IV part 2 — feasibility of an explicit point in the formally-defined
  finite LP relaxation (WHITEPAPER §19.4, the "optional enrichment" of the
  report, closing the paper's LP story in the kernel).

  Variables x_{p,c} for p ∈ {2,3,5}, c ∈ {1,…,p−1}.  Constraints:
    row bounds   Σ_{c=1}^{p−1} x_{p,c} ≤ 1           (p ∈ {2,3,5}),
    coverage     Σ_{p ∤ N} x_{p, N mod p}
               + Σ_{p ∣ N} (1 − Σ_{c=1}^{p−1} x_{p,c}) ≥ 1   (N = T(m−1)+k).
  The exhibited point x_{p,c} = α_p/p (with α₂ = α₃ = 1, α₅ = 5/6) satisfies
  every constraint on every layer; its objective value is 11/6
  (`smear_cost`), so the relaxation's optimum is ≤ 11/6.
-/

import Mathlib
import LeanWheel.Defs
import LeanWheel.Smear

namespace Wheel

/-- The exhibited point: x_{p,c} = α_p/p on {2,3,5} × {1,…,p−1}, else 0. -/
def xSmear (p c : ℕ) : ℚ :=
  if (p ∈ ({2, 3, 5} : Finset ℕ) ∧ 1 ≤ c ∧ c ≤ p - 1) then (α p : ℚ) / p else 0

/-- Every c ∈ {1,…,p−1} with p ∈ {2,3,5} contributes α_p/p to the row. -/
theorem xSmear_sum_Ico (p : ℕ) (hp : p ∈ ({2, 3, 5} : Finset ℕ)) :
    ∑ c ∈ Finset.Icc 1 (p - 1), xSmear p c =
      ((Finset.Icc 1 (p - 1)).card : ℚ) * (α p / p) := by
  have h : ∀ c ∈ Finset.Icc 1 (p - 1), xSmear p c = α p / p := by
    intro c hc
    have h1 : 1 ≤ c := (Finset.mem_Icc.1 hc).1
    have h2 : c ≤ p - 1 := (Finset.mem_Icc.1 hc).2
    simp [xSmear, hp, h1, h2]
  rw [Finset.sum_eq_card_nsmul h, nsmul_eq_mul]

/-- Row bound: Σ_{c=1}^{p−1} xSmear p c = (p−1)·α_p/p ≤ 1 for p ∈ {2,3,5}. -/
theorem xSmear_row_le (p : ℕ) (hp : p ∈ ({2, 3, 5} : Finset ℕ)) :
    ∑ c ∈ Finset.Icc 1 (p - 1), xSmear p c ≤ 1 := by
  rw [xSmear_sum_Ico p hp, Nat.card_Icc]
  simp only [Finset.mem_insert, Finset.mem_singleton] at hp
  rcases hp with rfl | rfl | rfl <;> norm_num [α]

/-- Per-tick coverage: for N = T(m−1)+k the exhibited point's coverage equals
    Σ_{p ∈ {2,3,5}} smearTerm p N ≥ 1. -/
theorem xSmear_covers (N : ℕ) :
    1 ≤ ∑ p ∈ ({2, 3, 5} : Finset ℕ),
      (if p ∣ N then 1 - ∑ c ∈ Finset.Icc 1 (p - 1), xSmear p c
       else xSmear p (N % p)) := by
  calc 1 ≤ ∑ p ∈ ({2, 3, 5} : Finset ℕ), smearTerm p N := smear_coverage N
    _ = ∑ p ∈ ({2, 3, 5} : Finset ℕ),
        (if p ∣ N then 1 - ∑ c ∈ Finset.Icc 1 (p - 1), xSmear p c
         else xSmear p (N % p)) := by
        apply Finset.sum_congr rfl
        intro p hp
        by_cases hpd : p ∣ N
        · rw [if_pos hpd]
          have hrow := xSmear_sum_Ico p hp
          rw [Nat.card_Icc] at hrow
          rw [hrow]
          simp only [Finset.mem_insert, Finset.mem_singleton] at hp
          rcases hp with rfl | rfl | rfl <;>
            simp [smearTerm, α, hpd] <;> norm_num
        · rw [if_neg hpd]
          have hp2 : 2 ≤ p := by
            simp only [Finset.mem_insert, Finset.mem_singleton] at hp
            rcases hp with rfl | rfl | rfl <;> norm_num
          have h1 : 1 ≤ N % p :=
            Nat.pos_of_ne_zero (fun h0 ↦ hpd (Nat.dvd_of_mod_eq_zero h0))
          have h2 : N % p ≤ p - 1 := by
            have h3 : N % p < p := Nat.mod_lt _ (by omega)
            omega
          simp [xSmear, hp, h1, h2, smearTerm, hpd]

/-- §19.4 — the exhibited point is feasible for the continuous relaxation on
    every layer: row bounds on {2,3,5} and coverage of every tick k ∈ [1,m].
    (Objective value 11/6 by `smear_cost`, so the LP optimum ≤ 11/6.) -/
theorem lp_relaxation_feasible (m : ℕ) :
    (∀ p ∈ ({2, 3, 5} : Finset ℕ), ∑ c ∈ Finset.Icc 1 (p - 1), xSmear p c ≤ 1) ∧
    (∀ k ∈ Finset.Icc 1 m,
      1 ≤ ∑ p ∈ ({2, 3, 5} : Finset ℕ),
        (if p ∣ (T (m - 1) + k) then 1 - ∑ c ∈ Finset.Icc 1 (p - 1), xSmear p c
         else xSmear p ((T (m - 1) + k) % p))) :=
  ⟨fun p hp ↦ xSmear_row_le p hp, fun k _ ↦ xSmear_covers (T (m - 1) + k)⟩

end Wheel
