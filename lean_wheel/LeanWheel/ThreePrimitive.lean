/-
  The Three-Primitive Theorem (WHITEPAPER §16.8) — the flagship certificate.

  Among discrete spirals Φ(m,k) = B(m) + k (1 ≤ k ≤ L(m)) with lap-start
  B : ℕ → ℤ and lap-length L : ℕ → ℤ, the primitives are

    P1  origin & contiguity :  B 1 = 0  and  B(m+1) − B m = L m   (all m : ℕ)
    P2  affine lap growth    :  L m = a·m + b for constants a, b
    P3  unit step            :  L(m+1) − L m = 1
    P4  odd-divisor seam lock:  for every odd m ≥ 1 and every q ≥ 1 with q ∣ m,
                                (q : ℤ) ∣ B m
    P5  lap palindrome       :  the polynomial extension of B satisfies
                                B̂(m) = B̂(1−m)

  Formalized here:
    • P3 ⇒ P2 (P2 is redundant);
    • from P1 ∧ P3, B m = TZ(m−1) + b·(m−1) for all m ≥ 1, with b = L 1 − 1
      (`formula_B`); the polynomial extension is taken to be
      B̂ x = TZ(x−1) + b·(x−1) (the unique quadratic agreeing with B on ℕ≥1);
    • (P1 ∧ P3 ∧ P4) → L 1 − 1 = 0 and B = T(·−1) on m ≥ 1
      (`three_primitive_P4`);
    • (P1 ∧ P3 ∧ P5) → the same (`three_primitive_P5`);
    • P4 ↔ P5 given P1 ∧ P3;
    • the independence witnesses (i), (ii), (iii) of the paper.

  SCOPE NOTE (see report): the conclusion is stated for m ≥ 1, matching the
  paper's domain ℤ_{≥1} — B 0 is not constrained by P1/P3 (P1 only ties B 0 to
  the free value L 0), so "∀ m, B m = T(m−1)" cannot hold at m = 0 in general.
  Also the paper's phrase "imposing P4 even at a single odd m > 1 forces b = 0"
  is COMPRESSED: one odd m gives only m ∣ b; the universal quantifier over odd m
  (or any unbounded family) is what forces b = 0.  The formalization uses the
  universal reading, which is the correct version of the claim.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- P1 — origin & contiguity.  Stated for all m : ℕ; the paper's §16.8 states
    the recurrence for m ≥ 1 only — the m = 0 conjunct is an inessential
    strengthening (see report). -/
def P1 (B L : ℕ → ℤ) : Prop := B 1 = 0 ∧ ∀ m, B (m + 1) - B m = L m

/-- P2 — affine lap growth. -/
def P2 (L : ℕ → ℤ) : Prop := ∃ a b, ∀ m, L m = a * m + b

/-- P3 — unit step. -/
def P3 (L : ℕ → ℤ) : Prop := ∀ m, L (m + 1) - L m = 1

/-- P4 — odd-divisor seam lock. -/
def P4 (B : ℕ → ℤ) : Prop :=
  ∀ m : ℕ, 1 ≤ m → Odd m → ∀ q : ℕ, 1 ≤ q → q ∣ m → (q : ℤ) ∣ B m

/-- The polynomial extension of B under P1 ∧ P3.  From P1 ∧ P3 one derives
    B m = TZ(m−1) + b·(m−1) with b = L 1 − 1 (`formula_B`), so the extension is
    x ↦ TZ(x−1) + b·(x−1).  (This is the unique quadratic polynomial agreeing
    with B on all of ℕ≥1 whenever P1 ∧ P3 hold.) -/
def Bext (L : ℕ → ℤ) : ℤ → ℤ := fun m ↦ TZ (m - 1) + (L 1 - 1) * (m - 1)

/-- P5 — lap palindrome on the polynomial extension: B̂(m) = B̂(1−m) ∀ m : ℤ. -/
def P5 (L : ℕ → ℤ) : Prop := ∀ m : ℤ, Bext L m = Bext L (1 - m)

/-- From P3: L(m+1) = L 1 + m for all m. -/
theorem telescope_L {L : ℕ → ℤ} (h : P3 L) (m : ℕ) : L (m + 1) = L 1 + m := by
  induction m with
  | zero => simp
  | succ r ih =>
      have h1 := h (r + 1)
      rw [ih] at h1
      push_cast
      linarith

