# PHASE 15 (part 2) — wedge d-curve under varying ring schedules

Date: 2026-10-12 (morning, autonomous). Probe: `lab/PHASE15_dynrings.py`
(frozen predictions in its header). Results: `lab/PHASE15_dynrings.json`,
log `lab/PHASE15_dynrings.log`.

## LEG S — fixed-B sensitivity (B=31, 11 rings; B=53, 16 rings), object A

- **B=31: infeasible at m = 60, 100, 150** (HiGHS status 8, MILP-infeasible,
  not solver failure — the status field distinguishes them). Frozen caveat
  said None on m ≤ 150 would be informative: it places j(31#) ≤ 60.
  [F+E consistent]
- **B=53: d = 7 at m=60 (U=7, pred 4.91), d = 11 at m=100 (U=15, pred 8.67),
  infeasible at m=150.** Predictions undershoot by ~2–3 at both finite
  layers (d ≈ U + small, harvest constant ≈ 1 near B=53), None at 150
  places j(53#) ≤ 150. [F+E consistent; B-dependence confirmed in sign —
  smaller B ⇒ smaller d, and feasibility cliffs exactly where Jacobsthal
  of the ring primorial says they must be]

## LEG N — native schedule (rings = primes ≤ √T(m)), object A

| m | rings | d | P (prime-value ticks) | d/P | d/m | frozen band N2 |
|---|---|---|---|---|---|---|
| 263 | 42 | 15 | 28 | 0.54 | 0.0570 | [18.2, 34.0] |
| 300 | 47 | 16 | 27 | 0.59 | 0.0533 | [17.6, 35.5] |
| 400 | 60 | 19 | 39 | 0.49 | 0.0475 | [25.4, 49.4] |
| 600 | 82 | 26 | 53 | 0.49 | 0.0433 | [34.5, 70.5] |
| 1000 | ~120 | — | — | — | — | OOM-killed (below) |

- **N1: PARTIAL PASS** — finite (optimal) on 4/4 measured layers
  263/300/400/600. **m=1000 never landed: the MILP build was OOM-killed
  by the kernel at 09:31** (anon-rss 19.8 GB, total-vm 43 GB; the run
  checkpoints per layer, everything up to m=600 was saved). This is an
  infrastructure limit, not a science result; m=1000 needs a
  memory-streamed formulation or a bigger box.
- **N2: FAIL as frozen, in the informative direction.** d sits BELOW the
  harvest-only band 0.65·P at every layer. The fixed-ring harvest constant
  does not transfer: under the native schedule d/P ≈ 0.49–0.59 (mean ~0.53,
  stable across a 2.3× m-range). Mechanism attribution [S]: with more rings
  per layer, one displaced ring covers a denser residue set and harvests
  more uncoverable ticks per displacement — harvest efficiency rises with
  ring budget, so d falls below the B=97-calibrated floor.
- **N3: PASS on the measured trend.** d/m declines monotonically
  0.0570 → 0.0533 → 0.0475 → 0.0433 across the four layers. The frozen
  m=1000 comparison point is unavailable (OOM), but the sublinear
  direction is unambiguous in the data that exists.

## Adjudication summary

The headline claim of part 1 survives and sharpens: **the 1/13.5 slope is
ring-budget-contingent, not a wheel constant.** Under the wheel's own
growing sieve the displacement cost grows measurably slower than linear,
at d ≈ 0.5·P(m) ≈ 0.5·m/(2 ln m), i.e. d/m ~ 1/(4 ln m) → 0. New
mechanistic observation [S, load-bearing for any future slope claim]:
harvest efficiency (ticks covered per displaced ring) is itself a
function of ring density — constants calibrated at one B do not transfer
across schedules.

## Open

- [G] m=1000 under native rings — needs a memory-bounded MILP
  formulation (the current dense build dies ~120 rings / 1M ticks).
- [G] exact harvest-efficiency law vs ring density (d/P as a function of
  B/ln T); four points at B~√T suggests saturation near ~0.5.
