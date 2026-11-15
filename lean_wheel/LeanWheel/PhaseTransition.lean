/-
  Theorem II part 3 — the T(m)^{1/4} phase-transition threshold
  (WHITEPAPER §19.2.3).

  With B = ⌊√(T(m−1))⌋ (`Bm`), every tick T(m−1)+k = p^a·Q with Q > B has
      p^a · (B+1) ≤ p^a · Q = T(m−1)+k ≤ T(m),
  so any ring with p²·(B+1) > T(m) — the exact kernel form of the paper's
  p > (T(m)/B)^{1/2} ≈ T(m)^{1/4}, slightly tighter since Q ≥ B+1 — carries
  no higher power a ≥ 2 with Q > B: a_max(p) = 1 identically.
-/

import Mathlib
import LeanWheel.Defs
import LeanWheel.Orphan

namespace Wheel

/-- The phase-transition theorem: above the exact threshold p²·(B+1) > T(m)
    every unconditional home orphan of p is a first power. -/
theorem phase_transition (m p a Q : ℕ) (hp : p.Prime) (hpa : 1 ≤ a)
    (hthresh : T m < p ^ 2 * (Bm m + 1))
    (hk : 1 ≤ k) (hkm : k ≤ m) (hdecomp : T (m - 1) + k = p ^ a * Q)
    (hQ : Bm m < Q) : a = 1 := by
  by_contra hne
  have ha2 : 2 ≤ a := by omega
  have hp2a : p ^ 2 ≤ p ^ a := pow_le_pow_right₀ hp.one_lt.le ha2
  have hB1 : Bm m + 1 ≤ Q := by omega
  have hchain : p ^ 2 * (Bm m + 1) ≤ p ^ a * Q :=
    calc p ^ 2 * (Bm m + 1) ≤ p ^ a * (Bm m + 1) := Nat.mul_le_mul hp2a (le_refl _)
      _ ≤ p ^ a * Q := Nat.mul_le_mul (le_refl _) hB1
  have hNm : p ^ a * Q ≤ T m := by
    rw [← hdecomp]
    have h1 := T_pred m (by omega : 1 ≤ m)
    omega
  omega

/-- The paper's intermediate bound in nat-divided form: every such tick has
    p^a < T(m)/B (needs m ≥ 3 so B ≥ 1). -/
theorem pow_mul_Bm_lt_Tm (m p a Q : ℕ) (hm : 3 ≤ m) (hp : p.Prime) (_hpa : 1 ≤ a)
    (hk : 1 ≤ k) (hkm : k ≤ m) (hdecomp : T (m - 1) + k = p ^ a * Q)
    (hQ : Bm m < Q) : p ^ a * Bm m < T m := by
  have hB1 : Bm m + 1 ≤ Q := by omega
  have h2 : p ^ a * (Bm m + 1) ≤ p ^ a * Q := Nat.mul_le_mul (le_refl _) hB1
  have h3 : p ^ a * Bm m < p ^ a * (Bm m + 1) :=
    Nat.mul_lt_mul_of_pos_left (Nat.lt_succ_self _) (pow_pos hp.pos _)
  have h4 : p ^ a * Q ≤ T m := by
    rw [← hdecomp]
    have h1 := T_pred m (by omega : 1 ≤ m)
    omega
  omega

/-- The exact threshold in root form: p²·(B+1) > T(m)  ⟺  p > √(T(m)/(B+1)),
    and (B+1)² > T(m−1) (`Nat.lt_succ_sqrt'`) gives B ≈ √(T(m)), placing the
    threshold at ≈ T(m)^{1/4}.  The paper's displayed sufficient form
    p² > T(m)/B is slightly looser (B < B+1). -/
theorem phase_transition_threshold_shape (m : ℕ) (hm : 3 ≤ m) :
    T (m - 1) < (Bm m + 1) ^ 2 := Nat.lt_succ_sqrt' (T (m - 1))

end Wheel
