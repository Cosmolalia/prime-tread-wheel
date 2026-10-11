# PHASE 7 — pre-registered replication scorecard: layer statistics to 1.8M layers

Date: 2026-10-10. Run by Kimi on the 32-thread lab box. Predictions written by
Claude *before* the run, in `column-engine/HANDOFF_TO_KIMI.md` §4; they are
quoted verbatim below. This is the witness-layer protocol applied across
machines: same binary, different hardware, frozen predictions.

## Instrument certification (before trusting new numbers)

- Compiled `column-engine/layerstats.c` locally, re-ran Claude's own
  100k-layer segment: summary block byte-identical on all 9 lines
  (fewest / worst-exp / longest-run / clash per decade, total primes
  234,956,465 = π(T(1e5)) ✓, last-layer-with-≤c list, e^γ/2 banner).
- Only the thread-count/timing header differed. Engine certified against
  the author's box before the pre-registered segment was run.

## The run

- Command: `./layerstats 1800000 layers_1p8M.csv` — layers 1..1,800,000,
  numbers to T(1.8M) = 1,620,000,900,000 (~1.62e12).
- Wall: 6843.6 s (~1 h 54 min) on 32 threads ≈ **60.8 CPU-hours**.
  Claude's estimate was "~5,400 thread-seconds (~11 min on 8 cores)" —
  underestimated by ~40×. Recorded as part of the scorecard; the
  predictions, not the time estimate, are what was being tested.
- Sanity: measured total primes 59,837,421,097 matches the asymptotic
  li(1.62e12) = 5.9837e10 within series-truncation error [E].

## Scorecard

| # | Prediction (frozen, pre-run) | Measured | Verdict |
|---|---|---|---|
| 1 | clash factor 100k–1M: 0.8906 ± 0.0005 | **0.89064** | **HIT** (+0.00004 from center) |
| 2 | clash factor 1M–1.8M: 0.8905 ± 0.0005 | **0.89060** | **HIT** (+0.00010) |
| 3 | fewest primes on a layer, 100k–1M: 4000–4350 | **4323** (at m=100,767) | **HIT** |
| 4 | fewest primes on a layer, 1M–1.8M: 35300 ± 700 | **36,720** (at m=1,093,005) | **MISS** (+1,020 over center; 720 over the band edge) |
| 5 | worst count/(m/ln T), 100k–1M: ≥ 0.93 | **0.959** | **HIT** |
| 6 | worst count/(m/ln T), 1M–1.8M: ≥ 0.95 | **0.985** | **HIT** |
| 7 | longest prime-free run / m, 100k–1M: ≤ 0.005 | **0.00305** | **HIT** |
| 8 | longest prime-free run / m, 1M–1.8M: ≤ 0.0006 | **0.00048** | **HIT** |
| 9 | last-layer-with-≤c list unchanged, all ≤ 121 | identical: 1 7 16 33 52 66 79 79 109 109 121 | **HIT** |

**8/9 hit.** The one miss is informative, not noise-shaped:

- The miss is **upward**: the sparsest layer of the top band holds *more*
  primes than the fluctuation model behind "35300 ± 700" allowed.
- Mechanism-level read [F from the measurements]: the worst/exp floor is
  still climbing (0.959 → 0.985, decade over decade) toward 1, and the
  absolute minimum of the layer counts is converging to expectation from
  *above*. Layer counts are **more uniform** than an iid-style tail model
  suggests — consistent with the anti-clumping intuition of the clash
  factor itself (rings over-cover correlated slots, which smooths the low
  tail as well as shaving the mean). The ±700 band was a guess with an
  unstated fluctuation model; the data says the min-of-8e5-layers tail is
  tighter than that guess. Residual: the fluctuation model behind the
  band is [G] — worth one derivation, not urgent.
- Both clash rows converging to e^γ/2 = 0.89054 from above (0.89092 →
  0.89064 → 0.89060): the phantom-clash haircut mechanism holds at 16×
  the certified range [E].

## Data

- `column-engine/layers_1p8M.csv.gz` — full per-layer counts
  (m, count, longest_run, indep) for all 1.8M layers, 47 MB → 14.5 MB.
- `column-engine/layerstats_1p8M_run.log` — the summary block above.

## Status labels

- Clash-factor law: [E] at 1.62e12 (was [E] at 5e9).
- "Every layer has primes, count → ∞": [E] for all layers ≤ 1.8M; the
  universal claim stays [S]/Legendre-hard per HANDOFF §3.
- Layer-count fluctuation model: [G].
