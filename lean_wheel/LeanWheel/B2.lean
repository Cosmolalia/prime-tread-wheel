/-
  B2 — the column law — and B5 — the m ≡ 2 (mod 4) seat-zero theorem
  (WHITEPAPER §4).

  B2: a prime value N = T(m−1)+k forces gcd(k,m) = 1 (the coprime columns),
  or the parity escape gcd(k,m) = 2 with m ≡ 2 (mod 4).  Mechanism: an odd
  prime factor of gcd(k,m) divides T(m−1) (since p ∣ m and p odd) hence
  divides N — impossible as p ≤ m < N; so the gcd is a power of 2, and 4 ∣ m
  would make T(m−1) and k both even, hence N even > 2.

  B5: on m ≡ 2 (mod 4) laps with m ≥ 6 the coprime columns are prime-free
  (the seat test is misaligned from value-divisibility by exactly m/2):
  k coprime to the even lap m is odd while T(m−1) = (m−1)(m/2) is odd, so
  N = T(m−1)+k is even and > 2.  Every prime sits on the parity-escape ticks
  gcd(k,m) = 2.  (The B6 density ratio 2.00× itself is measured [E] — its
  formalizable kernel is exactly this parity conditioning.)
-/

import Mathlib
import LeanWheel.Defs
import LeanWheel.Orphan

namespace Wheel

/-- A number with no prime divisor is 1. -/
private lemma eq_one_of_no_prime_dvd {n : ℕ} (hn : n ≠ 0)
    (h : ∀ p : ℕ, p.Prime → ¬ p ∣ n) : n = 1 := by
  by_contra hne
  have hp := Nat.minFac_prime hne
  have hd := Nat.minFac_dvd n
  exact h _ hp hd

/-- For even m: T(m−1) = (m−1)·(m/2), so the parity of T(m−1) is the parity
    of m/2 — even exactly when 4 ∣ m, odd exactly when m ≡ 2 (mod 4). -/
theorem T_pred_of_even {m : ℕ} (hm : Even m) : T (m - 1) = (m - 1) * (m / 2) := by
  obtain ⟨j, rfl⟩ := hm
  rcases Nat.eq_zero_or_pos j with rfl | hj
  · rfl
  · have h1 := two_mul_T (j + j - 1)
    have hs : j + j - 1 + 1 = j + j := by omega
    rw [hs] at h1
    have h2 : (j + j - 1) * (j + j) = 2 * ((j + j - 1) * j) := by ring
    have e2 : 2 * T (j + j - 1) = 2 * ((j + j - 1) * j) := by rw [h1, h2]
    rw [show (j + j) / 2 = j by omega]
    exact Nat.mul_left_cancel (by norm_num : 0 < 2) e2

/-- B2 — the column law.  A prime N = T(m−1)+k occurs only in an eligible
    column: gcd(k,m) = 1, or gcd(k,m) = 2 with m ≡ 2 (mod 4). -/
