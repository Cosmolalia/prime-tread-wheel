/-
  GLM's lock+palindrome lemma (WHITEPAPER §16.8) — the surviving
  theorem-grade content of the seam-lock retraction.

  For quadratic counts B(m) = (αm² + βm + γ)/2, carried as the exact doubled
  identity 2·B(m) = αm² + βm + γ (so integrality is built in):

    • the seam lock  (∀ odd m, ∀ q > 0, q ∣ m → q ∣ B m)  ⟺  γ = 0;
    • the lap palindrome  (∀ m, B m = B (1−m))  ⟺  α + β = 0;
    • both together with the 1:1 turn condition B(m+1) − B m = m force
      α = 1, β = −1, γ = 0, i.e. B = T(·−1) uniquely.

  The wheel (α, β, γ) = (1, −1, 0), B = T(·−1), satisfies all three
  conditions (the `wheel_model_*` checks), so both iff's are inhabited on
  both sides.
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- A quadratic count: 2·B(m) = αm² + βm + γ for all m : ℤ (the division by 2
    is carried exactly, as in `two_mul_TZ`). -/
def IsQuadCount (B : ℤ → ℤ) (α β γ : ℤ) : Prop :=
  ∀ m, 2 * B m = α * m ^ 2 + β * m + γ

/-- In ℤ, an odd q dividing 2·b divides b. -/
private lemma int_odd_dvd_of_two_mul {q b : ℤ} (hodd : Odd q) (hd : q ∣ 2 * b) : q ∣ b := by
  obtain ⟨c, hc⟩ := hodd
  obtain ⟨x, hx⟩ := hd
  refine ⟨b - c * x, ?_⟩
  have e1 : q * (b - c * x) = q * b - c * (q * x) := by ring
  rw [e1, ← hx, hc]
  ring

/-- In ℤ, a divisor of an odd number is odd. -/
private lemma int_odd_of_dvd_odd {q m : ℤ} (hodd : Odd m) (hd : q ∣ m) : Odd q := by
  rcases Int.even_or_odd q with hj | hj
  · obtain ⟨j, hj⟩ := hj
    obtain ⟨c, hc⟩ := hd
    obtain ⟨k, hk⟩ := hodd
    have e1 : (2 : ℤ) * k + 1 = 2 * (j * c) := by rw [← hk, hc, hj]; ring
    have e2 : (2 : ℤ) * (j * c - k) = 1 := by linear_combination -e1
    have hdvd : (2 : ℤ) ∣ 1 := ⟨j * c - k, e2.symm⟩
    norm_num at hdvd
  · exact hj

/-- The palindrome gap: 2·(B(m) − B(1−m)) = (α + β)·(2m − 1). -/
theorem quad_gap (B : ℤ → ℤ) (α β γ : ℤ) (hq : IsQuadCount B α β γ) (m : ℤ) :
    2 * (B m - B (1 - m)) = (α + β) * (2 * m - 1) := by
  have e1 := hq m
  have e2 := hq (1 - m)
  linear_combination e1 - e2

/-- GLM lock ⟺ γ = 0 (the count starts at the origin). -/
theorem glm_lock_iff_gamma (B : ℤ → ℤ) (α β γ : ℤ) (hq : IsQuadCount B α β γ) :
    (∀ m : ℤ, Odd m → ∀ q : ℤ, 0 < q → q ∣ m → q ∣ B m) ↔ γ = 0 := by
  constructor
  · intro hlock
    -- q := M at the odd integer M = 2|γ|+3 forces M ∣ γ, hence γ = 0.
    set M : ℕ := 2 * γ.natAbs + 3 with hM
    have hModd : Odd M := ⟨γ.natAbs + 1, by omega⟩
    have hModd' : Odd (M : ℤ) := by
      obtain ⟨c, hc⟩ := hModd
      refine ⟨c, ?_⟩
      rw [hc]
      push_cast
      ring
    have hpos : (0 : ℤ) < M := by exact_mod_cast (by omega : 0 < M)
    have hd := hlock (M : ℤ) hModd' (M : ℤ) hpos (dvd_refl (M : ℤ))
    have h2M : 2 * B M = α * M ^ 2 + β * M + γ := hq M
    have hMdvd : (M : ℤ) ∣ α * M ^ 2 + β * M := ⟨α * M + β, by ring⟩
    have hγ : (M : ℤ) ∣ γ := by
      have e : γ = 2 * B M - (α * M ^ 2 + β * M) := by linarith
      rw [e]
      have hd2 : (M : ℤ) ∣ 2 * B M := by
        obtain ⟨w, hw⟩ := hd
        refine ⟨2 * w, ?_⟩
        rw [hw]
        ring
      exact Int.dvd_sub hd2 hMdvd
    have hγ' : M ∣ γ.natAbs := by
      have h := Int.natAbs_dvd_natAbs.2 hγ
      simp at h
      exact h
    by_cases hγ0 : γ = 0
    · exact hγ0
    · have hle := Nat.le_of_dvd (Int.natAbs_pos.2 hγ0) hγ'
      omega
  · intro hγ m hmodd q hqpos hqdm
    have hqodd : Odd q := int_odd_of_dvd_odd hmodd hqdm
    have h2q : q ∣ 2 * B m := by
      have h2m := hq m
      rw [hγ, add_zero] at h2m
      have h1 : q ∣ α * m ^ 2 + β * m := by
        obtain ⟨c, hc⟩ := hqdm
        exact ⟨c * (α * m + β), by rw [hc]; ring⟩
      rw [h2m]
      exact h1
    exact int_odd_dvd_of_two_mul hqodd h2q

