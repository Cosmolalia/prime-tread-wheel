# PHASE 16 (cont.) — B=131 slope point + d_home/d_flip omega-accounting

Date: 2026-10-13 (midday). Artifact: `lab/PHASE16_b131_homeflip.py`
(+ `.json`, `.log`). Both legs run on the collapsed covering ILP
(GLM collapse, audited STANDS): `min Σ y_p` s.t. every layer position is
hit by one residue class per prime, `y_p = 1` iff the ring's residue is
nonzero (displaced). Ring 2 home fixes `x_{2,0}=1`, flip fixes `x_{2,1}=1`.
All solves status=0, zero gap.

## LEG A — the B=131 slope point [E]

Discriminating test named this morning (`PHASE16_omega_curve.md`):
does `k(B) = 0.876/ln B − 0.117` (2 params, 3 points: 31/53/97) predict
the fourth? Prediction: k(131) ≈ 0.0627.

| m | d |
|---|---|
| 25 | 3 |
| 50 | 4 |
| 100 | 8 |
| 150 | 10 |
| 200 | 13 |

Fit: **k₁₃₁ = 0.0578, c = 1.530**. |k − pred| = 8% of pred → **A2 PASS**
(the 1/ln B shape survives its first honest test; the fit is still only
2 params / now 4 points, so "law" remains [S]-grade, one more B would help).
**A1 PASS**: all five m feasible → certifies **j(131#) ≥ 201** as a side
catch (not in A048669's verified prefix; Hagedorn's tables likely carry it —
marked [E]-checkable, not yet checked).

## LEG B — d_home/d_flip omega-accounting [E]

GPT's handback §5 question (does ring-2 phase carry a systematic wedge
cost?) as pure arithmetic at the native schedule:

| m | rings | d_free | d_home | d_flip | gap (flip−home) | ω* = rings − d |
|---|---|---|---|---|---|---|
| 100 | 19 | 9 | 10 | **9** | **−1** | 10 / 9 / 10 |
| 263 | 42 | 15 | **15** | 17 | **+2** | 27 / 27 / 25 |

- **B1 PASS**: free(263) = home(263) = 15 — the collapsed ILP binds to the
  MILP-measured d=15 to the unit, and the home optimum known from
  PHASE15_dynrings is reproduced. Universal-"optimal-wipes-flip-ring-2" was
  already false at 263; now certified optimal, not just exhibited.
- **B2 — passes in magnitude, fails in sign (honest report)**: the frozen
  prediction "gap ∈ [0,3], home-neutral-to-slightly-worse" holds at m=263
  (gap +2) but **reverses at m=100, where flip is strictly better by 1**.
  So ring-2 phase is near-neutral (|gap| ≤ 2 at both points) but its
  direction is **m-dependent** — there is no universal home or flip
  advantage. What survives of the turning story: "not a ring-2 artefact"
  is now certified at both ends — the phase pays at most 2 displacement
  units either way, while d itself is 9–17.
- ω-accounting: at 263 rings, the best home-constrained translate carries
  ω = 27 prime divisors (flip-constrained only 25). The wedge is decided
  by *which* primes divide the translate, and ring-2 parity shifts the
  achievable ω by exactly ±2 at this scale.

## Verdicts

A1 PASS · A2 PASS (8% off prediction) · B1 PASS · B2 magnitude PASS,
sign REFUTED at m=100 · j(131#) ≥ 201 side-catch [E-checkable].
k-law status: [S], now 2 params / 4 points, still open at one more B.
