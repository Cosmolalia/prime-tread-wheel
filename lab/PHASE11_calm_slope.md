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

---

# CORRECTION v2 (2026-10-11 night) — pre-reg (a) SUPERSEDED: the fail was three artifacts, and the pair series matches on every rung

Source: Claude's relay `HANDOFF_CLAUDE_2026-10-11d.md` + GPT-6's relay §5–§7. House
rule applied: every fix audited independently before accepting. All three verify; the
filed FAIL stands below as the baseline (per house rules), superseded by PASS.

## Fix 3 (code, mine) — VERIFIED, decisive: the "not summable" drift was a bound mismatch

`build_F` applied the generic base G over odd primes ≤ PG = 1e7 but the common-root
(bp) correction only for split primes ≤ B2 = 1e5. Every split prime in (1e5, 1e7] left
a uniform −4/p² on ln F[d] with no +back on the ±δ classes, so mean(F) sat 7.9e-7 below
1 and S picked up −7.9e-7·W — exactly the "T(W) drifts −5..−9 per decade, rate still
growing, not summable" that was filed here as a mechanism.

Independent audit (`lab/PHASE13_fix3_audit.py`, my own build_F, B2 = 1e7):
- drift/W = **7.94–8.01e-7** at every W ≥ 1e5 on lanes 14 and 39 (claim was 7.86–8.01);
- band-mean of F over [9e6, 1e7) rises by exactly 7.94e-7 / 7.99e-7 under the fix;
- lane 14 last-decade slope collapses **−10.09 → −2.92**; lane 39 −12.78 → −5.60
  (lane 39 is a C = 0.41 poor lane; its C·S steps are −1.89..−2.58, same family);