/-- P3 ⇒ P2: the unit step is affine, so P2 is redundant. -/
theorem P3_implies_P2 {L : ℕ → ℤ} (h : P3 L) : P2 L := by
  refine ⟨1, L 1 - 1, fun m ↦ ?_⟩
  cases m with
  | zero =>
      have h0 := h 0
      simp at h0 ⊢
      linarith
  | succ r =>
      have hr := telescope_L h r
      push_cast
      linarith

/-- From P1 ∧ P3: B m = TZ(m−1) + b·(m−1) for all m ≥ 1, with b = L 1 − 1. -/
theorem formula_B {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L) (b : ℤ) (hb : b = L 1 - 1) :
    ∀ m : ℕ, 1 ≤ m → B m = TZ ((m : ℤ) - 1) + b * ((m : ℤ) - 1) := by
  intro m hm
  induction m, hm using Nat.le_induction with
  | base =>
      simp [h1.1, TZ]
  | succ r hr ih =>
      have hstep := h1.2 r
      have hL : L r = (r : ℤ) + b := by
        rw [hb]
        cases r with
        | zero =>
            have h0 := h3 0
            simp at h0 ⊢
            linarith
        | succ s =>
            have hs := telescope_L h3 s
            push_cast
            linarith
      have hp : (((r + 1 : ℕ) : ℤ) - 1) = (r : ℤ) := by push_cast; ring
      have e1 : B (r + 1) = B r + L r := by linarith
      rw [e1, ih, hL, hp]
      have hTz := TZ_pred (r : ℤ)
      rw [← hTz]
      ring

