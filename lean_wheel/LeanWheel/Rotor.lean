/-
  Prime Tread Wheel — §18.11 Schwinger rotor tuning [F].

  For a general rotor-plus-field spectrum `E = a·j(j+1) + b·m_z` on the
  Schwinger two-oscillator ladder:
    * the intra-lap spacing `E(j, m_z+1) − E(j, m_z)` is exactly `b`;
    * the inter-lap gap `E(j+1/2, −j−1/2) − E(j, +j)` is exactly
      `a·(j + 3/4) − b·(2j + 1/2)`;
    * demanding the inter-lap gap equal `b` for all `j` forces
      `a·(j + 3/4) = 2b·(j + 3/4)`, hence `b/a = 1/2` **uniquely**
      (up to overall scale) — the wheel's `Â = 2J² + J_z + I` tuning.

  Also included: the spectrum glue, `2j(j+1) + m_z + 1 = T(m−1) + k` on
  lap `m` with `j = (m−1)/2`, `m_z = k − (m+1)/2` (exact over ℚ, no
  evenness side condition needed at this resolution).
-/

import Mathlib

namespace Wheel

/-- Intra-lap ladder spacing of `E = a·j(j+1) + b·m_z` is exactly `b`. -/
lemma rotor_intra_lap_spacing (a b j m : ℚ) :
    a * (j * (j + 1)) + b * (m + 1) - (a * (j * (j + 1)) + b * m) = b := by
  ring

/-- Inter-lap gap from the top of lap `j` to the bottom of lap `j + 1/2`:
    `E(j+1/2, −j−1/2) − E(j, +j) = a·(j + 3/4) − b·(2j + 1/2)`. -/
lemma rotor_inter_lap_gap (a b j : ℚ) :
    a * ((j + 1/2) * ((j + 1/2) + 1)) + b * (-(j + 1/2))
      - (a * (j * (j + 1)) + b * j)
    = a * (j + 3/4) - b * (2*j + 1/2) := by
  ring

/-- **[F] Schwinger rotor tuning (WHITEPAPER §18.11).**
    If the inter-lap gap equals the intra-lap spacing `b` for every `j`,
    then `b/a = 1/2`.  (One equation at `j = 0` already forces it; the
    hypothesis is stated for all `j` exactly as in the paper.) -/
theorem schwinger_rotor_tuning (a b : ℚ) (ha : a ≠ 0)
    (h : ∀ j : ℚ, a * (j + 3/4) - b * (2*j + 1/2) = b) : b / a = 1/2 := by
  have h0 := h 0
  rw [div_eq_iff ha]
  linarith

/-- Spectrum glue: on lap `m`, with spin `j = (m−1)/2` and projection
    `m_z = k − (m+1)/2`, the tuned rotor `2j(j+1) + m_z + 1` evaluates to
    `m(m−1)/2 + k = T(m−1) + k`, the wheel's integer address.  Over ℚ the
    halves are exact, so no evenness case split is needed here. -/
lemma wheel_spectrum_glue (m k : ℚ) :
    2 * ((m - 1)/2) * (((m - 1)/2) + 1) + (k - (m + 1)/2) + 1
      = (m - 1) * m / 2 + k := by
  ring

end Wheel