theorem column_law {N m k : ℕ} (hk : 1 ≤ k) (hkm : k ≤ m) (hN : N = T (m - 1) + k)
    (hNp : N.Prime) :
    Nat.gcd k m = 1 ∨ (Nat.gcd k m = 2 ∧ m % 4 = 2) := by
  -- No odd prime divides the gcd: such a p divides T(m−1) and k, hence N,
  -- and p ≤ m < N contradicts primality.
  have key : ∀ p : ℕ, p.Prime → p ∣ Nat.gcd k m → p = 2 := by
    intro p hp hpdvd
    have hpk : p ∣ k := hpdvd.trans (Nat.gcd_dvd_left k m)
    have hpm : p ∣ m := hpdvd.trans (Nat.gcd_dvd_right k m)
    by_contra hp2
    have hpodd : Odd p := hp.odd_of_ne_two hp2
    have hco : Nat.Coprime p 2 := (Nat.coprime_two_right).2 hpodd
    have h2T : p ∣ 2 * T (m - 1) := by
      have e := two_mul_T (m - 1)
      have hs : m - 1 + 1 = m := by omega
      rw [e, hs]
      exact dvd_mul_of_dvd_right hpm (m - 1)
    have hTm : p ∣ T (m - 1) := hco.dvd_of_dvd_mul_left h2T
    have hpN : p ∣ N := by rw [hN]; exact Nat.dvd_add hTm hpk
    have hpeq : p = N := by
      rcases hNp.eq_one_or_self_of_dvd p hpN with h1 | h2'
      · rw [h1] at hp
        exact absurd hp Nat.not_prime_one
      · exact h2'
    have hmpos : 0 < m := by omega
    have hNm : N ≤ m := by
      have := Nat.le_of_dvd hmpos hpm
      omega
    have hlow : m ≤ N := by
      rw [hN]
      have h1 := le_T (m - 1)
      omega
    have hNeq : N = m := by omega
    -- m ≤ 2: T(m−1) = m−k with k ≥ 1 forces T(m−1) ≤ m−1, while for m ≥ 3
    -- the recurrence T(m−1) = T(m−2) + (m−1) exceeds it.
    have hm2 : m ≤ 2 := by
      rcases Nat.lt_or_ge m 3 with h | h
      · omega
      · have hs := T_succ (m - 2)
        have e : m - 2 + 1 = m - 1 := by omega
        rw [e] at hs
        have hT1 : 1 ≤ T (m - 2) := by
          have h2 : T 1 ≤ T (m - 2) := T_mono (by omega)
          have h3 : T 1 = 1 := rfl
          omega
        omega
    -- m ≤ 2 with N = m prime and p = N ≠ 2.
    have hm_cases : m = 1 ∨ m = 2 := by omega
    rcases hm_cases with rfl | rfl
    · rw [hNeq] at hNp
      norm_num at hNp
    · rw [hNeq] at hpeq
      rw [hpeq] at hp2
      exact hp2 rfl
  -- Main case split on the gcd.
  by_cases hg1 : Nat.gcd k m = 1
  · exact Or.inl hg1
  · right
    have hg2 : 2 ≤ Nat.gcd k m := by
      have hpos : 0 < Nat.gcd k m := Nat.gcd_pos_of_pos_left _ (by omega : 0 < k)
      omega
    have hge : 2 ∣ Nat.gcd k m := by
      have hmf := Nat.minFac_dvd (Nat.gcd k m)
      have hmf2 : (Nat.gcd k m).minFac = 2 :=
        key _ (Nat.minFac_prime (by omega : Nat.gcd k m ≠ 1)) hmf
      rw [← hmf2]
      exact hmf
    have hk2 : 2 ∣ k := hge.trans (Nat.gcd_dvd_left k m)
    have hm2d : 2 ∣ m := hge.trans (Nat.gcd_dvd_right k m)
    -- m ≡ 2 (mod 4): 4 ∣ m would make T(m−1) even and k even, so N even > 2.
    have hm4 : m % 4 = 2 := by
      have h42 : m % 4 = 0 ∨ m % 4 = 2 := by
        have he : m % 2 = 0 := Nat.dvd_iff_mod_eq_zero.1 hm2d
        omega
      rcases h42 with h0 | h2'
      · exfalso
        have hm4e : Even (m / 2) := by
          have e := Nat.div_add_mod m 4
          refine ⟨m / 4, by omega⟩
        have hTmeven : Even (T (m - 1)) := by
          have hTe := T_pred_of_even (even_iff_two_dvd.2 hm2d)
          rw [hTe]
          rcases hm4e with ⟨s, hs⟩
          refine ⟨(m - 1) * s, ?_⟩
          rw [hs]
          ring
        have hk2e : Even k := even_iff_two_dvd.2 hk2
        have hNe : Even N := by rw [hN]; exact Even.add hTmeven hk2e
        have hN2' : N = 2 := (hNp.even_iff).1 hNe
        have hT6 : T 3 ≤ T (m - 1) := T_mono (by omega)
        have hT3 : T 3 = 6 := rfl
        omega
      · exact h2'
    -- gcd = 2: the gcd divides m = 4t+2, so gcd/2 divides the odd number
    -- 2t+1; any prime divisor of gcd/2 divides the gcd, hence is 2 — but
    -- gcd/2 is odd, so it has no prime divisor and equals 1.
    refine ⟨?_, hm4⟩
    obtain ⟨t, ht⟩ : ∃ t, m = 4 * t + 2 := ⟨m / 4, by
      have e := Nat.div_add_mod m 4
      omega⟩
    have hgm : Nat.gcd k m ∣ m := Nat.gcd_dvd_right k m
    obtain ⟨c, hc⟩ := hgm
    have hg2e : 2 * (Nat.gcd k m / 2) = Nat.gcd k m :=
      Nat.two_mul_div_two_of_even (even_iff_two_dvd.2 hge)
    have hu : m / 2 = Nat.gcd k m / 2 * c := by
      apply Nat.mul_left_cancel (n := 2) (by norm_num : 0 < 2)
      have hm2e : 2 * (m / 2) = m := Nat.two_mul_div_two_of_even (even_iff_two_dvd.2 hm2d)
      rw [hm2e, ← mul_assoc, hg2e]
      exact hc
    have hodd_u : Odd (m / 2) := ⟨t, by omega⟩
    rw [hu] at hodd_u
    have hgodd : Odd (Nat.gcd k m / 2) := (Nat.odd_mul.1 hodd_u).1
    have hg1' : Nat.gcd k m / 2 = 1 := by
      apply eq_one_of_no_prime_dvd (by omega : Nat.gcd k m / 2 ≠ 0)
      intro p hp hpdvd
      have hpg : p ∣ Nat.gcd k m :=
        hpdvd.trans ⟨2, by omega⟩
      have hp2 := key p hp hpg
      rw [hp2] at hpdvd
      have hnotodd : ¬ Odd (Nat.gcd k m / 2) := by
        rintro ⟨r, hr⟩
        obtain ⟨s, hs⟩ := hpdvd
        omega
      exact hnotodd hgodd
    omega

