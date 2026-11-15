/-
  B3 — the triangular-offset theorem (WHITEPAPER §4, B3), formalized over ℤ
  exactly as stated in the audit task:

      2·(T(m−1) + m − c) = (m−j)(m+j+1)  ↔  2c = j(j+1).

  The paper's prose form "N = T(m−1) + m − c factors as (m−j)(m+j+1)/2 exactly
  when c = T(j)" is the same statement after multiplying through by 2 and
  expanding T (over ℤ the division is justified by `two_mul_TZ`).
-/

import Mathlib
import LeanWheel.Defs

namespace Wheel

/-- B3 — the triangular-offset theorem, over ℤ, as a two-way equivalence. -/
theorem B3 (m j c : ℤ) :
    2 * (TZ (m - 1) + m - c) = (m - j) * (m + j + 1) ↔ 2 * c = j * (j + 1) := by
  have h := two_mul_TZ (m - 1)
  constructor
  · intro he
    linear_combination h - he
  · intro he
    linear_combination h - he

/-- The paper's form: with c = T(j) the factorization holds; and conversely the
    factorization forces 2c = j(j+1), i.e. c is the j-th triangular number. -/
theorem B3_forward (m j : ℤ) :
    2 * (TZ (m - 1) + m - TZ j) = (m - j) * (m + j + 1) :=
  (B3 m j (TZ j)).2 (two_mul_TZ j)

end Wheel