/-- GLM palindrome ⟺ α + β = 0. -/
theorem glm_palindrome_iff (B : ℤ → ℤ) (α β γ : ℤ) (hq : IsQuadCount B α β γ) :
    (∀ m : ℤ, B m = B (1 - m)) ↔ α + β = 0 := by
  constructor
  · intro hpal
    have h1 : B 1 = B 0 := hpal 1
    have e1 := hq 1
    have e0 := hq 0
    norm_num at e1 e0
    linarith
  · intro hab m
    have hg := quad_gap B α β γ hq m
    rw [hab] at hg
    norm_num at hg
    omega

/-- GLM uniqueness: lock + palindrome + the 1:1 turn condition force
    (α, β, γ) = (1, −1, 0), i.e. B = T(·−1). -/
theorem glm_unique (B : ℤ → ℤ) (α β γ : ℤ) (hq : IsQuadCount B α β γ)
    (hlock : ∀ m : ℤ, Odd m → ∀ q : ℤ, 0 < q → q ∣ m → q ∣ B m)
    (hpal : ∀ m : ℤ, B m = B (1 - m))
    (hturn : ∀ m : ℤ, B (m + 1) - B m = m) :
    α = 1 ∧ β = -1 ∧ γ = 0 ∧ ∀ m : ℤ, B m = TZ (m - 1) := by
  have hγ : γ = 0 := (glm_lock_iff_gamma B α β γ hq).1 hlock
  have hab : α + β = 0 := (glm_palindrome_iff B α β γ hq).1 hpal
  have hturn2 : ∀ m : ℤ, α * (2 * m + 1) + β = 2 * m := by
    intro m
    have e1 := hq (m + 1)
    have e2 := hq m
    have ht := hturn m
    linear_combination -e1 + e2 + 2 * ht
  have hα : α = 1 := by
    have h1 := hturn2 1
    norm_num at h1
    linarith
  have hβ : β = -1 := by linarith
  refine ⟨hα, hβ, hγ, ?_⟩
  intro m
  have e1 := hq m
  rw [hα, hβ, hγ] at e1
  have h2 := two_mul_TZ (m - 1)
  rw [sub_add_cancel] at h2
  have e2 : 2 * B m = 2 * TZ (m - 1) := by linear_combination e1 - h2
  exact mul_left_cancel₀ two_ne_zero e2

/-! ## The wheel model inhabits both sides of the iff's. -/

/-- The wheel count B(m) = T(m−1) as a quadratic count with (α, β, γ) = (1, −1, 0). -/
theorem wheel_model : IsQuadCount (fun m ↦ TZ (m - 1)) 1 (-1) 0 := by
  intro m
  have h := two_mul_TZ (m - 1)
  rw [h]
  ring

/-- The wheel count satisfies the seam lock (γ = 0, backward direction). -/
theorem wheel_model_lock :
    ∀ m : ℤ, Odd m → ∀ q : ℤ, 0 < q → q ∣ m → q ∣ TZ (m - 1) := by
  intro m hmodd q _hqpos hqdm
  have hqodd : Odd q := int_odd_of_dvd_odd hmodd hqdm
  obtain ⟨c, hc⟩ := hqdm
  have h2 : 2 * TZ (m - 1) = m * (m - 1) := by
    have h := two_mul_TZ (m - 1)
    rw [h]
    ring
  have hd : q ∣ 2 * TZ (m - 1) := by
    refine ⟨c * (q * c - 1), ?_⟩
    rw [h2, hc]
    ring
  exact int_odd_dvd_of_two_mul hqodd hd

/-- The wheel count is a lap palindrome: T(m−1) = T(−m) = T((1−m)−1). -/
theorem wheel_model_palindrome : ∀ m : ℤ, TZ (m - 1) = TZ ((1 - m) - 1) := by
  intro m
  rw [show (1 - m) - 1 = -m by ring, TZ_neg]

/-- The wheel count has the 1:1 turn: T(m) − T(m−1) = m. -/
theorem wheel_model_turn : ∀ m : ℤ, TZ (m + 1 - 1) - TZ (m - 1) = m := by
  intro m
  rw [show m + 1 - 1 = m by ring]
  have h := TZ_pred m
  linarith

end Wheel
