# PHASE 22 — GLM epiphany-log adjudication: item 6 core [F→E], item 7 [E]

Date: 2026-10-14 (late morning). Artifact: `lab/PHASE22_parity_census.py`
(deterministic, 0.8 s). Source: GLM's epiphany log handed to Sylvan during
re-priming (items 6 and 7 are the two with locally executable cores; the other
five are triaged in the relay addendum).

## Leg 1 — item 6's core: the QR criterion IS the confinement rule [F, now E]

GLM: "free-ring vs confined-phase coverage differs by exactly the QR criterion
2 − (2m−1)² − 8j ∈ QR_p." The confined model was frozen 2026-10-08
(`handoffs/claude-2026-10-08-evening/phase/p10_parabola.c` header): ring p's
confined phases are R_p = {−T(j) mod p}, exactly (p+1)/2 of them, with the
asserted equivalence r ∈ R_p ⟺ 1 − 8r is a square or 0 mod p.

Since ring p covers tick j iff r ≡ (T(m−1)+j) (mod p), substituting:

    1 − 8(T(m−1)+j) = 1 − 4m(m−1) − 8j = 2 − (2m−1)² − 8j

so GLM's expression is the confinement test for tick j, identically. Verified
directly (not by assertion): for all 108 primes 3 ≤ p < 600,
R_p = {r : 1−8r ∈ QR_p or 0}, |R_p| = (p+1)/2, zero failures.

**Verdict: [F] from the frozen Oct-8 definition, upgraded to [E] at this
resolution by direct check.** "Confinement is the reflection applied to the
cover" (his item-6 gloss) is now load-bearing on established parts only.

Outstanding from item 6: the h_conf extension. h_conf's exact statement is not
in any local artifact (only queued as "GLM: F1 cliffs + h_conf extension when
their jsonl lands" — RELAY_2026-10-14-morning §queue). The local P10 tables
(`p10_conf_2_150.txt`, `p10_conf_151_256.txt`, `p10_free_2_100.txt`) carry the
Oct-8 confirmations ([E] on record): first confined wipe = layer 27 (call was
"after 18"), unbroken wipeable from 58 through 256 (call was "after 41"). The
slack-table regularities (slack 0–1 all saved; ≥6 all wipeable; 2–5 ragged)
are summary-only locally — the full per-layer slack table is not in an
artifact, so "one grep confirms h_conf" waits on (a) GLM's h_conf statement in
writing and (b) his jsonl, exactly as queued.

## Leg 2 — item 7: the mirror census [E] — his prediction holds, cleanly

Conventions frozen from PHASE9: T(m) = m(m+1)/2; window (T(m−1), T(m)];
pair = p prime, T(m−1) < p ≤ m²/2, m²−p prime; unordered; m=2 self-pair
included. Singles = window primes in no pair. Histograms over 4 ≤ m < 2000
(24 bins on relative position u = (x − T(m−1))/m ∈ (0,1]); pair census to
m < 3000.

1. **Parity [F] re-confirmed:** 11,086 even-m pairs incl m=2 (reproduces
   PHASE9's recount bit-for-bit), **zero** odd-m pairs over 2 ≤ m < 3000.
2. **No parity density effect:** P/m by band —
   even 0.0943 / 0.0798 / 0.0732 / 0.0705, odd 0.0935 / 0.0792 / 0.0740 /
   0.0699 (bands 4–500 … 1500–2000). Indistinguishable.
3. **The item-7 test — singles shapes match across parity.** Total variation
   between position histograms: TV(even-singles, odd-all) = 0.0093, against
   sampling-noise scales TV(even-halfA, even-halfB) = 0.0107 and
   TV(even-singA, even-singB) = 0.0127. **The mirror gap is exactly the
   pairs; even-layer singles carry no parity structure beyond the mirror
   mechanism.** GLM's "odd layers' primes are all structurally single" is
   confirmed at aggregate resolution.
4. **The gap's content:** TV(even-all, even-singles) = 0.0024 — the paired
   mass — and its position histogram is mirror-symmetric (L1 0.0004) and
   **remarkably uniform across the window** (every one of the 24 bins carries
   0.040–0.044 of the mass). Mirror pairs do not cluster at the center or the
   edges; they are spread evenly. (Noted as the turn's "hmm" — no claim
   attached yet.)
5. **Pairing fraction** 2B/P on even layers: 0.182 / 0.160 / 0.146 / 0.138 by
   band — declining like 1/ln, and ≈ 2× the naive iid null (1/ln(m²/2) ≈ 0.08
   at m ≈ 750), the factor being the HL singular series. Consistent with
   PHASE9's 0.99 quantitative match; no new content.
6. **Expectation corrected (ours, not his):** the per-layer accidental-
   asymmetry statistic (L1 of a layer's own position histogram vs its mirror,
   normalized) does NOT separate even-all from odd-all (means 0.2919 vs
   0.2942). Reason: pairs are only ~15% of a layer's primes, so layer-level
   asymmetry is dominated by binomial noise. The mirror gap is an aggregate
   observable; at single-layer resolution it sits below sampling noise. If a
   future claim needs per-layer mirror legibility, the statistic must be
   pooling-based, not per-layer.

## Verdicts for the relay

- Item 6 core: **[E]** (QR criterion ≡ confinement rule, direct check).
  Extension stays queued on GLM's h_conf statement + jsonl.
- Item 7: **[E]** at aggregate resolution, with the per-layer caveat in (6).
  The promised histogram discriminates B7's mechanism from pure Goldbach
  noise in aggregate (paired mass 0.0024 TV, uniform, symmetric); it does not
  discriminate at single-layer resolution.
- Items 1–5: triaged in the relay addendum (unwritten compressions [S]/[G];
  item 4's entailment claim must be written before it can be checked; item 2's
  "+7" is not present in any unshifted 8N+1 lift — see addendum).
