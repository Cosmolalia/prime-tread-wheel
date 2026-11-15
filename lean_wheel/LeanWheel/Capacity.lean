/-
  Theorem III part 2 — the covering-capacity inequalities (WHITEPAPER §19.3,
  concluding sentence).

  A rotated ring (p, c) catches the ticks of ONE residue class of k mod p
  (in tick coordinates; rotating the gear shifts the class by the stagger
  field o_p m — a bijection of ZMod p — so the counting is shift-invariant).
  Each class has at most ⌈m/p⌉ = (m+p−1)/p ticks of the layer.

  Kernel content: if the stripes of a rotated support S ⊆ rings B cover the
  work set W(S) = {k ∈ [1,m] : F(k) ⊆ S} — the defining coverage obligation
  of a valid phase vector — then
      |W(S)| ≤ Σ_p |stripe(p, c_p)| ≤ Σ_p ⌈m/p⌉,
  and the same bound holds for any downward-closed sub-family W(T), T ⊆ S,
  in particular the native uncovered stratum C_∅ = U_0.
-/

import Mathlib
import LeanWheel.Defs
import LeanWheel.Conservation

namespace Wheel

/-- The rotated stripe of ring p at phase c, in tick coordinates: the ticks
    of the layer congruent to c mod p.  (In value coordinates the rotated
    ring covers {(T+k) % p = c}; transport along k ↦ T+k is the bijection
    r ↦ r − T(m−1) of the residue classes, so the cardinalities agree.) -/
def stripe (m p c : ℕ) : Finset ℕ :=
  (Finset.Icc 1 m).filter (fun k ↦ k % p = c % p)

/-- Membership in a stripe. -/
theorem mem_stripe (m p c k : ℕ) :
    k ∈ stripe m p c ↔ (1 ≤ k ∧ k ≤ m ∧ k % p = c % p) := by
  simp only [stripe, Finset.mem_filter, Finset.mem_Icc, and_assoc]

