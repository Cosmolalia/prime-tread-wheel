# PHASE 3 — cross-layer correlation closure, retained-structure axis

Pre-registered prediction: **NULL** — no cross-layer correlation at any separation
or lag beyond the deterministic small-prime base.

This is the final closure attempt on the retained-structure axis: does the ring-state /
band-content (ω_small) pattern carry any exploitable correlation ACROSS layers — a
"wave" traveling from layer to layer that would make band content at one layer
predictive of band content at another? Consecutive layers' certified windows are
separated by ~m−W ≈ 451k uncertified ticks in N-space, so windows of different layers
are not adjacent; there is no adjacency confound.

Per theorem A2 the ring phase law is purely s(m) = −T(m−1) mod p — phases carry no
information beyond the odometer T. This phase tests the one thing A2 does not cover:
the witness-count content itself.

- CPU only, numpy. GPU untouched; nothing from gpu-frontier/cache/ was loaded.
- Independent sieve of the 82,885 primes ≤ 1,060,673 (bound =
  int((m+1)/√2)+1 across m = 1,500,000..1,500,015), built in-script.
- ω_small(N) = # distinct prime divisors p ≤ bound; computed sieve-style per window:
  `cnt = zeros(W, uint8); cnt[(-N0) mod p :: p] += 1` for each prime. Self-consistency:
  layer 1,500,000 mean ω_small = 2.8917, matching Phase 2's independent trial-division
  audit (2.89169).
- Real: L = 16 consecutive layers m = 1,500,000 .. 1,500,015, each W = 1,048,576
  ticks wide (N0 = T(m−1)+m−W+1).
- Honest null: 20 pairs of random 1M-windows at random offsets in [10¹¹, 10¹³],
  same sieve, same ω computation, seed 20261010. The distribution of the
  max-|corr|-over-all-lags statistic across these 20 pairs IS the
  multiple-comparison-corrected null envelope (searching all lags is built in).
- Statistic: series mean-centered and unit-norm; FFT cross-correlation
  (numpy.fft, length 2W) over ALL lags −(W−1)..(W−1); record max |corr| and its lag.
  Identical construction for real and null.

## 1. Headline: max |corr| over all lags, layer m vs layer m+j

Null envelope (20 pairs): min 0.3610, mean 0.3795 ± 0.0087, q50 0.3812,
q90 0.3912, q95 0.3922, max 0.3929.

| j | real max\|corr\| | lag of max | quantile of real in null dist | exceeds null max? |
|---|---|---|---|---|
| 1 | 0.3785 | −1,080,106 | 0.40 | no |
| 2 | 0.3737 | +15,483 | 0.25 | no |
| 3 | 0.3716 | +23,226 | 0.20 | no |
| 4 | 0.3688 | +30,970 | 0.15 | no |
| 5 | 0.3655 | +38,715 | 0.10 | no |
| 6 | 0.3752 | +21,051 | 0.30 | no |
| 7 | 0.3623 | +49,588 | 0.05 | no |
| 8 | 0.3804 | +18,066 | 0.45 | no |
| 9 | 0.3650 | −1,057,412 | 0.10 | no |
| 10 | 0.3707 | +9,625 | 0.15 | no |
| 11 | 0.3835 | −1,095,041 | 0.70 | no |
| 12 | 0.3680 | +42,138 | 0.10 | no |
| 13 | 0.3713 | +100,711 | 0.20 | no |
| 14 | 0.3723 | +69,195 | 0.20 | no |
| 15 | 0.3759 | +37,680 | 0.35 | no |

Real range 0.362–0.383 lies entirely INSIDE the null envelope [0.361, 0.393].
Quantiles of the real statistics within the null distribution span 0.05–0.70 —
uniformly unremarkable (15 draws from a 20-point null would, under the null
hypothesis itself, spread exactly like this). No separation j = 1..15 shows any
cross-layer signal at any lag.

## 2. Lag-0 predictivity probe (j = 1..3, direct corr(cnt_m[i], cnt_{m+j}[i]))

