# PHASE 18 — m=1000 native MILP: FEASIBLE d=38, optimality NOT proven (time limit)

Date: 2026-10-13 (night, cap 23:22). Artifact: `lab/PHASE18_sparse_m1000.log`
(solver `lab/phase15_sparse_relay.py 1000 10800 free`, fired 20:22).

## Raw outcome

```json
{"m": 1000, "rings": 126, "vars": 40313, "nnz": 166313, "seconds": 10800.09,
 "mode": "free", "status": 1, "message": "Time limit reached. (HiGHS Status 13)",
 "objective": 38.00000000000004, "best_bound": 32.0, "gap": 0.15789,
 "phase2": 0, "displacements": 38, "uncovered": 0}
```

## What this is — and is not

- **A feasible wheel exists with d = 38** (all 1000 laps covered, 126 rings).
  So the true optimum d(1000) ∈ **[32, 38]**.
- **Optimality is NOT proven.** HiGHS hit the 3 h cap with a 15.8% MIP gap
  (incumbent 38, dual bound 32). A timeout is not a verdict: d could still
  be 32–37. GLM's frozen band d ∈ [37, 43] is therefore **consistent with
  the evidence but not confirmed** — if the optimum lands at 32–36, the
  band dies on the low side.

## Native-law ratio

pred = m/(4 ln m) = 36.19 at m=1000. Feasible incumbent ratio:
38/36.19 = **1.05** — continues the sequence 1.26 → 1.22 → 1.14 → 1.11
(m = 300/400/600, all proven optimal) *downward*, but unlike the earlier
points this one is an upper-bound ratio: the proven-optimal ratio could be
as low as 32/36.19 = 0.88. The convergence story survives on the incumbent;
it is not yet stress-tested at m=1000.

## Options for the relay

1. Accept "d ≤ 38, opt ∈ [32,38]" as the m=1000 line (honest, weaker than
   the 300/400/600 PROVEN OPTIMAL lines).
2. Rerun overnight with a longer cap (e.g. 12 h) — m=600 took 294 s at
   15.5k vars; m=1000 is 40k vars and was still 15.8% from closed at 3 h,
   so closure is not guaranteed at 12 h either, but the bound would sharpen.
3. Warm-start the rerun from the d=38 incumbent.