- fixed-series C·S per-decade steps: −2.54, −2.17, −2.34, −2.27, −2.26 (lane 14) and
  −2.58, −1.89, −2.30, −2.32, −2.29 (lane 39) vs −ln10 = −2.3026; the shallow last
  step is the prime bound sitting at Wmax (Claude's edge.py: bound at 3e7 deepens it).

**The "not summable" claim retracts.** It was a one-signed mean deficit accumulating
linearly — the same artifact class as the (b) linear collapse, a million times smaller
(Claude's diagnosis, confirmed).

## Fix 2 (formula, Claude's handoff-c) — VERIFIED algebraically: the self-term

P9's baseline v = Σ q(1−q), q = 2p̄ on odd values. Exact identities, no approximation:
(e − v)/2 = Σ p̄² over the lane's values, and with the MS form Var = μ(1 + p̄(S−1)):
R − 1 = p̄(S+1)/(1−2p̄), pooled R − 1 = Σ_lanes ((e−v)/2)(S+1) / Σ v. Handoff c wrote
"1 + p̄·S" — the +1 self-term was omitted; I implemented the spec as written. Worth
≈ +0.02 on every rung. (The f(t)=t sanity shows it: S(1e7) + ln 1e7 = −0.4151 = B+1.)

## Fix 1 (sample, mine) — VERIFIED: the 12 lanes are all 5-poor

c = 14 + 25k forces D = 1−8c ≡ 4 (mod 5): ring 5 splits on every sampled lane.
Mean C over my 12 lanes = **0.7470** vs **0.9996** over P9's 300 (p9_a/b.jsonl).
C·S is universal, so poor lanes carry large |S|; uniform p̄ = 1/34.2 is right only for
a C = 1 lane. Correct per-lane weight: (e − v)/2, read off P9's own e and v.

## The result — all 300 P9 lanes, pooled exactly as P9 pools (reproduced, not trusted)

Re-ran Claude's `tools/pool300.py` on his `data/all300.jsonl`: his table reproduces
digit-for-digit, and his per-lane S curves match my own build_F(B2=1e7) to **8e-9**.

| W | 1e2 | 1e3 | 1e4 | 1e5 | 1e6 | 1e7 |
|---|---|---|---|---|---|---|
| measured (P9) | 0.8902 | 0.8142 | 0.7410 | 0.6707 | 0.5965 | 0.5093 |
| theory | 0.8895 | 0.8140 | 0.7408 | 0.6675 | 0.5942 | 0.5229 |
| z | −9.3 | −1.2 | −0.3 | −1.8 | −0.5 | +1.0 |

- **Slope per tenfold, six rungs: theory −0.0733 vs measured −0.0751 — inside the
  frozen ±0.005. Pre-reg (a): PASS (superseding the filed FAIL).**
- Every rung W ≥ 1e3 within 1.8 SE. The 1e2 residual (−0.0007, z = −9.3) lives in the
  scorer (window-edge terms O(p̄·ln W/W)): P9's sched stream shows the same −0.0006
  against its own series. Also note: real ≈ sched at every rung — the sieve model and
  the actual primes do not diverge (P12-adjacent confirmation).
- 1e8 rung [G]: one more −ln10 step gives 0.4494 vs measured 0.4458 ± 0.036.
- The bare singular series does this with **no fitted parameter and no confinement
  term**. C·S(W) = −ln W + O(1) lane-by-lane (Claude's exact identity: the
  Bateman–Horn constant is exactly the reciprocal residue of the pair series);
  cross-lane sd of C·S ≈ 0.19, and of a step falls to 0.016 by the last decade.
- **GLM's 0.64 ceiling: resolved.** The rings ≤ 1000 truncation pooled reproduces
  P9's sched column at every rung (|z| ≤ 1.3 for W ≥ 1e3); the curve plateaus at
  ≈ 0.68–0.70 by construction of the truncated sum. His 0.636 at 1e8 is a single
  300-window rung ≈ 1σ low (SE 0.05).

## Confinement [S]: RETIRED (by normalization audit, not by a confinement experiment)

GPT's relay §7 [G] was the right instinct: the pair series was never "free" — ρ(p) =
1 + (D|p) and the common-root factors already carry the seam lane's actual quadratic
residue structure (P10's confined root sets). Once the mean is honest (fix 3), the
weighting is per-lane (fix 1), and the self-term is included (fix 2), nothing is left
for a confinement term to explain. The [S] filed earlier tonight is retired; the
record should read: filed under a normalization gap, killed by audit. GLM's frozen
confined-phase prereg (triangular-image intersection weights c_pq) loses its target —
withdrawn by events; the (a)-gap it was meant to close no longer exists. Anyone who
wants it anyway: it's cheap, but a match would now prove nothing about confinement.

## Pre-reg (b): PASSES as filed, with the mechanism claim CORRECTED (GPT §5–§6)

Two errors in the filing, both GPT's catches, both confirmed:
1. **The printed no-common-root mean formula was wrong.** Printed μ_p =
   (p²−4p+2)/(p(p−4)) exceeds 1 for every p > 4 (p=5: 7/5). The correct local mean is
   μ_p = 1 − 2/(p−2)² (p=5: 7/9), and the committed JSON says S/W ≈ −0.298 at 1e7,
   i.e. mean ≈ **0.70, not 0.40** as the note claimed. Corrected here; the qualitative
   "linear in W" claim was right (S_B(1e6)/S_B(1e5) = 9.996).
2. **"Common-root terms are what make the calm a log-law at all" overclaims.** GPT's
   mean-preserving ablation, reproduced exactly under
   `lab/PHASE13_ablation_prereg.md` (frozen before running): μ computed =
   **0.70164914826** vs his 0.7016491483; his A/B/C S-curves reproduced to 3 decimals;
   band-mean(F_B) = 0.70166; variant C (common-root off, mean restored) is log-like —
   per-decade slope ratio 0.40 (frozen gate < 0.75) and the ln-fit beats the linear
   fit 1.1 vs 15.6 in residual SS. **The load-bearing structure is the mean-1
   normalization; the common-root terms are its physically correct construction, not
   its unique source.** (Fix 3 is the same lesson in miniature.)

## Corrected epistemic state

- Calm slope on wheel lanes [E]: Montgomery–Soundararajan log-law on the wheel's
  polynomial family, Var/μ = (ln N − ln W + κ − C)/ln N per lane, pooled exactly as
  measured. The wheel's third loud anomaly dissolves into classical law — third in one
  day (P9 mirror pairs, P10 C4, P11 calm).
- Claude's standing claim sharpened: the value side of the wheel keeps scoring
  classical; the content is on the index side (families + exact theorems).
- House-rule tally for this note: 1 code bug (mine, load-bearing), 1 sample bias
  (mine), 1 spec omission (Claude's handoff c), 1 formula error (mine), 1 overclaim
  (mine). Freeze → fail loudly → audit → classical. The method is the result.
