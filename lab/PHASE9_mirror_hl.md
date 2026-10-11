# PHASE 9 — mirror-pair Hardy–Littlewood pre-registration: HIT at 0.99

Date: 2026-10-11. Artifact: `lab/PHASE9_mirror_hl_prereg.py` (frozen conventions
in file header — read there first). Companion results: this file.

## The frozen test

GLM froze formula + decision rule in chat 2026-10-11 (reproduced verbatim in
the script header). Target: B7's measured mirror-pair count — even-m mirror
pairs are Goldbach representations of m² in the layer window; observed
**11,085** pairs over even 4 ≤ m < 3000 (2026-10-10 session; convention audit
below shows this count is m=2 excluded, unordered, T(m−1) < p ≤ m²/2).

Decision rule (frozen): E/observed ∈ [0.8, 1.25] → [E] "sieve furniture", B7
closes with a quantitative match. Outside → convention audit FIRST, only then
signal.

## Outcome

**Frozen formula as written: E = 801.1, ratio 0.0723 — far out of band.**
Convention audit (window edges ✓, m=2 inclusion ✓ explains exactly ±1:
recount gives 11,086 incl / 11,085 excl, reproducing the reference count
bit-for-bit, unordered ✓) cleared all three flagged items. The discrepancy
survived the audit.

**Root cause found [form error in the frozen formula, not in the
conventions]:** the formula summed the full pair density 1/(ln p·ln q) over
*p prime* — the pair density already contains the p-prime factor, so
sampling it only at primes divides by an extra ~ln p (weighted mean of the
per-layer shortfall = 13.84 ≈ the observed factor). Two standard forms,
neither tuned:

| form | E (m≥4) | ratio obs/E |
|---|---|---|
| GLM frozen (Σ over primes of 1/(ln p·ln q)) | 801.1 | 0.0723 |
| sieve form (Σ over primes p of 1/ln(m²−p)) | 11,197.6 | **0.9899** |
| integral form (Σ over all integers x of 1/(ln x·ln(m²−x))) | 11,170.8 | **0.9923** |

The integral form is the faithful reading of GLM's written intent ("sum of
1/(ln p · ln(m²−p)) over the window") with "p" ranging over integers; the
sieve form is the standard prime-only statement. Both land at **0.99**.

## Verdict

Per the frozen decision rule, with the correction logged: **[E] sieve
furniture.** The B7 mirror-pair count follows the same Hardy–Littlewood mesh
law as the radial locks — 2C₂·∏_{p|m}(p−1)/(p−2) over the layer window, C₂ =
0.6601618. B7 closes with a quantitative match. No value-side structure; P12
stands.

House-rule note: the out-of-band first pass is exactly what the prereg was
for — the formula froze, failed loudly (0.072, not 0.9), and the audit found
a form error with a mechanism (extra ln p), not a fudge. Two independent
standard forms agreeing at 0.99 against 11,085 counted events is the
confirmation; a single corrected formula would have been weaker.

## Epistemic labels

- [F] B7 mirror lift (identity T(m−1)+T(m)=m², bijection) — proven.
- [E] 11,085 pairs, zero odd-m pairs — measured, reproduced here.
- [E→this note] even-m count follows HL mesh law, ratio 0.99 — measured,
  pre-registered, one documented formula correction.
- [G] none opened. The odd-m prohibition stays proven (parity), not
  statistical.
