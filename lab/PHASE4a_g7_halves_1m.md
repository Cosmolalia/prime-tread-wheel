# PHASE 4a — Probe G7: Halves claim (C1) extended to 1M laps

Date: 2026-10-10. Probe: `probes/g7_halves_1m.py`. Data: `lab/g7_halves_1m.csv`.
CPU-only, single-thread, pure-Python deterministic Miller–Rabin
(bases [2,3,5,7,11,13,17], exact below 3.47×10¹⁴; our max value is
T(10⁶) ≈ 5×10¹¹). Convention matched exactly to `halves_struct.py`:
window = values T(m−1)+1 .. T(m−1)+m, T(m−1) = m(m−1)//2; left half =
ticks 1..⌊m/2⌋, right half = ticks ⌊m/2⌋+1..m.
MR cross-validated against the lab's 13-base `primes_util.is_prime` on
200k random values across the full range: 0 disagreements. Walk logic
verified against brute-force sieve for m = 21..300.

## THE number

**Laps covered: 999,980 (m = 21 .. 1,000,000). Full range — no time wall.**
Run time 5.2 min (~3,200 laps/s; the 90-min budget was never at risk).

**VIOLATIONS of C1: 0 (ZERO).**

Every one of the 1M windows has ≥1 prime in each half. Prior 120k-lap
record (0 violations, worst margin 240) now extends to 1M laps with zero
violations. C1 stands.

## W_L / W_R distributions

| stat | W_L | W_R |
|---|---|---|
| median | 15 | 16 |
| mean | 20.73 | 22.69 |
| p99 | 100 | 102 |
| p99.9 | 150 | 152 |
| max | 300 (m=692704) | 299 (m=530131) |

(120k-lap prior: median 11–12 — the 1M medians are 15/16; the small-lap
populations pull medians down at 120k, so this is consistent, not a shift.)

## Mirror symmetry (the N11 "statistical ghost")

- **Lap-level correlation**: Pearson r = 0.0106 (p≈3e-26), Spearman ρ =
  0.0109 — statistically nonzero only because n=10⁶ amplifies dust;
  practically **zero**, as pre-registered. Correlation conditioned on
  m-parity: 0.009 (even m), 0.012 (odd m).
- **Marginals**: KS test rejects identity (stat 0.131, p≈0) —
  but the entire deviation is a **deterministic parity-of-edge effect**:
  when a window edge lands on an even value, the walk wastes its first
  step (only odd values are prime candidates). Mean W when the edge is
  odd ≈ 19.9 (L) / 21.4 (R); when the edge is even ≈ 21.5 (L) / 23.9 (R).
  This is a ±1–2.5 tick shift, fully structural, not a dynamical
  asymmetry. After accounting for edge parity there is no residual ghost.
  Verdict: mirror symmetry **confirmed up to the parity granularity**.

## Worst-margin growth trend

Binned max(W_L, W_R) vs window scale N (log–log against ln N):

- Regression of log(maxW) on log(ln N) over 24 log-spaced bins:
  **slope = 2.19 ± 0.08, R² = 0.977** — statistically consistent with
  Cramér-scale (ln² N) growth, clearly not flat.
- In absolute terms: max W at the top of the range = 300 while
  ln²(T(10⁶)) ≈ 726, so the worst margin runs at **≈ 0.41 × ln²(N)** —
  Cramér-shaped but with a small constant, i.e. comfortably below the
  Cramér upper bound.
- Trend of raw max per bin: 12 (m≤33) → 240 (m≈1e5) → 300 (m=1e6).
  The 120k worst of 240 is now the 1e5-bin value; the 1M worst is 300.

Runway: a C1 violation needs a prime desert wider than the half-window
H = m/2 ticks, i.e. a gap of ~√N/2 in absolute terms near N. Worst
observed margin is ~300 ticks at N≈5×10¹¹; ln²(N)≈726; H at m=10⁶ is
5×10⁵. Even Cramér-speed growth gives orders of magnitude of headroom —
the binding constraint for the claim is not edge-walk margins but whether
any window of width m at all can be prime-free (a much stronger,
independently-observed non-event).

## Danger scan — closest C1 ever came to failing

Margin-to-midpoint per half: left = ⌊m/2⌋ − W_L − 1, right = (m − W_R) −
⌊m/2⌋ − 1; min over halves. Top-10 smallest:

| rank | m | H=⌊m/2⌋ | W_L | W_R | margin | margin/H |
|---|---|---|---|---|---|---|
| 1 | 33 | 16 | 12 | 4 | 3 | 0.188 |
| 2 | 42 | 21 | 1 | 16 | 4 | 0.190 |
| 3 | 24 | 12 | 0 | 7 | 4 | 0.333 |
| 4 | 25 | 12 | 6 | 8 | 4 | 0.333 |
| 5 | 50 | 25 | 3 | 16 | 8 | 0.320 |
| 6 | 23 | 11 | 3 | 5 | 6 | 0.545 |
| 7 | 35 | 17 | 3 | 11 | 6 | 0.353 |
| 8 | 26 | 13 | 5 | 2 | 7 | 0.538 |
| 9 | 21 | 10 | 0 | 2 | 8 | 0.800 |
| 10 | 28 | 14 | 0 | 5 | 8 | 0.571 |

**The closest call in 1M laps is m=33: the left half's only prime sat 3
ticks from the midpoint (tick 13 of 16).** Every close call has m ≤ 63;
for m ≥ 10⁴ the minimum observed margin-to-midpoint is ~0.987·H (primes
hug the edges as H outruns ln N), and the largest walk is 300 ticks vs
H ≥ 500,000. By both metrics (relative and absolute) C1's closest
approach was a small-lap event and the claim has been getting *safer*,
not riskier, with scale.

## Pre-registered calls — verdicts

- **(a) Zero violations to 1M laps — CONFIRMED.** 0 / 999,980.
- **(b) Mirror-identical marginals, lap-correlation ≈ 0 — CONFIRMED with
  a caveat.** Correlation ≈ 0.011 ≈ 0 as called. Marginals are
  statistically distinguishable at n=10⁶, but the entire deviation is
  the deterministic parity-of-edge effect (±1–2.5 ticks); no residual
  asymmetry. The N11 ghost remains a ghost.
- **(c) Worst margin grows slower than ln²(N) — NOT CONFIRMED as stated.**
  The binned-max trend is exponent 2.19 ± 0.08 on ln N, i.e. Cramér-scale
  (not slower, not flat). However, the absolute constant is ≈ 0.41, so
  observed worst margins stay far below ln²(N) itself; the 120k→1M
  extension (240 → 300) is exactly the gentle growth this implies.

## Method notes

- Incremental CSV, fsync every 10k laps; no crash occurred (clean
  completion, exit 0), resume logic present but unused.
- Values > 2 are tested only when odd; trial division against primes ≤
  10⁴ precedes MR rounds (rejects the overwhelming majority of
  composites without a single modular exponentiation).
- W = −1 would mark a half with no prime (violation encoding); no such
  row exists.
