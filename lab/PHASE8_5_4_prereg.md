# PHASE 8 — pre-registered extension of the 5:4 half-turn density law to m = 10⁶

Date: 2026-10-11. Artifact: `lab/PHASE8_5_4_run.py` (run it to reproduce every
number below; CPU only, sympy, ~10–30 min with multiprocessing). No other files
touched. This phase converts the morning's Bateman–Horn observation from
"heuristic and measurement agree at m ≤ 20,000" into a **frozen prediction,
then a measurement**, exactly the D8/PHASE7 witness protocol.

## 1. The observable (frozen definition, identical to the verified one)

Ratio 5:4, `L[m] = max(1, round(5m/4))` (half-up, as `(10m+4)//8`),
`B[m] = Σ_{j<m} L[j]`, half-turn position `n = B[m] + L[m]//2` on layers with
`L[m]` even. Counted: `n` prime, over `1 ≤ m ≤ 10⁶`. Eligibility filter
(verified invariant to m = 20,000 this morning): primes occur only at `m = 8`
or `m ≡ 6, 13 (mod 16)`. The `m = 8` value (`n = 41`) is deterministic and
counted separately.

The two live families, parity-filtered forms in `u ≥ 0`:

    m = 16u+13:  g13(u) = 160u² + 262u + 107
    m = 16u+6:   g6(u)  = 160u² + 122u + 23

## 2. The prediction (written BEFORE the run)

Singular series per family (exact rational product, all primes p < 300,000,
ρ brute-verified against the Legendre formula; ρ(2) = 0 since both forms are
identically odd — the p=2 factor is exactly 2; ρ(5) = ρ(41) = 1):

    C = 4.499267368…        (both families; identical ρ(p) — shared discriminant 164 = 4·41)

Logarithmic sums to `u_max = 62,499` (both families have the same u-range at
m ≤ 10⁶): S13 = 2503.737, S6 = 2503.907.

| # | Prediction (frozen) | Tolerance / stop condition |
|---|---|---|
| 1 | Total primes m ≤ 10⁶: **22,532** (C·(S13+S6) + 1 = 22,531.7) | measured/predicted ∈ **[0.98, 1.02]** |
| 2 | Family split: c13 ≈ 11,265, c6 ≈ 11,266 | each within ±3% of its prediction |
| 3 | Eligibility filter: zero primes at m ∉ {8} ∪ {m ≡ 6,13 (16)} | any violation → halt, report raw list |
| 4 | Ratio at the m ≤ 20,000 baseline recomputed by the same script: 662 measured vs 662.6 predicted (0.999) | script self-check; failure = bug, not physics |

Stop conditions: filter violation (pred 3) halts immediately; ratio outside
[0.97, 1.03] is recorded as a MISS with the exact count, no re-tuning of C
after the fact. If the ratio lands outside [0.98, 1.02] but inside
[0.97, 1.03], the entry is recorded MARGINAL with the deviation in σ
(Poisson σ ≈ √22532 ≈ 150).

## 3. Provenance and caveats (mechanism labels)

- [E] Hardy–Littlewood/Bateman–Horn singular series for admissible
  quadratics; calibration on n²+n+41 gave brute C = 6.6458 vs empirical
  6.5686 at U = 1249 (the often-quoted 3.3 is the odd-prime product; the
  full constant includes the p = 2 factor 2, as here).
- [S] The two families are admissible (no local obstruction), verified
  directly: ρ(p) < p for all p < 200.
- [G] Bateman–Horn itself is unproved; this phase tests whether the wheel's
  measured density tracks the singular series out-of-sample, not whether
  either is a theorem. A MISS would mean the 3-digit match at 20,000 was
  small-sample luck or a horizon-dependent bias; either way it is data.
- The discriminant is 164 = 4·41, a non-maximal order of Q(√41). Whether a
  Rabinowitsch-type theorem governs positive-discriminant forms is [G] and
  unaffected by this run.

## 4. Result

(pending — filled by lab/PHASE8_5_4_run.py)

## 4. Result (filled by lab/PHASE8_5_4_run.py)

Wall: 4s on 12 workers. C recomputed in-run: 4.499267368 (matches prereg).

| # | Prediction | Measured | Verdict |
|---|---|---|---|
| 1 | 22,532 total, ratio in [0.98,1.02] | 22506 primes, ratio 0.99886 (-0.17σ) | HIT |
| 2 | c13 ≈ 11,265, c6 ≈ 11,266 (±3%) | c13 = 11175 (-0.80%), c6 = 11330 (+0.57%) | HIT |
| 3 | zero filter violations | 0 violations | HIT |
| 4 | baseline self-check 662 vs 662.6 | 662 vs 662.6 | HIT |