| j | real corr(0) | null \|corr(0)\| envelope (20 pairs) |
|---|---|---|
| 1 | −0.1841 | mean \|c0\| 0.114 ± 0.066, max 0.185 |
| 2 | −0.0435 | (same distribution) |
| 3 | +0.2183 | frac of null \|c0\| ≥ real: **0/20** |

At face value j = 3 (and j = 15 at +0.2433) exceed every unconditioned null |c0|.
This is NOT structure — it is the deterministic small-prime base, and it is fully
explained and reproduced:

- The layer spacing is fixed: D_j = N0(m+j) − N0(m) = j·m + j(j+1)/2, with
  m = 1,500,000 = 2⁵·3·5⁶. Hence D_1 = 1,500,001 (odd → parity patterns
  anticoincide, corr(0) ≈ −0.18), D_3 = 4,500,006 = 2·3·7·107143, and
  D_15 = 22,500,120 = 2³·3·5·93751.
- Lag-0 correlation between two ω series is dominated by the alignment of the
  spacing with small primes: if D ≡ 0 mod p, the p-divisibility lattice of the
  two windows coincides (positive contribution); if D ≢ 0, it is out of phase
  (negative). Random null offsets almost never align as well with 2,3,5,7 as the
  real layer spacings do.
- Conditioned-null check (seed 777, 20 pairs each): null pairs with
  X1−X0 ≡ 0 mod 42 (j=3-like 2·3·7 alignment) give mean |corr(0)| = 0.234
  (range 0.214–0.301); with X1−X0 ≡ 0 mod 120 (j=15-like 2³·3·5) mean 0.257
  (range 0.238–0.331). Both AT or ABOVE the real values 0.218 and 0.243.
  Random windows given the same deterministic alignment reproduce — in fact
  exceed — the real lag-0 excursions.

So the lag-0 excursion is the sieve lattice looking at itself through the fixed
layer spacing, exactly the deterministic small-prime structure the pre-registration
excluded from counting as signal. Once alignment is matched, real ≈ null. And the
max-over-all-lags statistic, which absorbs alignment entirely, is null for every j.

## 3. Where the max lands

Both real and null maxima occur at small positive lags (noise alignment of the
dominant 2- and 3-lattices) or near ±(W−50k..W−1M) (boundary-overlap lags where the
unit-norm normalization lets partial-overlap dot products spike). Both populations
show the same two clusters. Nothing layer-specific.

## 4. Verdict

**NULL.** The retained-structure axis is closed with data.

- No cross-layer correlation at any separation j = 1..15 or any lag beyond the
  deterministic small-prime base: all 15 real max-|corr| statistics lie inside the
  20-pair null envelope (quantiles 0.05–0.70, none exceeding the null max).
- No lag-0 predictivity beyond small-prime alignment: the one apparent excursion
  (j = 3, |corr(0)| = 0.218) is reproduced and exceeded by alignment-matched null
  pairs (mean 0.234), i.e. it is the sieve lattice, not retained wave structure.
- Combined with theorem A2 (phase law = pure odometer) and Phase 2 (spatial stats
  at/inside null envelope): the wheel's band content carries no exploitable
  cross-layer or spatial information beyond ω_small's deterministic construction.

A measured null was the pre-registered, expected outcome; this axis is closed
permanently unless new theory proposes a mechanism that survives A2 + Phases 0.5–3.

## 5. Reproduction

- Script: `lab/phase3_run.py` (sieve, ω computation, FFT correlations, null pairs,
  envelope + quantiles; total runtime ~12 s, CPU only).
- Lag-0 alignment diagnostic: conditioned nulls D%42, D%120, seed 777 (inline in
  analysis; numbers recorded in PHASE3_results.json).
- Key numbers: `lab/PHASE3_results.json`.
- Layer band reference (matches Phase 2): layer 1,500,000, N ∈
  [1,124,999,701,425, 1,125,000,750,000], mean ω_small 2.8917.
