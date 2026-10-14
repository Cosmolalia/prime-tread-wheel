# PHASE 19 — m=1000 overnight rerun: PROVEN OPTIMAL, d = 37

Date: 2026-10-14 (06:07, mid-course check caught it early). Artifact:
`lab/PHASE19_sparse_m1000_overnight.log` (verbatim below).

```
{"m": 1000, "rings": 126, "vars": 40313, "nnz": 166313, "seconds": 17842.78,
 "mode": "free", "status": 0, "message": "Optimization terminated successfully.
 (HiGHS Status 7: Optimal)", "objective": 37.0, "best_bound": 37.0, "gap": 0.0,
 "phase2": 0, "displacements": 37, "uncovered": 0}
```

Closed after 4 h 57 m of the 12 h cap — the plain rerun tightened the
3 h incumbent (38) by exactly one and then proved closure.

## Verdicts against the frozen predictions

- **GLM's band [37, 43]: PASS — at the low edge.** d = 37 is the band's
  lower bound, inclusive. The band is now fully tested, not half-tested.
  The true optimum sits at the very bottom of what GLM registered.
- **Native-law ratio, now on a PROVEN point:**
  1.26 (263) → 1.22 (300) → 1.14 (400) → 1.11 (600) → **1.02 (1000)**.
  pred = m/(4 ln m) = 36.19; 37/36.19 = 1.022. The ratio compression
  continues and this point is a proof, not an incumbent — the 1.05 from
  the 3 h run tightens to 1.02.

## Honest read on the additive residual — NOT monotone

d − pred: 3.1 → 2.8 → 2.3 → 2.55 → **0.81**. The ratio converges
cleanly, but the additive residual jumped down only at 1000 after
flatlining at 600. So "ratio → 1" is supported by five proven points;
"smooth additive decay" is refuted by the 600 → 1000 step. Two readings:
[G] either the residual is noisy at the 1-ring scale (each unit of d is
one ring — at these magnitudes a single ring is 2-3% of d), or the law's
finite-m correction has structure the linear-in-m model doesn't carry.
Next discriminating point per the adopted convention: m = 1500 or 2000
(normalized position x = m/(j(B#)−1)).

## Instrument notes

- The overnight run was a plain rerun — the 3 h run had logged only the
  objective, not the translate vector, so no warm start was possible.
  Lesson filed: persist solution vectors.
- This makes five native proven points (263, 300, 400, 600, 1000), all
  by the same sparse MILP instrument.
