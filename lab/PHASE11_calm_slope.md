# PHASE 11 — calm-slope derivation: pre-reg (a) FAILS LOUDLY, (b) PASSES stronger than wagered

Date: 2026-10-11. Artifact: `lab/PHASE11_calm_slope.py` (frozen conventions C1–C9 in the
script header — read those first). Results: `lab/PHASE11_calm_slope.json`.
Pre-registration: Claude, `HANDOFF_CLAUDE_2026-10-11c.md`.

## Verdicts

| check | target | measured | verdict |
|---|---|---|---|
| sanity `f(t)=t` | −ln10 = −2.3026 per tenfold | −2.310 (adjacent decades −2.334/−2.306/−2.304) | **PASS** |
| pre-reg (a) lane slope | −2.565 ± 0.171 per tenfold (ΔS units) | pooled 12-lane OLS: ΔS-slope −4.82 (p̄=1/34.2 → r-slope −0.141); p̄=1/29.2 → −0.165 | **FAIL** (measured r-slope −0.0750) |
| pre-reg (b) c_d terms off | removes ~11% of the MS slope | S goes linear: no log-law remains | **PASS, inverted** (see below) |
| GLM 0.64 ceiling | truncated sum reproduces cut-off curve | levels off by ~2×, shape inverted | **FAIL** (same root cause as (a)) |

## What was verified before trusting the fail (audit-first, house rule)

1. **F[d] is exact.** Brute-force check against direct local counts over t mod p for d ≤ 48:
   ratios 0.994–1.002, the residual being the expected prime tail beyond p=60. Two real bugs
   were caught and fixed in flight: Legendre sign (Euler returns −1 as q−1 mod q) and
   prime-power exponents ((D|q^e) counted once instead of e times — fires only on even
   exponents, invisible in the two-lane smoke pass). The Kronecker table was then verified
   against sympy for all 72 lanes used: zero mismatches.
2. **The machinery reproduces MS.** The linear `f(t)=t` case returns −2.334/−2.306/−2.304
   per tenfold, converging to −ln10 — the anchor [E] of the handoff.
3. **Average-1 holds computationally.** Band means of F over [1e4,1e5), [1e5,1e6),
   [1e6,1e7) are 1.0000 exactly — the analytic identity avg_d 𝔖(d) = G·∏(1/C_p)·1 = 1
   (per-prime expectation of the re-based factors is exactly 1/C_p) is confirmed.

So the miss is not arithmetic. It is model-level.

## The failure mechanism

The pooled theory rungs vs P9's measured rungs (p̄ = 1/34.2):

| W | measured r | theory r (12-lane mean) |
|---|---|---|
| 1e2 | 0.890 | 0.785 |
| 1e3 | 0.814 | 0.674 |
| 1e4 | 0.741 | 0.571 |
| 1e5 | 0.671 | 0.463 |
| 1e6 | 0.597 | 0.337 |
| 1e7 | 0.509 | 0.023 |

Even the FIRST rung is off by ~2× in S (−3.76 needed, −7.34 delivered). The gap grows
super-logarithmically: the unweighted sum T(W) = Σ_{d≤W}(F[d]−1) does not converge —
it drifts −4.5 to −9 per decade at large W with the rate itself still growing
(−7.1 at 1e6→1e7 for c=14, −9.2 for c=39). Yet band-mean F = 1 exactly: the divergence
is oscillatory, not a density deficit. The two-point singular series for a thin quadratic
sequence accumulates correlation at every scale (D's split-prime lattice: each split prime
p plants ±δ(d) classes mod p at every period), so the variance correction sum is not
summable and "the slope" is not well-defined at the ±0.005 level — only the OLS-over-rungs
procedure of the measurement gives a number, and that number is −0.14, not −0.075.

Per-lane structure: lanes with D ≡ 1 mod 3 (the forced p=3 case, b_3 = 0 killing 2/3 of
gaps) are ~2× steeper than normal lanes (S(1e7): −48 vs −26); both families miss the
measurement. Lane slope dispersion is large (60 lanes: mean −3.90 ± 1.68 over 1e2..1e6).

## Reading of the gap [S — hypothesis for the swarm]

The free quadratic singular series over-predicts the calm's strength by ~2×. The wheel's
realized turnings are **confined** (P10: ring phases locked to the stagger parabola, not
free per-prime variables). The free two-point sum is the FREE-RING ceiling; the wheel's
lanes inherit the confinement and are calmer than any free-phase model. On this reading,
Claude's measured 11%-over-MS is the gears' true contribution, the naive transfer (0.067)
is the plain-prime floor, and the singular series (−0.14) is an unachievable free-phase
bound — the calm is MADE by confinement quantitatively more than by the gears alone.
Discriminator: repeat the cut-off experiment (GLM) and check whether the flattening
asymptote matches the confined-phase prediction rather than the free truncated sum.

## GLM ceiling detail

Truncated (p ≤ 1000) free-sum curve: 0.821 / 0.729 / 0.663 / 0.618 / 0.592 / 0.577,
still descending at 1e7 (ΔS = −0.52 in the last decade). GLM's measured cut-off rungs:
0.891 / 0.820 / 0.765 / 0.729 / 0.704 / 0.689 / 0.636. Level off by ~2× at every rung;
shape inverted (theory accelerates where the measurement flattens). The truncation
mechanism is qualitatively right — cutting gears weakens and flattens the calm — but the
free-series baseline is wrong from the first rung.

## Pre-reg (b), exactly as wagered and inverted

With common-root terms off, the per-prime average of the re-based factors is
∏_p (p²−4p+2)/(p(p−4)) = exp(−2Σ_p 1/p² + O(Σ1/p³)) ≈ 0.40 < 1, so S(W) ≈ −0.6·W:
**linear, not logarithmic**. There is no slope to measure. The d²≡D terms are not an
11% correction on top of MS — they are what makes the calm a log-law at all. (For the
D ≡ 1 mod 3 lanes the p=3 common-root term is forced — b_3 = 0 — and cannot be switched
off without making a local joint density negative; those lanes are reported with the
term kept, flagged.)

## Side note: the 34.2 vs 29.2 convention

Claude's naive-transfer arithmetic uses p̄ = 1/E[ln T] = 1/34.2; a direct average over
m uniform in [1e5, 1e8] gives E[ln T(m)] ≈ 29.2. The choice moves the theory slope by
15% (wrong direction — 29.2 makes the miss worse) and is logged as a convention
difference, non-load-bearing for the fail.

## Status

The calm's slope derivation stays OPEN at the connector "quadratic pair series ⇒ wheel
lane variance" [G], now with a quantified, mechanistically-hinted gap: the free series
overshoots by 2× and the likely repair is confinement (P10 machinery), not more gears.
Plain-prime MS anchor [E] untouched. Next queue item: D2 filing.
