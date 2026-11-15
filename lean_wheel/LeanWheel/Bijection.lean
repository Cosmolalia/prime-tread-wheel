/-
  Theorem I part 1 — the triangular coordinate bijection.

  Paper (§19.1.1): the map Φ(m, k) = T(m−1) + k with 1 ≤ k ≤ m is a bijection
  between {(m,k) : 1 ≤ k ≤ m} and ℤ_{≥1}.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- Theorem I part 1 — existence, by strong induction (peeling the last tick). -/
theorem exists_coord (N : ℕ) (hN : 1 ≤ N) :
    ∃ m k : ℕ, 1 ≤ k ∧ k ≤ m ∧ T (m - 1) + k = N := by
  induction N using Nat.strong_induction_on with
  | _ N IH =>
    rcases Nat.lt_or_ge N 2 with hN1 | hN2
    · interval_cases N
      exact ⟨1, 1, by omega, by omega, by simp [T]⟩
    · have h1 : 1 ≤ N - 1 := by omega
      obtain ⟨m, k, hk1, hkm, hNk⟩ := IH (N - 1) (by omega) h1
      rcases Nat.lt_or_ge k m with hklt | hkge
      · refine ⟨m, k + 1, by omega, by omega, ?_⟩
        omega
      · have hk : k = m := le_antisymm hkm hkge
        have hTm : T m = T (m - 1) + m := T_self_sub_add m
        refine ⟨m + 1, 1, by omega, by omega, ?_⟩
        rw [Nat.add_sub_cancel]
        omega

/-- Theorem I part 1 — uniqueness (layer sandwich). -/
theorem unique_coord {N : ℕ} (hN : 1 ≤ N) {m1 k1 m2 k2 : ℕ}
    (h1 : 1 ≤ k1 ∧ k1 ≤ m1 ∧ T (m1 - 1) + k1 = N)
    (h2 : 1 ≤ k2 ∧ k2 ≤ m2 ∧ T (m2 - 1) + k2 = N) :
    (m1, k1) = (m2, k2) := by
  have hm1lo : T (m1 - 1) < N := by omega
  have hm1hi : N ≤ T m1 := by
    have hpred := T_pred m1 (by omega : 1 ≤ m1)
    omega
  have hm2lo : T (m2 - 1) < N := by omega
  have hm2hi : N ≤ T m2 := by
    have hpred := T_pred m2 (by omega : 1 ≤ m2)
    omega
  have hmeq : m1 = m2 := by
    rcases Nat.lt_trichotomy m1 m2 with h | h | h
    · have h1' : T m1 ≤ T (m2 - 1) := T_mono (by omega)
      omega
    · exact h
    · have h2' : T m2 ≤ T (m1 - 1) := T_mono (by omega)
      omega
  have hkeq : k1 = k2 := by
    have e1 : T (m1 - 1) + k1 = T (m2 - 1) + k2 := h1.2.2.trans h2.2.2.symm
    rw [hmeq] at e1
    omega
  exact Prod.ext hmeq hkeq

/-- Theorem I part 1 — the coordinate bijection, packaged as ∃! over ℕ × ℕ. -/
theorem theoremI_bijection (N : ℕ) (hN : 1 ≤ N) :
    ∃! mk : ℕ × ℕ, 1 ≤ mk.2 ∧ mk.2 ≤ mk.1 ∧ T (mk.1 - 1) + mk.2 = N := by
  obtain ⟨m, k, hk1, hkm, hNk⟩ := exists_coord N hN
  refine ⟨(m, k), by exact ⟨hk1, hkm, hNk⟩, ?_⟩
  rintro ⟨m2, k2⟩ ⟨hk21, hk2m, hNk2⟩
  exact (unique_coord hN ⟨hk1, hkm, hNk⟩ ⟨hk21, hk2m, hNk2⟩).symm

end Wheel
