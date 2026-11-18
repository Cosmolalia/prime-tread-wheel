/-
  Prime Tread Wheel — the exact parabolic multiplicity theorem [F]
  (WHITEPAPER §17.7, INSIGHTS Addendum 42).

  On an odd prime p, `8·T(m−1) ≡ (2m−1)² − 1 (mod p)`, so a constellation
  `N + D` with `N = T(m−1) + k` meets the residue class of `d ∈ D` at `p`
  exactly when `(2m−1)² ≡ 1 − 8(k+d)`. The squaring fibers at distinct
  right-hand sides are disjoint, and each carries `1 + χ(c)` points
  (1 at c = 0, 2 at nonzero squares, 0 at non-squares), so the number of
  killed m-phases is an exact finite union — no density heuristic:

      S_{p,D}(k) = p − Σ_{distinct c ∈ 1−8(k+D)} (1 + χ(c)).

  Kernel consequences proved below:
    `sqr_fiber_card`         — the fiber count 1 + χ(c), odd characteristic;
    `sqr_fiber_affine_ncard` — the affine change of variables m ↦ 2m−1
                               transports every fiber cardinality;
    `surviving_phases_eq`    — the general Legendre-union phase-count law;
    `twin_phase_count_mod3`  — twins D = {0,2}, p = 3: exact (0, 1, 2)
                               split across k ≡ (0, 1, 2) mod 3;
    `triple_phase_count_mod5`— triple D = {0,2,8}, p = 5: exact
                               (2, 3, 0, 3, 2) split across k mod 5.
  The census confirmations (0 / 25,339 / 50,220 twins; shares
  0.1943 / 0.3016 / 0 / 0.3007 / 0.2034) are the Python probe's [E];
  `lab/probes/parabolic_obstruction_2026-11-17.out`.

  `twin_int_kill_mod3` — integer-coordinate bridge (INSIGHTS Addendum 44):
  the 3 ∣ k row: for every layer m, a twin tick (T(m−1)+k, T(m−1)+k+2) with
  k ≡ 0 (mod 3) loses at least one member to 3, period-3 in m.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- **[F]** Surviving `m`-phases modulo `p` at column `k` for offset pattern
    `D`: the `m ∈ ZMod p` for which `T(m−1) + k + d` survives at `p` for all
    `d ∈ D`, written via `8·T(m−1) ≡ (2m−1)² − 1` as `(2m−1)² ≢ 1 − 8(k+d)`. -/
def survivingPhases (p : ℕ) [NeZero p] (D : Finset (ZMod p)) (k : ZMod p) : ℕ :=
  (Finset.univ.filter fun m : ZMod p => ∀ d ∈ D, (2 * m - 1) ^ 2 ≠ 1 - 8 * (k + d)).card

/-- Bridge: a `Finset.filter` over the full finite type counts the same as the
    corresponding set's `ncard` (subtype cardinality in two steps). -/
theorem Finset.card_filter_univ_eq_ncard {α : Type*} [Fintype α] (P : α → Prop)
    [DecidablePred P] :
    (Finset.univ.filter P).card = {x : α | P x}.ncard := by
  rw [← Fintype.card_subtype, ← Nat.card_eq_fintype_card, ← Nat.card_coe_set_eq]
  rfl

/-- **[F] fiber cardinalities of the squaring map on a field of odd
    characteristic.** For `c` in a finite field `F` with `ringChar F ≠ 2`:
    `#{x | x² = c}` is `1` at `c = 0`, `2` at nonzero squares, `0` at
    non-squares — i.e. `1 + χ(c)` with `χ` the quadratic character. -/