/-- B5 — the m ≡ 2 (mod 4) seat-zero theorem.  On these laps (m ≥ 6) every
    prime sits on a parity-escape tick: gcd(k,m) = 2 exactly.  The coprime
    columns are prime-free — k odd while T(m−1) = (m−1)(m/2) is odd makes the
    value even.  (The B6 "2.00×" is the measured [E] density of this parity
    conditioning.) -/
theorem B5_seat_zero {N m k : ℕ} (hm : 6 ≤ m) (hmod : m % 4 = 2)
    (hk : 1 ≤ k) (hkm : k ≤ m) (hN : N = T (m - 1) + k) (hNp : N.Prime) :
    Nat.gcd k m = 2 := by
  rcases column_law hk hkm hN hNp with h1 | ⟨h2, _⟩
  · exfalso
    have hm2d : 2 ∣ m := by omega
    have hTu_odd : Odd (m / 2) := by
      have e := Nat.div_add_mod m 4
      refine ⟨m / 4, by omega⟩
    have hTm_odd : Odd (T (m - 1)) := by
      have hTe := T_pred_of_even (even_iff_two_dvd.2 hm2d)
      rw [hTe]
      exact (Nat.odd_mul).2 ⟨by
        have hm1 : Odd (m - 1) := ⟨(m - 2) / 2, by omega⟩
        exact hm1, hTu_odd⟩
    have hk_odd : Odd k := by
      by_contra hke
      have hke2 : 2 ∣ k := even_iff_two_dvd.1 (Nat.not_odd_iff_even.1 hke)
      have : 2 ∣ Nat.gcd k m := Nat.dvd_gcd hke2 hm2d
      omega
    have hNe : Even N := by rw [hN]; exact Odd.add_odd hTm_odd hk_odd
    have hN2' : N = 2 := (hNp.even_iff).1 hNe
    have hT15 : T 5 ≤ T (m - 1) := T_mono (by omega)
    have hT5 : T 5 = 15 := rfl
    omega
  · exact h2

end Wheel
