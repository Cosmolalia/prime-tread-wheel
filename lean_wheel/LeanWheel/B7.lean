/-
  B7 — the mirror lift.

  Paper (§4, B7):  T(m−1) + T(m) = m², so the tick involution k ↔ m − k pairs values
  summing to exactly m²; eligibility is preserved exactly
  (gcd(k, m) = gcd(m − k, m)) and the map is a bijection on ticks.

  Scoping note: as a map on the LINEAR tick set {1..m}, k ↦ m − k is not closed
  (k = m ↦ 0); the involution is exact on the cyclic ticks (k ≡ 0 class included).
  We formalize the involution on `ZMod m` (a genuine self-inverse bijection, the
  seat palindrome) and the value pairing for the interior ticks 1 ≤ k ≤ m−1;
  the two endpoint values T(m) and T(m−1) are swapped by m² − v across layers
  (`mirror_endpoint`), which is what the circle identifications k ≡ m ≡ 0 say.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- The mirror identity: T(m−1) + T(m) = m² for all m ≥ 1. -/
theorem T_pred_add_T (m : ℕ) (hm : 1 ≤ m) : T (m - 1) + T m = m ^ 2 := by
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le hm
  rw [add_comm 1 r, Nat.add_sub_cancel, pow_two]
  have h1 := two_mul_T r
  have h2 := two_mul_T (r + 1)
  have e : 2 * (T r + T (r + 1)) = 2 * ((r + 1) * (r + 1)) := by
    rw [mul_add, h1, h2]
    ring
  exact Nat.eq_of_mul_eq_mul_left (by decide) e

/-- The value pairing: for interior ticks 1 ≤ k ≤ m−1 the mirror tick m − k
    carries the value m² − v.  (Here stated additively.) -/
theorem mirror_sum (m k : ℕ) (hk1 : 1 ≤ k) (hk2 : k < m) :
    T (m - 1) + k + (T (m - 1) + (m - k)) = m ^ 2 := by
  obtain ⟨r, rfl⟩ := Nat.exists_eq_add_of_le (by omega : 1 ≤ m)
  rw [add_comm 1 r, Nat.add_sub_cancel, pow_two]
  have h1 := two_mul_T r
  have e : T r + k + (T r + (r + 1 - k)) = 2 * T r + (r + 1) := by omega
  rw [e, h1]
  ring

/-- Endpoint exchange: the value pairing swaps the layer's last tick T(m) with
    the previous layer's last tick T(m−1). -/
theorem mirror_endpoint (m : ℕ) : m ^ 2 - T m = T (m - 1) := by
  rcases Nat.eq_zero_or_pos m with rfl | hm
  · rfl
  · have h := T_pred_add_T m hm
    omega

/-- Eligibility preservation: gcd(k, m) = gcd(m − k, m) for 1 ≤ k ≤ m
    (the gcd = 2 parity escape included, as no case distinction is made). -/
theorem mirror_gcd (m k : ℕ) (hk : k ≤ m) : Nat.gcd k m = Nat.gcd (m - k) m := by
  rw [Nat.gcd_comm k m, Nat.gcd_comm (m - k) m, Nat.gcd_self_sub_right hk]

/-- The mirror map on cyclic ticks: −k ≡ m − k  in ZMod m  (for k ≤ m). -/
theorem mirror_zmod (m k : ℕ) (hk : k ≤ m) :
    (-(k : ZMod m) : ZMod m) = ((m - k : ℕ) : ZMod m) := by
  have hm0 : ((m : ℕ) : ZMod m) = 0 := (ZMod.natCast_eq_zero_iff m m).2 (dvd_refl m)
  rw [Nat.cast_sub hk, hm0, zero_sub]

/-- The tick involution is a bijection: negation on ZMod m is a self-inverse
    equivalence (the seat palindrome, lifted to values). -/
def mirrorEquiv (m : ℕ) : ZMod m ≃ ZMod m := Equiv.neg _

theorem mirrorEquiv_involutive (m : ℕ) (x : ZMod m) :
    mirrorEquiv m (mirrorEquiv m x) = x := neg_neg x

/-- For odd m ≥ 3 no mirror prime pair can exist: v and m² − v have opposite
    parity and the even one is ≥ 4, hence composite. -/
theorem no_mirror_prime_pair_odd (m k : ℕ) (hm : Odd m) (h3 : 3 ≤ m)
    (hk1 : 1 ≤ k) (hk2 : k < m) :
    ¬ ((T (m - 1) + k).Prime ∧ (T (m - 1) + (m - k)).Prime) := by
  rintro ⟨hp1, hp2⟩
  have hsum := mirror_sum m k hk1 hk2
  have hoddm : Odd (m ^ 2) := by rw [pow_two]; exact hm.mul hm
  rw [← hsum] at hoddm
  rcases Nat.even_or_odd (T (m - 1) + k) with he1 | ho1
  · have hge : 4 ≤ T (m - 1) + k := by
      have h1 : T 2 ≤ T (m - 1) := T_mono (by omega)
      have h2 : T 2 = 3 := rfl
      omega
    have h2 : T (m - 1) + k = 2 := (Nat.Prime.even_iff hp1).1 he1
    omega
  · rcases Nat.even_or_odd (T (m - 1) + (m - k)) with he2 | ho2
    · have hge : 4 ≤ T (m - 1) + (m - k) := by
        have h1 : T 2 ≤ T (m - 1) := T_mono (by omega)
        have h2 : T 2 = 3 := rfl
        omega
      have h2 : T (m - 1) + (m - k) = 2 := (Nat.Prime.even_iff hp2).1 he2
      omega
    · have hev : Even (T (m - 1) + k + (T (m - 1) + (m - k))) := ho1.add_odd ho2
      exact (Nat.not_even_iff_odd.2 hoddm) hev

end Wheel