theorem sqr_fiber_card {F : Type*} [Field F] [Fintype F] [DecidableEq F]
    (hF : ringChar F ≠ 2) (c : F) :
    {x : F | x ^ 2 = c}.ncard =
      if c = 0 then 1 else if IsSquare c then 2 else 0 := by
  by_cases hc : c = 0
  · subst hc
    have hset : {x : F | x ^ 2 = (0 : F)} = {0} := by
      ext x
      simp
    simp only [hset, Set.ncard_singleton, eq_self_iff_true, ite_true]
  · by_cases hs : IsSquare c
    · obtain ⟨r, hr⟩ := hs
      have hr0 : r ≠ 0 := by
        rintro rfl
        rw [mul_zero] at hr
        exact hc hr
      have h2 : (2 : F) ≠ 0 := by
        intro h
        have hdvd : ringChar F ∣ 2 :=
          (CharP.cast_eq_zero_iff F (ringChar F) 2).mp (by simpa using h)
        rcases (Nat.dvd_prime Nat.prime_two).mp hdvd with h1 | h1
        · have h10 : (1 : F) = 0 := by
            have h' : ((1 : ℕ) : F) = 0 :=
              (CharP.cast_eq_zero_iff F (ringChar F) 1).mpr (by rw [h1])
            simpa using h'
          exact one_ne_zero h10
        · exact hF h1
      have hroot : ∀ x : F, x ^ 2 = c → x = r ∨ x = -r := fun x hx =>
        sq_eq_sq_iff_eq_or_eq_neg.mp (by rw [hx, pow_two]; exact hr)
      have hrne : r ≠ -r := by
        intro hrr
        have hsum : r + r = 0 := add_eq_zero_iff_eq_neg'.mpr hrr
        have h2r : (2 : F) * r = 0 := by rw [two_mul]; exact hsum
        rcases mul_eq_zero.mp h2r with h | h
        · exact (h2 h).elim
        · exact hr0 h
      have hset : {x : F | x ^ 2 = c} = {r, -r} := by
        ext x
        constructor
        · intro hx
          simp only [Set.mem_ofPred_eq] at hx
          rcases hroot x hx with e | e <;> simp [e]
        · intro hx
          simp only [Set.mem_insert_iff, Set.mem_singleton_iff, Set.mem_ofPred_eq] at hx
          rcases hx with e | e
          · subst x
            show r ^ 2 = c
            rw [pow_two]; exact hr.symm
          · subst x
            show (-r) ^ 2 = c
            rw [neg_pow_two, pow_two, hr]
      have hsc : IsSquare c := ⟨r, hr⟩
      simp only [hset, Set.ncard_pair hrne, hc, hsc, ite_false, ite_true]
    · have hset : {x : F | x ^ 2 = c} = ∅ := by
        ext x
        simp only [Set.mem_ofPred_eq, Set.mem_empty_iff_false, iff_false]
        intro hx
        exact hs ⟨x, by rw [← hx, pow_two]⟩
      simp only [hset, Set.ncard_empty, hc, hs, ite_false]

/-- **[F]** The affine change of variables `m ↦ 2m − 1` (a bijection since
    `2 ≠ 0`) transports every squaring-fiber cardinality unchanged. -/
theorem sqr_fiber_affine_ncard {F : Type*} [Field F] [Fintype F] (h2 : (2 : F) ≠ 0) (c : F) :
    {m : F | (2 * m - 1) ^ 2 = c}.ncard = {x : F | x ^ 2 = c}.ncard := by
  have himg : {m : F | (2 * m - 1) ^ 2 = c}
      = (fun x => (2 : F)⁻¹ * (x + 1)) '' {x : F | x ^ 2 = c} := by
    ext m
    constructor
    · intro hm
      refine ⟨2 * m - 1, hm, ?_⟩
      have h1 : 2 * m - 1 + 1 = 2 * m := by ring
      calc (2 : F)⁻¹ * (2 * m - 1 + 1) = (2 : F)⁻¹ * (2 * m) := by rw [h1]
        _ = ((2 : F)⁻¹ * 2) * m := by ring
        _ = (1 : F) * m := by rw [inv_mul_cancel₀ h2]
        _ = m := one_mul m
    · rintro ⟨x, hx, rfl⟩
      show (2 * ((2 : F)⁻¹ * (x + 1)) - 1) ^ 2 = c
      have he : 2 * ((2 : F)⁻¹ * (x + 1)) - 1 = x := by
        calc 2 * ((2 : F)⁻¹ * (x + 1)) - 1 = ((2 : F) * (2 : F)⁻¹) * (x + 1) - 1 := by ring
          _ = (1 : F) * (x + 1) - 1 := by rw [mul_inv_cancel₀ h2]
          _ = x := by rw [one_mul, add_sub_cancel_right]
      rw [he, hx]
  rw [himg, Set.ncard_image_of_injective]
  intro a b h
  exact add_left_injective 1 (mul_left_cancel₀ (inv_ne_zero h2) h)