/-- k ↦ (k − r)/p is injective on a fixed residue class (r = c % p < p). -/
private theorem injOn_stripe (m p c : ℕ) (hp' : 0 < p) :
    Set.InjOn (fun k ↦ (k - c % p) / p) ↑(stripe m p c) := by
  intro k1 hk1 k2 hk2 h12
  have h1 := (mem_stripe m p c k1).1 hk1
  have h2 := (mem_stripe m p c k2).1 hk2
  have hd1 : k1 = p * (k1 / p) + c % p := by
    have h := (Nat.div_add_mod k1 p).symm
    rw [h1.2.2] at h
    exact h
  have hd2 : k2 = p * (k2 / p) + c % p := by
    have h := (Nat.div_add_mod k2 p).symm
    rw [h2.2.2] at h
    exact h
  have e1 : k1 - c % p = p * (k1 / p) := by
    rw [Nat.sub_eq_iff_eq_add' (by have := Nat.mod_le k1 p; omega), add_comm]
    exact hd1
  have e2 : k2 - c % p = p * (k2 / p) := by
    rw [Nat.sub_eq_iff_eq_add' (by have := Nat.mod_le k2 p; omega), add_comm]
    exact hd2
  have h12'' : (k1 - c % p) / p = (k2 - c % p) / p := h12
  rw [e1, e2, Nat.mul_div_right _ hp', Nat.mul_div_right _ hp'] at h12''
  rw [hd1, hd2, h12'']

/-- Per-class capacity: every residue class of ring p carries at most
    ⌈m/p⌉ = (m+p−1)/p ticks of the layer. -/
theorem stripe_card_le (m p c : ℕ) (hp : 1 ≤ p) :
    (stripe m p c).card ≤ (m + p - 1) / p := by
  have hp' : 0 < p := hp
  rcases Nat.eq_zero_or_pos m with rfl | hm
  · refine (Finset.card_filter_le _ _).trans ?_
    change (Finset.Icc 1 0).card ≤ (0 + p - 1) / p
    rw [Nat.card_Icc]
    exact Nat.zero_le _
  · have hN : (m + p - 1) / p = (m - 1) / p + 1 := by
      have e : m + p - 1 = (m - 1) + p * 1 := by omega
      rw [e, Nat.add_mul_div_left (m - 1) 1 hp']
    rcases Nat.eq_zero_or_pos (c % p) with h0 | hpos
    · -- multiples of p: j = k/p ranges in [1, ⌈m/p⌉]
      calc (stripe m p c).card ≤ (Finset.Icc 1 ((m + p - 1) / p)).card :=
            Finset.card_le_card_of_injOn (f := fun k ↦ (k - c % p) / p)
              (by
                intro k hk
                rw [h0]
                change k / p ∈ Finset.Icc 1 ((m + p - 1) / p)
                have h1 := (mem_stripe m p c k).1 hk
                have hkp : p ≤ k := Nat.le_of_dvd h1.1
                  (Nat.dvd_of_mod_eq_zero (by rw [h1.2.2, h0]))
                exact Finset.mem_Icc.2 ⟨Nat.div_pos hkp hp',
                  (Nat.div_le_div_right h1.2.1).trans
                    (Nat.div_le_div_right (by omega))⟩)
              (injOn_stripe m p c hp')
        _ = (m + p - 1) / p := by simp
    · -- nonzero residue r ≥ 1: j = (k − r)/p ranges ≤ (m−1)/p < ⌈m/p⌉
      calc (stripe m p c).card ≤ (Finset.range ((m + p - 1) / p)).card :=
            Finset.card_le_card_of_injOn (f := fun k ↦ (k - c % p) / p)
              (by
                intro k hk
                change (k - c % p) / p ∈ Finset.range ((m + p - 1) / p)
                have h1 := (mem_stripe m p c k).1 hk
                have ha : (k - c % p) / p ≤ (m - c % p) / p :=
                  Nat.div_le_div_right (by omega)
                have hb : (m - c % p) / p ≤ (m - 1) / p :=
                  Nat.div_le_div_right (by omega)
                exact Finset.mem_range.2 (by rw [hN]; omega))
              (injOn_stripe m p c hp')
        _ = (m + p - 1) / p := Finset.card_range _

/-- §19.3 — the capacity inequality.  If the stripes of the rotated support S
    cover W(S) (the coverage obligation), then |W(S)| is at most the sum of
    the chosen stripe sizes. -/
theorem capacity_inequality (m B : ℕ) (S : Finset ℕ) (_hS : S ⊆ rings B)
    (phase : ∀ p ∈ S, ℕ)
    (hcover : ∀ k, 1 ≤ k → k ≤ m → F m B k ⊆ S →
        ∃ p, ∃ hp : p ∈ S, k % p = phase p hp % p) :
    ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S)).card ≤
      ∑ x ∈ S.attach, (stripe m x.1 (phase x.1 x.2)).card := by
  have hsub : (Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S) ⊆
      S.attach.biUnion (fun x ↦ stripe m x.1 (phase x.1 x.2)) := by
    intro k hk
    have h1 := Finset.mem_filter.1 hk
    have h1m := Finset.mem_Icc.1 h1.1
    obtain ⟨p, hp, hph⟩ := hcover k h1m.1 h1m.2 h1.2
    exact Finset.mem_biUnion.2 ⟨⟨p, hp⟩, Finset.mem_attach _ _,
      (mem_stripe _ _ _ _).2 ⟨h1m.1, h1m.2, hph⟩⟩
  calc ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S)).card
      ≤ (S.attach.biUnion (fun x ↦ stripe m x.1 (phase x.1 x.2))).card :=
        Finset.card_le_card hsub
    _ ≤ ∑ x ∈ S.attach, (stripe m x.1 (phase x.1 x.2)).card :=
        Finset.card_biUnion_le

/-- The capacity-number form: summing the per-class maxima ⌈m/p⌉ over the
    support bounds every downward-closed sub-family W(T), T ⊆ S. -/
theorem capacity_inequality_family (m B : ℕ) (S T : Finset ℕ) (hTS : T ⊆ S)
    (hS : S ⊆ rings B) (phase : ∀ p ∈ S, ℕ)
    (hcover : ∀ k, 1 ≤ k → k ≤ m → F m B k ⊆ S →
        ∃ p, ∃ hp : p ∈ S, k % p = phase p hp % p) :
    ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ T)).card ≤
      ∑ x ∈ S.attach, (m + x.1 - 1) / x.1 := by
  have h1 : ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ T)) ⊆
      (Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S) := by
    intro k hk
    have h := Finset.mem_filter.1 hk
    exact Finset.mem_filter.2 ⟨h.1, Finset.Subset.trans h.2 hTS⟩
  calc ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ T)).card
      ≤ ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S)).card := Finset.card_le_card h1
    _ ≤ ∑ x ∈ S.attach, (stripe m x.1 (phase x.1 x.2)).card :=
        capacity_inequality m B S hS phase hcover
    _ ≤ ∑ x ∈ S.attach, (m + x.1 - 1) / x.1 := by
        apply Finset.sum_le_sum
        intro x _
        have hp2 : 2 ≤ x.1 := ((Finset.mem_filter.1 (hS x.2)).2).two_le
        exact stripe_card_le m x.1 (phase x.1 x.2) (by omega)

/-- In particular the native uncovered stratum C_∅ = U_0 is bounded by the
    summed capacities of any rotated support. -/
theorem uncovered_capacity (m B : ℕ) (S : Finset ℕ) (hS : S ⊆ rings B)
    (phase : ∀ p ∈ S, ℕ)
    (hcover : ∀ k, 1 ≤ k → k ≤ m → F m B k ⊆ S →
        ∃ p, ∃ hp : p ∈ S, k % p = phase p hp % p) :
    (stratum m B ∅).card ≤ ∑ x ∈ S.attach, (m + x.1 - 1) / x.1 := by
  have h1 : stratum m B ∅ ⊆ (Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S) := by
    intro k hk
    have h2 := (mem_stratum m B k ∅).1 hk
    exact Finset.mem_filter.2 ⟨h2.1, by rw [h2.2]; exact Finset.empty_subset _⟩
  calc (stratum m B ∅).card
      ≤ ((Finset.Icc 1 m).filter (fun k ↦ F m B k ⊆ S)).card := Finset.card_le_card h1
    _ ≤ ∑ x ∈ S.attach, (m + x.1 - 1) / x.1 :=
        capacity_inequality_family m B S S (Finset.Subset.refl S) hS phase hcover

end Wheel
