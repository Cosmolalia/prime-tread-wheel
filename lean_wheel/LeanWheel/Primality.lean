/-
  Theorem I part 3 — the exact primality criterion (WHITEPAPER §19.1.3).

  For N = T(m−1) + k > ⌊√(T m)⌋ (with 1 ≤ k ≤ m):

      N is prime  ↔  ∀ prime p ≤ ⌊√(T m)⌋,  p ∤ N.

  The bridge is the classical fact that a composite N has a prime factor
  ≤ √N (formalized here as `exists_prime_le_sqrt_of_not_prime`).
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- Bridge: a composite N ≥ 2 has a prime factor ≤ √N. -/
theorem exists_prime_le_sqrt_of_not_prime {N : ℕ} (hN : 2 ≤ N) (hnp : ¬ N.Prime) :
    ∃ p, p.Prime ∧ p ∣ N ∧ p ≤ Nat.sqrt N := by
  refine ⟨N.minFac, Nat.minFac_prime (by omega : N ≠ 1), Nat.minFac_dvd N, ?_⟩
  have hlt : N.minFac < N := (Nat.not_prime_iff_minFac_lt hN).1 hnp
  obtain ⟨c, hc⟩ := Nat.minFac_dvd N
  have hc2 : 2 ≤ c := by
    rcases Nat.lt_or_ge c 2 with h | h
    · interval_cases c <;> omega
    · exact h
  have hle : N.minFac ≤ c := by
    rcases Nat.lt_or_ge c N.minFac with h | h
    · exact absurd (Nat.minFac_le_of_dvd hc2 (by rw [hc]; exact Nat.dvd_mul_left _ _))
        (not_le.2 h)
    · exact h
  have hsq : N.minFac * N.minFac ≤ N := by
    calc N.minFac * N.minFac ≤ N.minFac * c := mul_le_mul_right hle N.minFac
      _ = N := hc.symm
  exact Nat.le_sqrt.2 hsq

/-- Theorem I part 3 — the exact primality criterion inside a layer. -/
theorem theoremI_criterion (N : ℕ) {m k : ℕ} (hk : 1 ≤ k) (hkm : k ≤ m)
    (hN : N = T (m - 1) + k) (hbig : Nat.sqrt (T m) < N) :
    N.Prime ↔ ∀ p, p.Prime → p ≤ Nat.sqrt (T m) → ¬ p ∣ N := by
  constructor
  · intro hNp p hp hple hdiv
    rcases hNp.eq_one_or_self_of_dvd p hdiv with h | h
    · rw [h] at hp
      exact Nat.not_prime_one hp
    · subst h
      omega
  · intro h
    by_contra hnp
    have hm2 : 2 ≤ m := by
      by_contra hm
      push_neg at hm
      interval_cases m
      · omega
      · have hT1 : T 1 = 1 := rfl
        have hs1 : Nat.sqrt (T 1) = 1 := by rw [hT1]; exact Nat.sqrt_one
        have hT0 : T (1 - 1) = 0 := rfl
        omega
    have hN2 : 2 ≤ N := by
      rw [hN]
      have h1 : T 1 ≤ T (m - 1) := T_mono (by omega)
      have h2 : T 1 = 1 := rfl
      omega
    have hNm : N ≤ T m := by
      rw [hN]
      have hpred := T_pred m (by omega : 1 ≤ m)
      omega
    have hsqrt : Nat.sqrt N ≤ Nat.sqrt (T m) := Nat.sqrt_le_sqrt hNm
    obtain ⟨p, hp, hpdvd, hple⟩ := exists_prime_le_sqrt_of_not_prime hN2 hnp
    exact h p hp (le_trans hple hsqrt) hpdvd

end Wheel
