/-
  B1 — the visible set is exactly the primes (WHITEPAPER §4, B1).

  A composite value inside layer m has a prime factor p ≤ √(T m) < m, so the
  wheel at layer m is the √N sieve rendered as occlusion: uncovered ⟹ prime.
  Companion: a prime layer value admits no wheel-prime factor other than
  itself (the trivial self-cover of the layer floor).
-/

import Mathlib
import LeanWheel.Defs
import LeanWheel.Primality

namespace Wheel

/-- √(T m) < m for m ≥ 2: the layer floor stays strictly below m² since
    2·(T m) = m·(m+1) < 2·m². -/
theorem sqrt_Tm_lt (m : ℕ) (hm : 2 ≤ m) : Nat.sqrt (T m) < m := by
  have hsq : T m < m ^ 2 := by nlinarith [two_mul_T m]
  by_contra h
  push_neg at h
  have h1 := Nat.le_sqrt.1 h
  rw [pow_two] at hsq
  omega

/-- B1 — a composite value in the layer has a wheel-prime factor p ≤ m. -/
theorem B1 {N m k : ℕ} (hk : 1 ≤ k) (hkm : k ≤ m) (hN : N = T (m - 1) + k)
    (hN2 : 2 ≤ N) (hcomp : ¬ N.Prime) :
    ∃ p, p.Prime ∧ p ∣ N ∧ p ≤ m := by
  have hm2 : 2 ≤ m := by
    by_contra h
    push_neg at h
    interval_cases m
    · omega
    · rw [hN, show T (1 - 1) = 0 from rfl] at hN2
      omega
  have hNm : N ≤ T m := by
    rw [hN]
    have h1 := T_pred m (by omega : 1 ≤ m)
    omega
  obtain ⟨p, hp, hpdvd, hple⟩ := exists_prime_le_sqrt_of_not_prime hN2 hcomp
  refine ⟨p, hp, hpdvd, ?_⟩
  have h1 : p ≤ Nat.sqrt (T m) := le_trans hple (Nat.sqrt_le_sqrt hNm)
  have h2 := sqrt_Tm_lt m hm2
  omega

/-- B1 companion — a prime layer value is m-rough: no wheel prime p ≤ m
    divides it except itself (the trivial self-cover at the layer floor). -/
theorem B1_rough {N m k : ℕ} (_hk : 1 ≤ k) (_hkm : k ≤ m) (_hN : N = T (m - 1) + k)
    (hNp : N.Prime) (p : ℕ) (hp : p.Prime) (_hpm : p ≤ m) (hpdvd : p ∣ N) : N = p := by
  rcases hNp.eq_one_or_self_of_dvd p hpdvd with h1 | h2
  · rw [h1] at hp
    exact absurd hp Nat.not_prime_one
  · exact h2.symm

end Wheel
