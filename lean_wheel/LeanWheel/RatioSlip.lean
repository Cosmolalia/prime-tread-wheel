/-
  Theorem I part 2 — the ratio-slip recurrence (WHITEPAPER §19.1.2).

  For any modulus p ≥ 1, working in ZMod p, the stagger field
      o_p(m) = −T(m−1)
  evolves by the first-order difference equation
      o_p(m+1) = o_p(m) − m        (in ZMod p),
  and divisibility is detected exactly:
      p ∣ (T(m−1) + k)  ↔  (k : ZMod p) = o_p(m).
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- The stagger field o_p(m) = −T(m−1) as an element of ZMod p. -/
def o (p : ℕ) (m : ℕ) : ZMod p := - (T (m - 1) : ZMod p)

/-- Theorem I part 2 (a) — the ratio-slip recurrence in ZMod p. -/
theorem o_succ (p m : ℕ) : o p (m + 1) = o p m - (m : ZMod p) := by
  simp only [o, Nat.add_sub_cancel, T_self_sub_add m, Nat.cast_add, neg_add, sub_eq_add_neg]

/-- Theorem I part 2 (b) — the exact divisibility criterion. -/
theorem dvd_iff_eq_o (p m k : ℕ) (_hp : 1 ≤ p) :
    p ∣ (T (m - 1) + k) ↔ (k : ZMod p) = o p m := by
  constructor
  · intro h
    have h0 : ((T (m - 1) + k : ℕ) : ZMod p) = 0 := (ZMod.natCast_eq_zero_iff _ _).2 h
    push_cast at h0
    rw [add_comm] at h0
    exact eq_neg_of_add_eq_zero_left h0
  · intro h
    apply (ZMod.natCast_eq_zero_iff (T (m - 1) + k) p).1
    have hk : (k : ZMod p) = - (T (m - 1) : ZMod p) := h
    have hsum : ((T (m - 1) : ℕ) : ZMod p) + (k : ZMod p) = 0 := by
      rw [hk]
      ring
    push_cast
    exact hsum

end Wheel