/-- For odd m : ℕ, (m : ℤ) divides TZ (m − 1). -/
theorem int_dvd_TZ_pred_of_odd {m : ℕ} (hm : Odd m) : (m : ℤ) ∣ TZ ((m : ℤ) - 1) := by
  obtain ⟨c, hc⟩ := hm
  have hc' : (m : ℤ) = 2 * (c : ℤ) + 1 := by exact_mod_cast hc
  have h2 := two_mul_TZ ((m : ℤ) - 1)
  have e : 2 * TZ ((m : ℤ) - 1) = 2 * ((m : ℤ) * (c : ℤ)) := by
    rw [h2, hc']
    ring
  have e2 : TZ ((m : ℤ) - 1) = (m : ℤ) * (c : ℤ) := mul_left_cancel₀ two_ne_zero e
  exact ⟨c, e2⟩

/-- gcd(m, m−1) = 1 in ℤ (Bezout: m − (m−1) = 1). -/
theorem isCoprime_int_self_sub_one (m : ℕ) : IsCoprime (m : ℤ) ((m : ℤ) - 1) := by
  refine ⟨1, -1, ?_⟩
  ring

/-- The Euclid step: in ℤ, if m is coprime to m−1 and m ∣ b·(m−1), then m ∣ b. -/
theorem int_self_dvd_of_dvd_mul_pred {m b : ℤ} (hco : IsCoprime m (m - 1))
    (hd : m ∣ b * (m - 1)) : m ∣ b := by
  obtain ⟨s, t, hst⟩ := hco
  obtain ⟨x, hx⟩ := hd
  refine ⟨s * b + t * x, ?_⟩
  calc b = b * (s * m + t * (m - 1)) := by rw [hst, mul_one]
    _ = b * (s * m) + b * (t * (m - 1)) := by rw [mul_add]
    _ = s * b * m + t * (b * (m - 1)) := by ring
    _ = s * b * m + t * (m * x) := by rw [hx]
    _ = m * (s * b + t * x) := by ring

/-- Three-Primitive Theorem, P4 route:
    (P1 ∧ P3 ∧ P4) → L 1 − 1 = 0  and  B m = TZ(m−1) for all m ≥ 1. -/
theorem three_primitive_P4 {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L) (h4 : P4 B) :
    L 1 - 1 = 0 ∧ ∀ m : ℕ, 1 ≤ m → B m = TZ ((m : ℤ) - 1) := by
  have key : ∀ m : ℕ, 3 ≤ m → Odd m → (m : ℤ) ∣ (L 1 - 1) := by
    intro m hm3 hodd
    have hBm := formula_B h1 h3 (L 1 - 1) rfl m (by omega)
    have hd := h4 m (by omega) hodd m (by omega) (dvd_refl m)
    rw [hBm] at hd
    have hTz := int_dvd_TZ_pred_of_odd hodd
    have hd3 : (m : ℤ) ∣ (L 1 - 1) * ((m : ℤ) - 1) := by
      obtain ⟨x, hx⟩ := hd
      obtain ⟨y, hy⟩ := hTz
      refine ⟨x - y, ?_⟩
      have e1 : (L 1 - 1) * ((m : ℤ) - 1) = (m : ℤ) * x - TZ ((m : ℤ) - 1) := by
        rw [← hx]
        ring
      rw [e1, hy]
      ring
    exact int_self_dvd_of_dvd_mul_pred (isCoprime_int_self_sub_one m) hd3
  have hb0 : L 1 - 1 = 0 := by
    by_contra hne
    set M := 2 * (L 1 - 1).natAbs + 3 with hM
    have hModd : Odd M := ⟨(L 1 - 1).natAbs + 1, by omega⟩
    have hd := key M (by omega) hModd
    have hd' : M ∣ (L 1 - 1).natAbs := by
      have h1 := Int.natAbs_dvd_natAbs.2 hd
      simpa using h1
    have hle : M ≤ (L 1 - 1).natAbs := Nat.le_of_dvd (Int.natAbs_pos.2 hne) hd'
    omega
  refine ⟨hb0, fun m hm ↦ ?_⟩
  rw [formula_B h1 h3 (L 1 - 1) rfl m hm, hb0]
  simp

/-- The extension gap: B̂(m) − B̂(1−m) = b·(2m−1) with b = L 1 − 1. -/
theorem Bext_gap (L : ℕ → ℤ) (m : ℤ) :
    Bext L m - Bext L (1 - m) = (L 1 - 1) * (2 * m - 1) := by
  have e := TZ_neg m
  unfold Bext
  rw [show (1 - m) - 1 = -m by ring, e]
  ring

/-- Three-Primitive Theorem, P5 route:
    (P1 ∧ P3 ∧ P5) → L 1 − 1 = 0  and  B m = TZ(m−1) for all m ≥ 1. -/
theorem three_primitive_P5 {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L) (h5 : P5 L) :
    L 1 - 1 = 0 ∧ ∀ m : ℕ, 1 ≤ m → B m = TZ ((m : ℤ) - 1) := by
  have hb0 : L 1 - 1 = 0 := by
    have h := h5 1
    have g := Bext_gap L 1
    rw [h, sub_self] at g
    have e : (L 1 - 1) * (2 * (1 : ℤ) - 1) = L 1 - 1 := by ring
    rw [e] at g
    exact g.symm
  refine ⟨hb0, fun m hm ↦ ?_⟩
  rw [formula_B h1 h3 (L 1 - 1) rfl m hm, hb0]
  simp

/-- P4 and P5 are equivalent given P1 + P3. -/
theorem P4_iff_P5_of_P1_P3 {B L : ℕ → ℤ} (h1 : P1 B L) (h3 : P3 L) : P4 B ↔ P5 L := by
  constructor
  · intro h4
    obtain ⟨hb0, _⟩ := three_primitive_P4 h1 h3 h4
    intro m
    rw [Bext, Bext, hb0, show (1 - m) - 1 = -m by ring]
    simp [TZ_neg]
  · intro h5
    obtain ⟨hb0, hB⟩ := three_primitive_P5 h1 h3 h5
    intro m hm1 hmodd q hq1 hqdvd
    rw [hB m hm1]
    exact dvd_trans (Int.natCast_dvd_natCast.2 hqdvd) (int_dvd_TZ_pred_of_odd hmodd)

/-! ## Independence witnesses -/

/-- Witness (i): B(m) = T(m−1) + (m−1), L(m) = m + 1  — keeps P1, P3;
    fails P4 (at m = 3) and fails P5. -/
def Bw1 : ℕ → ℤ := fun m ↦ TZ ((m : ℤ) - 1) + ((m : ℤ) - 1)
def Lw1 : ℕ → ℤ := fun m ↦ (m : ℤ) + 1

theorem witness1_P1 : P1 Bw1 Lw1 := by
  constructor
  · simp [Bw1, TZ]
  · intro m
    have hp : (((m + 1 : ℕ) : ℤ) - 1) = (m : ℤ) := by push_cast; ring
    have e1 : Bw1 (m + 1) = TZ (m : ℤ) + (m : ℤ) := by
      rw [Bw1, hp]
    rw [e1]
    simp only [Bw1, Lw1]
    linear_combination -(TZ_pred (m : ℤ))

theorem witness1_P3 : P3 Lw1 := fun m ↦ by simp [Lw1]

theorem witness1_not_P4 : ¬ P4 Bw1 := by
  intro h
  have h3 := h 3 (by norm_num) ⟨1, rfl⟩ 3 (by norm_num) (dvd_refl 3)
  norm_num [Bw1, TZ] at h3

theorem witness1_not_P5 : ¬ P5 Lw1 := by
  intro h
  have h2 := h 2
  norm_num [Bext, Lw1, TZ] at h2

/-- Witness (ii): B(m) = 2·T(m−1) = m(m−1), L(m) = 2m  — keeps P1, P4;
    fails P3.  Its polynomial extension p(x) = x(x−1) IS a lap palindrome
    (paper's reading); under the Bext convention it fails P5 (see report). -/
def Bw2 : ℕ → ℤ := fun m ↦ (m : ℤ) * ((m : ℤ) - 1)
def Lw2 : ℕ → ℤ := fun m ↦ 2 * (m : ℤ)

theorem witness2_P1 : P1 Bw2 Lw2 := by
  constructor
  · simp [Bw2]
  · intro m
    simp only [Bw2, Lw2, Nat.cast_add, Nat.cast_one]
    push_cast
    ring

theorem witness2_P3 : ¬ P3 Lw2 := by
  intro h
  have h0 := h 0
  norm_num [Lw2] at h0

theorem witness2_P4 : P4 Bw2 := by
  intro m _ hmodd q hq1 hqdvd
  obtain ⟨c, hc⟩ := hqdvd
  refine ⟨c * ((m : ℤ) - 1), ?_⟩
  rw [Bw2, hc]
  push_cast
  ring

/-- The literal polynomial extension of witness (ii): p(x) = x(x−1), agreeing
    with Bw2 on every natural. -/
theorem witness2_extension_agrees (m : ℕ) : Bw2 m = (m : ℤ) * ((m : ℤ) - 1) := rfl

theorem witness2_palindrome : ∀ m : ℤ, (m * (m - 1) : ℤ) = (1 - m) * ((1 - m) - 1) :=
  fun m ↦ by ring

/-- Under the Bext convention, witness (ii) fails P5 (Bext is built from
    b = L 1 − 1, which is only the true polynomial extension when P3 holds). -/
theorem witness2_not_P5 : ¬ P5 Lw2 := by
  intro h
  have h1 := h 1
  norm_num [Bext, Lw2, TZ] at h1

/-- Witness (iii): B(m) = T(m−1) + 1 (c₀ = 1), L(m) = m  — keeps P3, P5;
    fails P1 and P4 (at m = 3, q = 3). -/
def Bw3 : ℕ → ℤ := fun m ↦ TZ ((m : ℤ) - 1) + 1
def Lw3 : ℕ → ℤ := fun m ↦ (m : ℤ)

theorem witness3_P3 : P3 Lw3 := fun m ↦ by simp [Lw3]

theorem witness3_P5 : P5 Lw3 := by
  intro m
  have h1 : Bext Lw3 m = TZ (m - 1) := by simp [Bext, Lw3]
  have h2 : Bext Lw3 (1 - m) = TZ ((1 - m) - 1) := by simp [Bext, Lw3]
  rw [h1, h2, show (1 - m) - 1 = -m by ring, TZ_neg]

theorem witness3_not_P1 : ¬ P1 Bw3 Lw3 := by
  rintro ⟨h0, _⟩
  norm_num [Bw3, TZ] at h0

theorem witness3_not_P4 : ¬ P4 Bw3 := by
  intro h
  have h3 := h 3 (by norm_num) ⟨1, rfl⟩ 3 (by norm_num) (dvd_refl 3)
  norm_num [Bw3, TZ] at h3

/-- Witness (iii-b), the paper's alternative decoupled family: B ≡ 0 with
    L(m) = m — satisfies B 1 = 0 vacuously as a constant, P3, P4, and the
    palindrome on its (zero) polynomial extension, but violates contiguity
    B(m+1) − B m = L m at m = 1.  (Under the Bext convention it fails P5,
    since Bext is the extension determined by P1 ∧ P3; see report.) -/
def Bw3b : ℕ → ℤ := fun _ ↦ 0
def Lw3b : ℕ → ℤ := fun m ↦ (m : ℤ)

theorem witness3b_P3 : P3 Lw3b := fun m ↦ by simp [Lw3b]

theorem witness3b_P4 : P4 Bw3b := fun m _ hmodd q hq1 hqdvd ↦ ⟨0, by simp [Bw3b]⟩

theorem witness3b_not_contiguous : ¬ (∀ m, Bw3b (m + 1) - Bw3b m = Lw3b m) := by
  intro h
  have h1 := h 1
  norm_num [Bw3b, Lw3b] at h1

theorem witness3b_palindrome : ∀ m : ℤ, (0 : ℤ) = 0 := fun _ ↦ rfl

end Wheel
