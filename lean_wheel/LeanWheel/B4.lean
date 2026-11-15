/-
  B4 — forced-composite endpoints (WHITEPAPER §4, B4).

      T(m)   is composite for all m ≥ 3;
      T(m)−1 is composite for all m ≥ 4.

  The paper gives the identities  T(m) = m(m+1)/2  and  T(m)−1 = (m−1)(m+2)/2.
  "Composite" is taken in the standard arithmetic sense: the number is ≥ 2 and
  not prime (equivalently it has a divisor strictly between 1 and itself).
  The proofs split on the parity of m so that the factor 2 lands on one factor.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- Small helper: for 0 < a and 2 ≤ b, a < a * b over ℕ. -/
private lemma lt_mul_right_nat {a b : ℕ} (ha : 0 < a) (hb : 2 ≤ b) : a < a * b := by
  obtain ⟨c, rfl⟩ := Nat.exists_eq_add_of_le hb
  have hpos : 0 < a * (c + 1) := Nat.mul_pos ha (by omega)
  exact (Nat.lt_add_of_pos_right hpos).trans_eq (by ring)

/-- The second endpoint identity: 2·(T m − 1) = (m−1)(m+2) for m ≥ 1. -/
lemma two_mul_T_sub_one (m : ℕ) (hm : 1 ≤ m) : 2 * (T m - 1) = (m - 1) * (m + 2) := by
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le hm
  rw [add_comm 1 r, Nat.add_sub_cancel]
  have h1 := two_mul_T (r + 1)
  have hT : 1 ≤ T (r + 1) := by
    have h := T_succ r
    omega
  have e : (r + 1) * (r + 1 + 1) = r * (r + 1 + 2) + 2 := by ring
  omega

/-- T(m) is composite for all m ≥ 3. -/
theorem B4_first (m : ℕ) (hm : 3 ≤ m) : ¬ (T m).Prime := by
  rcases Nat.even_or_odd m with ⟨r, hr⟩ | ⟨r, hr⟩
  · -- m even: m = 2r with r ≥ 2, and T m = r(2r+1).
    have hr' : m = 2 * r := by omega
    subst hr'
    have hr2 : 2 ≤ r := by omega
    have hTm : T (2 * r) = r * (2 * r + 1) := by
      have h1 := two_mul_T (2 * r)
      have h2 : 2 * (r * (2 * r + 1)) = (2 * r) * (2 * r + 1) := by ring
      omega
    rw [hTm]
    refine Nat.not_prime_of_dvd_of_ne (Nat.dvd_mul_right r (2 * r + 1)) (by omega) ?_
    exact ne_of_lt (lt_mul_right_nat (by omega) (by omega))
  · -- m odd: m = 2r+1 with r ≥ 1, and T m = (2r+1)(r+1).
    have hr' : m = 2 * r + 1 := by omega
    subst hr'
    have hr1 : 1 ≤ r := by omega
    have hTm : T (2 * r + 1) = (2 * r + 1) * (r + 1) := by
      have h1 := two_mul_T (2 * r + 1)
      have h2 : 2 * ((2 * r + 1) * (r + 1)) = (2 * r + 1) * (2 * r + 2) := by ring
      have h3 : 2 * r + 1 + 1 = 2 * r + 2 := by omega
      rw [h3] at h1
      omega
    rw [hTm]
    refine Nat.not_prime_of_dvd_of_ne (Nat.dvd_mul_right (2 * r + 1) (r + 1)) (by omega) ?_
    exact ne_of_lt (lt_mul_right_nat (by omega) (by omega))

/-- T(m) − 1 is composite for all m ≥ 4. -/
theorem B4_second (m : ℕ) (hm : 4 ≤ m) : ¬ (T m - 1).Prime := by
  have hm1 : 1 ≤ m := by omega
  rcases Nat.even_or_odd m with ⟨r, hr⟩ | ⟨r, hr⟩
  · -- m even: m = 2r with r ≥ 2, and T m − 1 = (2r−1)(r+1).
    have hr' : m = 2 * r := by omega
    subst hr'
    have hr2 : 2 ≤ r := by omega
    have hTm : T (2 * r) - 1 = (2 * r - 1) * (r + 1) := by
      have h1 := two_mul_T_sub_one (2 * r) (by omega)
      have h2 : 2 * ((2 * r - 1) * (r + 1)) = (2 * r - 1) * (2 * r + 2) := by
        obtain ⟨s, rfl⟩ := Nat.exists_eq_add_of_le hr2
        rw [show 2 * (2 + s) - 1 = 2 * s + 3 by omega]
        ring
      have hT : 1 ≤ T (2 * r) := by
        have h := T_succ (2 * r - 1)
        have hm : 2 * r - 1 + 1 = 2 * r := by omega
        rw [hm] at h
        omega
      omega
    rw [hTm]
    have h1 : 2 * r - 1 ≠ 1 := by omega
    refine Nat.not_prime_of_dvd_of_ne (Nat.dvd_mul_right (2 * r - 1) (r + 1)) h1 ?_
    exact ne_of_lt (lt_mul_right_nat (by omega) (by omega))
  · -- m odd: m = 2r+1 with r ≥ 2, and T m − 1 = r(2r+3).
    have hr' : m = 2 * r + 1 := by omega
    subst hr'
    have hr2 : 2 ≤ r := by omega
    have hTm : T (2 * r + 1) - 1 = r * (2 * r + 3) := by
      have h1 := two_mul_T_sub_one (2 * r + 1) (by omega)
      have h2 : 2 * (r * (2 * r + 3)) = (2 * r) * (2 * r + 3) := by ring
      have h3 : 2 * r + 1 - 1 = 2 * r := by omega
      have h4 : 2 * r + 1 + 2 = 2 * r + 3 := by omega
      have hT : 1 ≤ T (2 * r + 1) := by
        have h := T_succ (2 * r)
        omega
      rw [h3, h4] at h1
      omega
    rw [hTm]
    refine Nat.not_prime_of_dvd_of_ne (Nat.dvd_mul_right r (2 * r + 3)) (by omega) ?_
    exact ne_of_lt (lt_mul_right_nat (by omega) (by omega))

end Wheel
