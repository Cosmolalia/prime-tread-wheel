# PHASE 16 — omega-degradation curve: the wedge slope as pure arithmetic

Date: 2026-10-13. Artifact: `lab/PHASE16_omega_curve.py` (+ `.json`, `.log`).
22 s total; zero MILP (native m=300/400 MILPs below, 19 s/40 s, proven
optimal). Frame: GLM CRT-shift collapse (audited STANDS), d = |P| − ω(a*).

## LEG A — B=97 reference curve [E]

From the existing PHASE14 objA d-curve (244 layers, 14..257): k_d = 0.0747,
c = 0.54, max resid 3.3; ω: 24 → 3 across the cliff edge (GLM's endpoints
confirmed arithmetically).

## LEG B/C — collapsed exact-cover curves (new measurements)

| m | B=31 (11 rings) | B=53 (16 rings) |
|---|---|---|
| 14 | 2 | 1 |
| 20 | 3 | 3 |
| 28 | 3 | 3 |
| 36 | 5 | 5 |
| 44 | 6 | 5 |
| 52 | 7 | 4 |
| 57 | 8 | — |
| 60 | — | 7 |
| 72 | — | 7 |
| 84 | — | 8 |
| 96 | — | 9 |
| 105 | — | 13 |

Every point exact (exhaustive S-search + exact-cover DFS, per-point
deadline; none hit). Full table in `.json`.

**Measured slopes** (least squares): k_31 = **0.1386**, k_53 = **0.1037**,
k_97 = 0.0747.

## The B-law [S→measured, 2-param fit on 3 exact points]

k(B) = 0.876/ln B − 0.117 fits all three: 0.138 / 0.104 / 0.075
(residuals < 0.001). Shape right, but a 3-point fit with one free check —
**named discriminating test: B=131 or B=151** (predicts k ≈ 0.066/0.063).
Negative intercept cannot hold globally (k>0 needs B<1800; the native
regime, where U collapses entirely, is a different object anyway).

## Frozen verdicts

- **F1 FAIL** (both bands): measured 0.139/0.104 vs frozen [0.070–0.095].
- **F2 PASS**: measured above the PHASE15 two-load extrapolation at both
  small B (0.139 vs 0.086; 0.104 vs 0.081). Direction right, amplitude
  off 30–60%: the constants 0.215/0.051 calibrated at B=97 do NOT
  transfer down-B. The U-density theory has the correct 1/ln B shape and
  wrong small-B amplitude — plausibly the linear-in-m assumption on U(m)
  (its sawtooth/early ramp) at small windows; [G] at the level of why the
  amplitude is 0.876 rather than 0.215·e^γ-scale.
- **F3 PASS**: collapsed DFS == MILP JSON at B=97, m=60 (d=6, 2.4 s).
  The two instruments are bound at 25 rings [E].
- **F4 PASS**: ω(14)=24, ω(257)=3.

## LEG D — native schedule (rings = primes ≤ √T(m−1))

| m | rings | d | law pred 0.5·m/(2 ln m) | d/pred | ω |
|---|---|---|---|---|---|
| 263  | 42 | 15 | 11.9 | 1.26 | 27 |
| 300  | 47 | **16** (opt) | 13.2 | 1.22 | 31 |
| 400  | 60 | **19** (opt) | 16.7 | 1.14 | 41 |
| 1000 | 127 | 38 (inc, bound 32) | 36.2 | 1.05 | 89 |

m=300/400 both proven optimal by the sparse MILP (free mode). The
0.5-prefactor law sits **systematically low but converging**: d−pred =
3.1 → 2.8 → 2.3 → ~1.8. Four points, one an incumbent — [S→measured];
named follow-up m=600 to watch the decay.

## What this settles and what it opens

Settled: the slope is arithmetic, measurable to the unit in seconds, and
steepens as B shrinks with a clean 1/ln B law across three bounds.
Opened: (i) B=131/151 discriminating point for the k(B) law; (ii) the
small-B amplitude gap vs the two-load model; (iii) native-law finite-m
correction decay; (iv) GPT's d_home/d_flip split is now pure ω-accounting
(free vs forced non-divisors), queue item #6.
