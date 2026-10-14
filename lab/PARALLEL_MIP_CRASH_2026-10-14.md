# Parallel-MIP crash observation — 2026-10-14 (morning)

Question: can the m=1500 native MILP be sped up by using more of the
machine's 32 cores? (Sylvan's ask.)

## Background

`lab/phase15_sparse_relay.py` solves via `scipy.optimize.milp` → HiGHS.
The scipy wrapper exposes no threading options, and the observed run uses
~1 core (branch-and-bound is serial in this configuration). `highspy`
1.15.1 was installed to reach HiGHS's `parallel` / `threads` options
directly (incremental addVars/addRows API; model construction verified
against the scipy reference dimensions at m=600: nvar 15,537, nrows 682).

## Observation [E]

`parallel=on, threads=16`, m=600 testbed: the solve starts normally
(dual bound progressing, ~22.2 at 80 s vs the single-thread reference's
294 s to optimal d=26) but the process vanishes without error output or
JSON result at ~80–100 s elapsed, reproducibly (2/2 attempts). No OOM
(dmesg/journalctl clean; 11 GB available throughout). Single-threaded
runs under identical construction are stable (the scipy lane has dozens
of clean completions; the portfolio lane below runs the same highspy
construction with parallel off).

Status: filed as an environment/ solver-build instability. Not load-
bearing — the portfolio approach does not depend on it.

## What actually got deployed instead

Portfolio racing: same model, `parallel=off, threads=1`,
`random_seed` ∈ {1,2,3,4}, 24 h cap, launched 08:31 alongside the
primary m=1500 run (PID 3900668, scipy lane, 24 h cap from 07:44).
Logs: `lab/PF1500_seed{1..4}.log`, verdicts `lab/PF1500_seed{1..4}.out`.
Verdict rule: best (lowest) objective with gap 0.0 wins; if none close,
best dual bound across lanes is reported as the honest bound.
