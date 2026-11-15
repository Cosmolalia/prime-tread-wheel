/-
  Prime Tread Wheel — §18.9 Exact-Integer Dual Certificate Identity [F].

  This is the pure algebra behind `lab/phaseb_2026-10-19/verify_dual.py`
  (and the CBB engine's leaf certificates): for ANY free-ring residue
  structure, ANY non-negative integer tick weights `u_k`, ANY integer scale
  D > 0, and EVERY valid integer phase cover, the exact lower-bound
  inequality holds.  The large search trees stay in Python; this file
  certifies that the identity those trees rely on is sound, with no solver
  and no floating point anywhere.

  Abstraction: ticks are a finite type `κ`, free rings a finite type `ι`.
  Ring `p` reads each tick `k` in a residue `r p k : ZMod (n p)` (in the
  wheel, `n p = p` and `r p k = (T + k) mod p`).  A cover assigns each ring
  a phase `c p`; `y p ∈ {0,1}` is its rotation indicator, linked to `c p`.
  Validity: every positively weighted tick is covered by some free ring.

  The statement matches WHITEPAPER §18.9 verbatim:
    D·|{rotated rings}| ≥ D·|{fixed rotated rings}| + Σ_k (1−f(k))·u_k
                           − Σ_p max(0, max_{c≠0} W_p(c) − W_p(0) − D).
-/

import Mathlib

namespace Wheel

variable {ι κ : Type*} [Fintype ι] [Fintype κ]
variable (n : ι → ℕ) [∀ p, NeZero (n p)]

/-- In `ZMod k` with `2 ≤ k`, the element `1` is nonzero. -/
lemma zmod_one_ne_zero (k : ℕ) (hk : 2 ≤ k) : (1 : ZMod k) ≠ 0 := by
  intro h
  rw [← Int.cast_one] at h
  have hd := (ZMod.intCast_zmod_eq_zero_iff_dvd (1 : ℤ) k).mp h
  have : (k : ℤ) ≤ 1 := Int.le_of_dvd (by norm_num) hd
  omega

/-- Residue-class load: total weight of ticks landing in class `c` of ring `p`.
    In the wheel this is `W_p(c) = Σ_{k : (T+k) ≡ c (mod p)} u_k`. -/
def dualW (u : κ → ℤ) (r : ∀ p, κ → ZMod (n p)) (p : ι) (c : ZMod (n p)) : ℤ :=
  ∑ k, u k * (if r p k = c then 1 else 0)

/-- The nonzero residue classes of a ring with `2 ≤ n p` are nonempty
    (witness the class of `1`). -/
lemma dualM_nonempty (u : κ → ℤ) (r : ∀ p, κ → ZMod (n p)) (p : ι) (hn : 2 ≤ n p) :
    ((Finset.univ : Finset (ZMod (n p))).filter (fun c => c ≠ 0)).Nonempty := by
  refine ⟨(1 : ZMod (n p)), ?_⟩
  exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, zmod_one_ne_zero (n p) hn⟩

/-- Peak load over the NONZERO residue classes of ring `p`
    (`max_{1 ≤ c < p} W_p(c)` in the paper).  Requires `2 ≤ n p` so that the
    nonzero classes are nonempty (every wheel ring is prime, hence ≥ 2). -/
noncomputable def dualM (u : κ → ℤ) (r : ∀ p, κ → ZMod (n p)) (p : ι)
    (hn : 2 ≤ n p) : ℤ :=
  ((Finset.univ : Finset (ZMod (n p))).filter (fun c => c ≠ 0)).image (dualW n u r p)
    |>.max' ((dualM_nonempty n u r p hn).image (dualW n u r p))

/-- Any nonzero-class load is at most the peak `dualM`. -/
lemma dualM_spec (u : κ → ℤ) (r : ∀ p, κ → ZMod (n p))
    {p : ι} (hn : 2 ≤ n p) (c : ZMod (n p)) (hc : c ≠ 0) :
    dualW n u r p c ≤ dualM n u r p hn := by
  unfold dualM
  apply Finset.le_max'
  refine Finset.mem_image.mpr ⟨c, ?_, rfl⟩
  exact Finset.mem_filter.mpr ⟨Finset.mem_univ c, hc⟩

/-- Per-ring exact integer inequality (the engine of the identity):
    for binary `y_p ∈ {0,1}` and integer scale `D > 0`,
    `(W_p(c_p) − W_p(0))·y_p ≤ D·y_p + max(0, M_p − W_p(0) − D)`,
    where `M_p = max_{c≠0} W_p(c)`. -/
lemma dual_per_ring (u : κ → ℤ) (r : ∀ p, κ → ZMod (n p))
    {p : ι} (hn : 2 ≤ n p) (D : ℤ) (hD : 0 < D) (c : ∀ p, ZMod (n p)) (y : ι → ℤ)
    (hl : ∀ p, (y p = 0 ∧ c p = 0) ∨ (y p = 1 ∧ c p ≠ 0)) :
    (dualW n u r p (c p) - dualW n u r p 0) * y p
      ≤ D * y p + max 0 (dualM n u r p hn - dualW n u r p 0 - D) := by
  rcases hl p with ⟨hy, -⟩ | ⟨hy, hne⟩
  · rw [hy]
    simp only [mul_zero, zero_add]
    exact le_max_left 0 (dualM n u r p hn - dualW n u r p 0 - D)
  · rw [hy]
    simp only [mul_one]
    have hW := dualM_spec n u r hn (c p) hne
    by_cases h : dualM n u r p hn - dualW n u r p 0 - D ≤ 0
    · rw [max_eq_left h]; omega
    · rw [max_eq_right (le_of_not_ge h)]; omega

/-- Number of free rings whose zero class catches tick `k`
    (`f_free(k)` in the paper). -/
def dualF (r : ∀ p, κ → ZMod (n p)) (k : κ) : ℕ :=
  (Finset.univ.filter (fun p => r p k = 0)).card

/-- TotalNum of the paper (numerator of the certified lower bound):
    `D·F + Σ_k (1−f(k))·u_k − Σ_p max(0, M_p − W_p(0) − D)`
    with `F` the fixed-ring rotation count. -/
noncomputable def dualTotalNum (u : κ → ℤ) (r : ∀ p, κ → ZMod (n p))
    (hn : ∀ p, 2 ≤ n p) (D : ℤ) (F : ℤ) : ℤ :=
  D * F + ∑ k, (1 - (dualF n r k : ℤ)) * u k
    - ∑ p, max 0 (dualM n u r p (hn p) - dualW n u r p 0 - D)

/-- **[F] Exact-Integer Dual Certificate Identity (WHITEPAPER §18.9).**
    For any free-ring residue structure, any non-negative integer tick
    weights, any integer scale `D > 0`, and every valid integer phase cover
    (every positively weighted tick is covered by some free ring; `y p` is
    the rotation indicator of phase `c p`):
    `D·(F + Σ_p y_p) ≥ TotalNum`.  Python's `(TotalNum + D - 1)//D` of
    `verify_dual.py` is `⌈TotalNum/D⌉ ≤ F + Σ_p y_p`. -/
theorem dual_certificate_identity (hn : ∀ p, 2 ≤ n p)
    (r : ∀ p, κ → ZMod (n p)) (u : κ → ℤ) (hu : ∀ k, 0 ≤ u k)
    (D : ℤ) (hD : 0 < D) (c : ∀ p, ZMod (n p)) (y : ι → ℤ)
    (hl : ∀ p, (y p = 0 ∧ c p = 0) ∨ (y p = 1 ∧ c p ≠ 0))
    (hcover : ∀ k, 0 < u k → ∃ p, c p = r p k) (F : ℤ) :
    D * (F + ∑ p, y p) ≥ dualTotalNum n u r hn D F := by
  -- Step 1 (coverage): Σ_k u_k ≤ Σ_k u_k·(#rings covering k) = Σ_p W_p(c_p).
  have h1 : ∑ k, u k ≤ ∑ p, dualW n u r p (c p) := by
    calc ∑ k, u k
        ≤ ∑ k, u k * ((Finset.univ.filter (fun p => c p = r p k)).card : ℤ) := by
          apply Finset.sum_le_sum
          intro k _
          rcases lt_or_ge 0 (u k) with huk | huk
          · obtain ⟨p, hpe⟩ := hcover k huk
            have hcard : 1 ≤ (Finset.univ.filter (fun p => c p = r p k)).card :=
              Finset.card_pos.mpr ⟨p, Finset.mem_filter.mpr ⟨Finset.mem_univ p, hpe⟩⟩
            calc (u k : ℤ) = u k * 1 := (mul_one _).symm
              _ ≤ u k * (Finset.univ.filter (fun p => c p = r p k)).card := by
                  apply mul_le_mul_of_nonneg_left _ (hu k)
                  exact_mod_cast hcard
          · have huk0 : u k = 0 := by linarith [hu k]
            rw [huk0]; simp
      _ = ∑ p, dualW n u r p (c p) := by
          simp only [dualW, Finset.card_filter, Nat.cast_sum, Finset.mul_sum]
          rw [Finset.sum_comm]
          apply Finset.sum_congr rfl
          intro p _
          apply Finset.sum_congr rfl
          intro k _
          by_cases h : c p = r p k
          · simp only [h, eq_self_iff_true, if_true, Nat.cast_one, mul_one]
          · have h2 : ¬(r p k = c p) := fun hh => h hh.symm
            simp only [h, h2, if_false, Nat.cast_zero, mul_zero, zero_mul]
  -- Step 2 (split): Σ_p W_p(c_p) = Σ_p (W_p(0) + (W_p(c_p) − W_p(0))·y_p).
  have h2 : ∑ p, dualW n u r p (c p)
      = ∑ p, (dualW n u r p 0 + (dualW n u r p (c p) - dualW n u r p 0) * y p) := by
    apply Finset.sum_congr rfl
    intro p _
    rcases hl p with ⟨hy, h0⟩ | ⟨hy, -⟩
    · rw [hy, h0]; simp
    · rw [hy]; simp
  -- Step 3 (per-ring bound on the rotation-charged part).
  have h3 : ∑ p, (dualW n u r p 0 + (dualW n u r p (c p) - dualW n u r p 0) * y p)
      ≤ ∑ p, (dualW n u r p 0 + (D * y p
          + max 0 (dualM n u r p (hn p) - dualW n u r p 0 - D))) := by
    apply Finset.sum_le_sum
    intro p _
    have hr := dual_per_ring n u r (hn p) D hD c y hl
    omega
  -- Step 4 (swap): Σ_p W_p(0) = Σ_k f(k)·u_k.
  have h4 : ∑ p, dualW n u r p 0 = ∑ k, (dualF n r k : ℤ) * u k := by
    simp only [dualW, dualF, Finset.card_filter, Nat.cast_sum, Finset.sum_mul]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro k _
    apply Finset.sum_congr rfl
    intro p _
    by_cases h : r p k = 0
    · simp only [h, if_true, Nat.cast_one, mul_one, one_mul]
    · simp only [h, if_false, Nat.cast_zero, mul_zero, zero_mul]
  -- Step 5: per-tick aggregation of (1 − f(k))·u_k.
  have h5 : ∑ k, u k - ∑ k, (dualF n r k : ℤ) * u k
      = ∑ k, (1 - (dualF n r k : ℤ)) * u k := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro k _
    ring
  -- Step 6: distribute the per-ring bound.
  have h6 : ∑ p, (dualW n u r p 0 + (D * y p
        + max 0 (dualM n u r p (hn p) - dualW n u r p 0 - D)))
      = (∑ p, dualW n u r p 0) + D * (∑ p, y p)
        + ∑ p, max 0 (dualM n u r p (hn p) - dualW n u r p 0 - D) := by
    rw [Finset.sum_add_distrib, Finset.sum_add_distrib, Finset.mul_sum, add_assoc]
  -- Combine (omega chains the sum atoms through h4, h5, h6).
  rw [dualTotalNum, mul_add]
  have hb := h1.trans (h2.le.trans h3)
  omega

/-- Solver-form corollary: Python's `(TotalNum + D - 1)//D` (exact ceiling
    division, valid also for negative TotalNum) is a certified lower bound
    on the rotation count `F + Σ_p y_p`. -/
theorem dual_certificate_lb_floor (hn : ∀ p, 2 ≤ n p)
    (r : ∀ p, κ → ZMod (n p)) (u : κ → ℤ) (hu : ∀ k, 0 ≤ u k)
    (D : ℤ) (hD : 0 < D) (c : ∀ p, ZMod (n p)) (y : ι → ℤ)
    (hl : ∀ p, (y p = 0 ∧ c p = 0) ∨ (y p = 1 ∧ c p ≠ 0))
    (hcover : ∀ k, 0 < u k → ∃ p, c p = r p k) (F : ℤ) :
    (dualTotalNum n u r hn D F + D - 1) / D ≤ F + ∑ p, y p := by
  have hid := dual_certificate_identity n hn r u hu D hD c y hl hcover F
  rw [ge_iff_le, mul_comm] at hid
  rw [Int.ediv_le_iff_le_mul hD]
  omega

/-- Ceil-form corollary over ℚ: `⌈TotalNum / D⌉ ≤ F + Σ_p y_p`. -/
theorem dual_certificate_lb_ceil (hn : ∀ p, 2 ≤ n p)
    (r : ∀ p, κ → ZMod (n p)) (u : κ → ℤ) (hu : ∀ k, 0 ≤ u k)
    (D : ℤ) (hD : 0 < D) (c : ∀ p, ZMod (n p)) (y : ι → ℤ)
    (hl : ∀ p, (y p = 0 ∧ c p = 0) ∨ (y p = 1 ∧ c p ≠ 0))
    (hcover : ∀ k, 0 < u k → ∃ p, c p = r p k) (F : ℤ) :
    ⌈(dualTotalNum n u r hn D F : ℚ) / D⌉ ≤ F + ∑ p, y p := by
  apply Int.ceil_le.mpr
  have hDq : (0 : ℚ) < D := by exact_mod_cast hD
  rw [div_le_iff₀ hDq]
  have h := dual_certificate_identity n hn r u hu D hD c y hl hcover F
  rw [ge_iff_le, mul_comm] at h
  exact_mod_cast h

end Wheel