open Classical in
/-- **[F] the exact parabolic multiplicity theorem (general Legendre union
    law).** For an odd prime `p`, offset pattern `D ⊆ ZMod p` and column `k`,
    the number of surviving m-phases is `p` minus the sum of `1 + χ(c)` over
    the *distinct* values `c ∈ 1 − 8(k+D)`; distinct fibers are disjoint. -/
theorem surviving_phases_eq {p : ℕ} [Fact p.Prime] (hp : p ≠ 2) (D : Finset (ZMod p))
    (k : ZMod p) :
    survivingPhases p D k = p - (D.image fun d => 1 - 8 * (k + d)).sum
      (fun c => if c = 0 then 1 else if IsSquare c then 2 else 0) := by
  classical
  haveI : NeZero p := ⟨(Fact.out : Nat.Prime p).pos.ne'⟩
  have hchar : ringChar (ZMod p) = p := ZMod.ringChar_zmod_n p
  have h2 : (2 : ZMod p) ≠ 0 := by
    intro h
    have h' : ((2 : ℕ) : ZMod p) = 0 := by simpa using h
    have hdvd : p ∣ 2 := (ZMod.natCast_eq_zero_iff 2 p).mp h'
    rcases (Nat.dvd_prime Nat.prime_two).mp hdvd with h1 | h1
    · exact (Fact.out : Nat.Prime p).one_lt.ne' h1
    · exact hp h1
  have hcompl : (Finset.univ.filter fun m : ZMod p =>
        ∀ d ∈ D, (2 * m - 1) ^ 2 ≠ 1 - 8 * (k + d))
      = Finset.univ \ D.biUnion
        (fun d => Finset.univ.filter fun m : ZMod p => (2 * m - 1) ^ 2 = 1 - 8 * (k + d)) := by
    ext m
    simp only [Finset.mem_filter, Finset.mem_univ, Finset.mem_sdiff, Finset.mem_biUnion, true_and]
    constructor
    · intro h ⟨d, hd, hdm⟩
      exact h d hd hdm
    · intro h d hd hdm
      exact h ⟨d, hd, hdm⟩
  rw [survivingPhases, hcompl, Finset.card_sdiff, Finset.inter_univ, Finset.card_univ,
    ZMod.card p]
  congr 1
  have himg : D.biUnion (fun d => Finset.univ.filter fun m : ZMod p =>
        (2 * m - 1) ^ 2 = 1 - 8 * (k + d))
      = (D.image fun d => 1 - 8 * (k + d)).biUnion
        (fun c => Finset.univ.filter fun m : ZMod p => (2 * m - 1) ^ 2 = c) := by
    ext m
    simp only [Finset.mem_biUnion, Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and]
    constructor
    · rintro ⟨d, hd, hdm⟩
      exact ⟨1 - 8 * (k + d), ⟨d, hd, rfl⟩, hdm⟩
    · rintro ⟨c, ⟨d, hd, rfl⟩, hcm⟩
      exact ⟨d, hd, hcm⟩
  rw [himg]
  have hdisj : Set.PairwiseDisjoint (↑(D.image fun d => 1 - 8 * (k + d)) : Set (ZMod p))
      (fun c => Finset.univ.filter fun m : ZMod p => (2 * m - 1) ^ 2 = c) := by
    intro c hc c' hc' hne
    apply Finset.disjoint_left.mpr
    rintro m hm hm'
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hm hm'
    exact hne (hm.symm.trans hm')
  rw [Finset.card_biUnion hdisj]
  refine Finset.sum_congr rfl ?_
  intro c hc
  have hchar2 : ringChar (ZMod p) ≠ 2 := by rw [hchar]; exact hp
  rw [Finset.card_filter_univ_eq_ncard, sqr_fiber_affine_ncard h2, sqr_fiber_card hchar2]

/-- **[F + E]** Twins `D = {0, 2}` at `p = 3`: the exact `(0, 1, 2)` split —
    surviving m-phases are exactly `0, 1, 2` for `k ≡ 0, 1, 2 (mod 3)`,
    matching the census `0 / 25,339 / 50,220`. Kernel-checked by `decide`. -/
theorem twin_phase_count_mod3 (k : ZMod 3) :
    survivingPhases 3 {0, 2} k = ZMod.val k := by
  revert k
  decide

/-- **[F + E]** Triple `D = {0, 2, 8}` at `p = 5`: the exact `(2, 3, 0, 3, 2)`
    split — `k ≡ 2 (mod 5)` is the unique killing residue (0/5 phases), the
    other classes carry `2, 3, 3, 2` of 5, matching the census shares
    `0.1943 / 0.3016 / 0 / 0.3007 / 0.2034`. Kernel-checked by `decide`. -/
theorem triple_phase_count_mod5 (k : ZMod 5) :
    survivingPhases 5 {0, 2, 8} k =
      if ZMod.val k = 0 then 2 else
      if ZMod.val k = 1 then 3 else
      if ZMod.val k = 2 then 0 else
      if ZMod.val k = 3 then 3 else 2 := by
  revert k
  decide

/-- Bridge helper [F]: the doubling identity `2 · T n = n(n+1)` scaled by 4. -/
private theorem eight_mul_T (n : ℕ) : 8 * T n = 4 * (n * (n + 1)) := by
  calc 8 * T n = 4 * (2 * T n) := by ring
    _ = 4 * (n * (n + 1)) := by rw [two_mul_T]

/-- **[F] integer bridge** (Argon, board #832 → #833): the `k ≡ 0 (mod 3)` row of
    the twin table on the wheel's integer coordinate `N = T(m−1) + k`. For every
    layer `m` and tick `k` with `3 ∣ k`, at least one member of the twin pair
    `(T(m−1)+k, T(m−1)+k+2)` is divisible by 3. The mechanism is period-3 in
    `m`: `m ≡ 0, 1 (mod 3)` gives `3 ∣ T(m−1)` (left member falls),
    `m ≡ 2 (mod 3)` gives `T(m−1) ≡ 1 (mod 3)` (right member falls) — the
    integer-coordinate shadow of `twin_phase_count_mod3`'s 0-row, with zero
    surviving twin ticks at `k ≡ 0 (mod 3)` and no density heuristic. -/
theorem twin_int_kill_mod3 (m k : ℕ) (hk : 3 ∣ k) :
    3 ∣ (T (m - 1) + k) ∨ 3 ∣ (T (m - 1) + k + 2) := by
  cases m with
  | zero =>
    simp only [Nat.zero_sub, T_zero, zero_add]
    exact Or.inl hk
  | succ r =>
    change 3 ∣ (T r + k) ∨ 3 ∣ (T r + k + 2)
    rw [← CharP.cast_eq_zero_iff (ZMod 3) 3 (T r + k),
      ← CharP.cast_eq_zero_iff (ZMod 3) 3 (T r + k + 2)]
    push_cast
    have hk0 : (k : ZMod 3) = 0 := (CharP.cast_eq_zero_iff (ZMod 3) 3 k).mpr hk
    rw [hk0, add_zero]
    have h8 : 8 * (T r : ZMod 3) = 4 * ((r : ZMod 3) * ((r : ZMod 3) + 1)) := by
      have key : ((8 * T r : ℕ) : ZMod 3) = 4 * ((r : ZMod 3) * ((r : ZMod 3) + 1)) := by
        rw [eight_mul_T r]
        push_cast
        ring
      rw [← key]
      norm_cast
    have h16 : (8 : ZMod 3) * 2 = 1 := by decide
    have hy : (T r : ZMod 3) = 2 * (4 * ((r : ZMod 3) * ((r : ZMod 3) + 1))) := by
      calc (T r : ZMod 3) = 1 * (T r : ZMod 3) := (one_mul _).symm
        _ = (8 * 2) * (T r : ZMod 3) := by rw [← h16]
        _ = 2 * (8 * (T r : ZMod 3)) := by ring
        _ = 2 * (4 * ((r : ZMod 3) * ((r : ZMod 3) + 1))) := by rw [h8]
    rw [hy]
    have hc : ∀ c : ZMod 3, 2 * (4 * (c * (c + 1))) = 0 ∨ 2 * (4 * (c * (c + 1))) + 2 = 0 := by
      decide
    exact hc _

end Wheel
