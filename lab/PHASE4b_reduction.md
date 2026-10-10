# Phase 4b — C1 proof attempt: the reduction verdict (2026-10-10 ~03:00)

## Attempt

One genuine proof attempt on C1 (≥1 interval prime strictly each side of the
layer midpoint, all m ≥ 21) via the B-theorem cluster, per plan.

## What the cluster gives

- B1 [F]: at layer m the wheel's visible set is EXACTLY the primes in the
  window — "the wheel at layer m is the sqrt(N) sieve rendered as occlusion."
  Every value in the window exceeds T(m−1) ≈ m²/2 ≫ m (m ≥ 7), so any prime
  in the window is > m, and any composite in the window has a factor
  ≤ √T(m) ≈ m/√2 < m — i.e., among the rings. The occlusion is precisely
  trial division by primes ≤ m; nothing else.
- N1 [E]: the stagger/phase law has zero internal correlation — no coupling
  or inductive lever (the field IS the odometer).
- N10 [E]: values don't inherit the seat palindrome — no symmetry lever.
- halves_struct [E]: free rings can cover either half of every layer 21..60 —
  no capacity lever.

## The reduction

By B1, "the left half of layer m contains an interval prime" ⟺
"∃ prime in [T(m−1)+1, T(m−1)+⌊m/2⌋]" — unconditionally, with no wheel
content surviving the translation. That interval has length ⌊m/2⌋ at height
N ≈ m²/2, i.e. length ≈ √(N/2)·(1/√2) ≈ 0.7·√N·... parameterized against
Legendre's conjecture (prime in [x², (x+1)²], length ≈ 2√N): **C1 asserts
primes in intervals ~3× SHORTER than Legendre's, at comparable height.**
(The right half is symmetric.)

## Consequence — the proof door closes by reduction

Best unconditional short-interval result: π(x+x^0.525) − π(x) ≫ x^0.525/ln x
(Baker–Harman–Pintz 2001). Primes in [x, x+c√x] (Legendre and strengtheners)
are open; C1 is a constant-factor strengthening of Legendre, restricted to
triangular windows. Since B1 says the wheel contributes NOTHING beyond the
√N sieve, no wheel-native proof strategy can escape that class: a wheel proof
of C1 would be a sieve-independent proof of a sub-Legendre interval
conjecture. **"Zero structural support" is now explained, not just observed:**
support would require structure the sieve doesn't have, and the wheel is the
sieve. This also cleanly explains the C1/C2 contrast: C2 (one prime in the
full width-m window) has finite structural support (to layer 57, confined)
because one prime in width m is vastly easier than one in width m/2 — the
halves split is exactly what pushes the claim across the √N boundary.

## Status reassessment (honest)

- C1 stays [S], but its paper role changes: it cannot be the theorem of a
  paper — it is a machine-checkable instance of a Legendre-family conjecture,
  verified to 1M+ laps (G7, running). Under Cramér it is expected true with
  margins growing like ln²N — G7's pre-registered call (c) tests exactly this.
- The paper-value migrates from the CLAIM to the INSTRUMENT: the wedge (F2)
  — "conjecture = one realized quadratic curve never enters the characterized
  wipe set; the per-lap DISTANCE is measurable (SAT)" — is wheel-native, new,
  and produces data no sieve pipeline emits. Pair with G7's margin law for
  the empirical half.
- Falsifiable prediction recorded: G7 worst-margins ~ Cramér ln²N growth;
  deviation = news about prime gaps at triangular windows (P12 mechanism).

## Labels

- C1-reduction: [F] (argument above; 1-line core: B1 ⇒ C1 ⟺ sub-Legendre
  short-interval conjecture).
- C1: [S, Legendre-hard by reduction] — replaces "strongest paper candidate"
  with "strongest conjecture-instance; proof out of current reach."
- Wedge distance (F2/J1c): promoted to the paper's candidate core.
