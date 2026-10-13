# PHASE 16 — dial C-decomposition census: what actually selects a winning ratio

Date: 2026-10-13. Artifact: `lab/PHASE16_dial_census.py` (+ `.json`,
`_grid.json`). 18.5 s for the full grid.

## Question

Post-sharpening (evidence swarm, filed bb89446): "7/6 is the wheel's modal
ratio" was naming, not measurement. The measured content: argmax of the
live-family singular series C over the PHASE8b 20-ratio b≤8 sweep. Open:
what selects the winner, and at what resolution is argmax-C stable?

## Method

Every coprime a/b with 2 ≤ b ≤ 60, 1 ≤ a ≤ 2b (2202 ratios; 2132 with live
families). Per ratio: live eligible-class quadratics via the exact PHASE8b
engine (ties-up convention), per-family C_small = ∏_{p≤67}(1−ρ/p)/(1−1/p),
decomposed as logC2 + logC_bad(odd p|b) + logC_rest. LEG V validates against
the full brute C (p<2000) on the old-20 ratios + observed leaders.

## Frozen-verdict adjudication

- **D1 PASS**: at b≤8, argmax C_small = 7/6 (the old sweep reproduces).
- **D2 PASS**: at b≤60, argmax = **89/46** (C 6.83), not 7/6.
- **D3 FAIL (refuted)**: top-10 at every cut is b-parity mixed; more
  decisively — **logC2 = log 2 for all 2132 live ratios.** The engine's
  parity eligibility filter (n odd) forces every induced family odd-valued,
  so ρ(2)=0 and the 2-adic factor is ×2 everywhere. It cannot select
  anything. The "b-even dial deletes ring 2" mechanism is dead as a
  selector [E-refuted at census scale].
- **D4 half**: 7/6's bad-prime factor at 3 = 1.5 exactly (ρ=0) ✓, but
  logC2 = log 2, **not log 4** — the "×4" in the swarm decomposition was
  wrong; the absolute 2-adic factor is ×2, universal.
- **D5 order-fail, set-pass**: small-C vs full-C top-5 are the SAME SET
  {89/46, 45/47, 6/31, 95/59, 6/59}; the internal order shuffles (all five
  within a 2% cluster; small/full ratios 0.95–1.01). At p≤67 the top-tier
  membership is stable; the order within it is cutoff noise.

## 7/6's rank vs resolution [S→measured]

| b-cut | rank of 7/6 |
|---|---|
| ≤ 8  | 1/35   |
| ≤ 12 | 3/78   |
| ≤ 20 | 14/232 |
| ≤ 30 | 48/521 |
| ≤ 60 | 442/2132 |

"Modal" was the small-league champion. The league grows with b and the
champion dissolves into it.

## The selector, decompressed [F from measurement]

Per-family ρ-profile of the leaders (ρ = roots mod p; factor =
p/(p−1) if ρ=0, (p−2)/(p−1) if ρ=2):

- **89/46** C 6.83: ρ=0 at 16 primes ≤67 (gain ×7.10), losses only at
  47, 61 (ρ=2).
- **45/47** C 6.81: ρ=0 at 15 primes, losses at 53, 59, 67.
- **6/31** C 6.79: ρ=0 at 15 primes, losses at 43, 67.
- **95/59**, **6/59**, **19/45**: same shape — ~15 inert primes, 2–3
  split losses, all at large primes.
- **7/6** C 4.76: ρ=0 at only 11 primes; **six** split losses
  (29, 41, 43, 53, 59, 61).

Bad-prime (p|b) factors of the leaders are ≈ ×1.0 — neutral. So:

1. **C = prime-avoidance constellation of the family's values.** For odd p
   not dividing the leading coefficient, ρ(p)=0 ⟺ the discriminant is a
   quadratic non-residue mod p ⟺ p is **inert** in the family's quadratic
   field [E, standard; qualified 2026-10-13 per GPT §10 of the day relay —
   the code counts roots by direct scan, so exceptional primes dividing the
   leading coefficient/conductor/discriminant are handled exactly; the ⟺
   statement itself requires p odd and p ∤ A]. The winners are
   families whose discriminant's field keeps nearly every small prime
   inert (16/19 at p≤67 vs density 1/2 for a random discriminant).
2. **The dial's real role is lattice richness, not advantage**: live
   family count grows with b (7/6: 2; 89/46: 44; 45/47: 60). More
   families = more constellations to search = better best-of-N. The
   resolution-dependence of argmax-C is a **search effect**, and the
   winners cluster at C≈6.6–6.8 (best-of-N saturation at the p≤67
   cutoff), not at a dial-determined ceiling.
3. Two different "winners" depending on the statistic: best single
   family = 89/46; total predicted haul (ΣC, tickets×odds) = **1/59**
   at b≤60. The sharpened dial question must specify which.

## Consequences

- The value-side dial story is now: **best-of-N inert-constellations over
  the ratio's family lattice.** Any future "privileged ratio" claim must
  state its b-resolution and its statistic (max-C vs ΣC) or it is
  naming, not measurement.
- Untouched: the realized turning (which curve the wheel actually rolls)
  — this census is the BH/instrument side, as the collapse ledger
  requires.
- Cutoff caveat: profiles are p≤67; full-C shifts ±4%, top-tier set
  stable. Named follow-up if ever needed: p≤151 profiles of the top-5.

## Verdicts

D1 PASS, D2 PASS, D3 FAIL (2-adic selector refuted, universal ×2),
D4 half (×2 not ×4; bad-3 = 1.5 ✓), D5 set-pass/order-fail.
