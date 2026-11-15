/-
  Theorem II part 1 — the orphan characterization (WHITEPAPER §19.2.1).

  With B := ⌊√(T(m−1))⌋ and m ≥ 3 (so T(m) < 2(B+1)² — proved here as
  `Tm_lt_two_mul_Bm_add_one_sq`; the paper records a 2026-10-25 GPT-audit repair
  of this very hypothesis), if p ≤ B is the UNIQUE prime factor ≤ B of
  N = T(m−1) + k ≤ T(m), then

      ∃ a ≥ 1,  N = p^a  ∨  (∃ Q, N = p^a · Q ∧ Q.Prime ∧ B < Q).

  Mechanism (paper): write N = p^a · Q with p ∤ Q; if Q > 1 were composite its
  least prime factor exceeds B, forcing Q ≥ (B+1)² > T(m)/2 ≥ N/p^a = Q.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- The wheel horizon B := ⌊√(T(m−1))⌋. -/
def Bm (m : ℕ) : ℕ := Nat.sqrt (T (m - 1))

/-- n ≤ T(n). -/
lemma le_T (n : ℕ) : n ≤ T n := by
  induction n with
  | zero => simp
  | succ r ih => rw [T_succ]; omega

/-- The repaired side hypothesis: for m ≥ 3, T(m) < 2(B+1)² with B = ⌊√(T(m−1))⌋.
    (The paper's original sufficient condition T(m) < 2B² failed at m = 5;
    this is the corrected form, verified for all m ≥ 3.) -/
theorem Tm_lt_two_mul_Bm_add_one_sq (m : ℕ) (hm : 3 ≤ m) :
    T m < 2 * (Bm m + 1) ^ 2 := by
  have h1 : T (m - 1) < (Bm m + 1) ^ 2 := Nat.lt_succ_sqrt' (T (m - 1))
  have h2 : T m = T (m - 1) + m := T_self_sub_add m
  have h3 : m ≤ T (m - 1) + 1 := by
    have h4 := le_T (m - 1)
    omega
  omega

/-- A composite N ≥ 2 has its least prime factor ≤ √N. -/
lemma minFac_sq_le_of_not_prime {N : ℕ} (hN : 2 ≤ N) (hnp : ¬ N.Prime) :
    N.minFac ^ 2 ≤ N := by
  have hq : N.minFac.Prime := Nat.minFac_prime (by omega : N ≠ 1)
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
  calc N.minFac ^ 2 = N.minFac * N.minFac := pow_two _
    _ ≤ N.minFac * c := Nat.mul_le_mul (le_refl _) hle
    _ = N := hc.symm

/-- Theorem II part 1 — orphan characterization. -/
theorem orphan_characterization (m p k : ℕ) (hm : 3 ≤ m)
    (hp : p.Prime) (hpB : p ≤ Bm m) (hpdvd : p ∣ (T (m - 1) + k))
    (hkle : T (m - 1) + k ≤ T m)
    (huniq : ∀ q : ℕ, q.Prime → q ≤ Bm m → q ∣ (T (m - 1) + k) → q = p) :
    ∃ a : ℕ, 1 ≤ a ∧
      (T (m - 1) + k = p ^ a ∨
        ∃ Q : ℕ, T (m - 1) + k = p ^ a * Q ∧ Q.Prime ∧ Bm m < Q) := by
  have hN0 : T (m - 1) + k ≠ 0 := by
    have h1 : T 2 ≤ T (m - 1) := T_mono (by omega)
    have h2 : T 2 = 3 := rfl
    omega
  obtain ⟨a, Q, hnp, hdecomp⟩ := Nat.exists_eq_pow_mul_and_not_dvd hN0 p hp.ne_one
  have ha : 1 ≤ a := by
    rcases Nat.eq_zero_or_pos a with h | h
    · rw [h, pow_zero, one_mul] at hdecomp
      rw [hdecomp] at hpdvd
      exact absurd hpdvd hnp
    · exact h
  refine ⟨a, ha, ?_⟩
  rcases Nat.lt_or_ge Q 2 with hQlt | hQge
  · interval_cases Q
    · rw [hdecomp, mul_zero] at hN0
      exact absurd rfl hN0
    · left
      rw [hdecomp, mul_one]
  · -- Q > 1.  If Q were composite, its least prime factor exceeds B and
    -- (B+1)² ≤ minFac(Q)² ≤ Q ≤ T(m)/2 < (B+1)², a contradiction.
    have hQp : Q.Prime := by
      by_contra hnc
      have hQ1 : 1 < Q := hQge
      have hmf_gt : Bm m < Q.minFac := by
        by_contra hle
        push_neg at hle
        have hmf_dvd_N : Q.minFac ∣ (T (m - 1) + k) :=
          dvd_trans (Nat.minFac_dvd Q) (by rw [hdecomp]; exact Nat.dvd_mul_left _ _)
        have heq := huniq _ (Nat.minFac_prime (by omega : Q ≠ 1)) hle hmf_dvd_N
        rw [← heq] at hnp
        exact hnp (Nat.minFac_dvd Q)
      have hsq : Q.minFac ^ 2 ≤ Q := minFac_sq_le_of_not_prime (by omega : 2 ≤ Q) hnc
      have hQ2 : 2 * Q ≤ T m := by
        have h1 : p ^ a * Q ≤ T m := by rw [← hdecomp]; exact hkle
        have h2 : 2 ≤ p ^ a := by
          obtain ⟨b, rfl⟩ := Nat.exists_eq_add_of_le ha
          rw [add_comm 1 b, pow_succ]
          have hpb : (0 : ℕ) < p ^ b := Nat.pow_pos hp.pos
          calc 2 = 1 * 2 := by norm_num
            _ ≤ p ^ b * p := Nat.mul_le_mul hpb hp.two_le
        have h3 : Q * 2 ≤ Q * p ^ a := Nat.mul_le_mul (le_refl Q) h2
        have h4 : Q * p ^ a = p ^ a * Q := mul_comm _ _
        omega
      have hchain : (Bm m + 1) ^ 2 ≤ Q.minFac ^ 2 :=
        pow_le_pow_left₀ (Nat.zero_le (Bm m + 1)) (by omega : Bm m + 1 ≤ Q.minFac) 2
      have hB := Tm_lt_two_mul_Bm_add_one_sq m hm
      omega
    refine Or.inr ⟨Q, hdecomp, hQp, ?_⟩
    by_contra hle
    push_neg at hle
    have hdvdN : Q ∣ (T (m - 1) + k) := by rw [hdecomp]; exact Nat.dvd_mul_left _ _
    have heq := huniq Q hQp hle hdvdN
    rw [heq] at hnp
    exact hnp (dvd_refl p)

end Wheel
