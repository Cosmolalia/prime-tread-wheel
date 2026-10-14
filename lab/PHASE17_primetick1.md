# PHASE 17 — #18 prime-layer seam-lock check: PASS, with two honest footnotes

Date: 2026-10-13 (late afternoon). Artifact: `lab/PHASE17_primetick1.py`
(+ `.json`, `.log`). Spec: Claude's insights handoff #18 (13:29 relay).

## The mechanism, decompressed [F]

On the native 1:1 wheel, the L-build seam-locks ring q to its own layer:
phase j_q = T(q−1) ≡ 0 (mod q). Ring q therefore hits tick 1 of layer m
iff T(m−1)+1 ≡ 0 (mod q) iff **m²−m+2 ≡ 0 (mod q)** — discriminant **−7**,
which is exactly why Claude's r_q = 1+(−7|q) had to be right. Predicted
hit rates: r_q/q over all layers; **r_q/(q−1) over prime layers** (m prime
excludes the class 0 mod q, and 0 is never a root since m²−m+2 evaluates to
2 there — all roots live in nonzero classes).

## Results (M_HI = 300k layers, odd q ≤ 97; frozen predictions P1–P4 in header)

- **P2 PASS, the cleanest**: prime-layer hit rates match r_q/(q−1) at
  |z| ≤ 0.46 on every prime with r_q ≥ 1. q=7 (degenerate discriminant,
  (−7|7)=0, single double root m ≡ 4 mod 7): emp 0.16658 vs 1/6 = 0.16667,
  z = −0.04. The bad-prime behavior from the dial census (p | discriminant
  ⟹ ρ(p) counts the collapsed root) shows up here in pure wheel form.
- **r_q = 0 primes (q ≡ 3,5,6 mod 7)**: empirical rate exactly 0 over
  ~280k composite + ~26k prime layers each. Zero-rate is exact, not
  statistical. 12 primes, 24 buckets, all identically zero.
- **P3 PASS**: prime/composite lift = q/(q−1) at every q
  (7/6 at q=7: lift 1.185 vs 1.1667 predicted-from-rates; 11/10 at q=11).
  Flagged in advance: this 7/6 is a statistical lift, not dial evidence.
- **P1 footnote (our frozen prediction, not the mechanism)**: composite
  buckets run low at exactly z = −3.37 (q=7) and −2.38 (q=11) — fully
  explained: the composite bucket is all-layers MINUS the prime layers, and
  the prime layers carry the excess. The predicted deficit
  (r_q/(q−1) − r_q/q)·f_prime/(1−f_prime) = 0.00227 at q=7 matches the
  observed 0.00225 to the third decimal. P1 as frozen mis-specified the
  composite expectation; corrected, every cell in the table is within
  |z| ≤ 0.46 of its proper prediction.
- **P4 (exploratory, frozen negative correlation) FAILS honestly**:
  mean layer prime count by tick-1 hit multiplicity: 552.9, 556.1, 550.6,
  562.6, 537.8, 605.7 (n = 9514, 7508, 2470, 453, 46, 7) — no monotone
  trend; high-hit buckets too small to read. Mechanistically expected:
  layer prime counts are phase-insensitive to first order (a ring's
  multiples-per-layer is ⌊m/q⌋ or ⌈m/q⌉ regardless of phase; the seam lock
  moves WHERE the multiples sit, not HOW MANY). So #18's statistical core
  (prime layers hit tick 1 more) is confirmed; "seam locking shapes what's
  on a layer" is NOT visible in prime counts — it would have to be tested
  in a phase-sensitive observable (e.g., positions/gaps of the surviving
  primes), which this probe did not freeze.

Free cross-check: every one of the 19,998 layers 3..20,000 holds ≥ 1 prime
[N1 re-verified on the native schedule from our own sieve; consistent with
the filed 1.8M count].

## Relay consequence

#18 upgrades from [H] to **[F/E]: the seam lock's arithmetic signature is
exactly as Claude predicted, including the degenerate q=7 cell.** The
layer-content extension stays [H] with a named next observable.

## Queue item P-TRI step 2 — filed as [G], NOT run

Claude's spec ("tie j ≡ m−1 mod small primes one prime at a time") is
well-posed, but the P-TRI #16 engine is not in this repo, and the two
reconstructions we can build from audited conventions both fail against
Claude's published numbers:

1. **Native-schedule + mod-q image reading** ("triangle-reachable phase" =
   {c : 8c+1 ≡ □ mod q}): provably wrong — the anchor a = T(m−1) is always
   phase-valid (8T(m−1)+1 = (2m−1)² is a square mod every q) and always
   avoids W_m mod Q, so EVERY layer is triangle-coverable. Contradicts the
   published added-infeasible set {19–21, 25, 29–33, 35–39, 42–44, 52}.
2. **Fixed-bound reading** (rings ≤ B₀=31, j(31#)=58): cannot host "53..500
   all covered" (free-phase infeasibility starts at 59; triangle-feasible ⊆
   free-feasible).

The u=0 witness (small wheel theorem, [F]: *the seam anchor is universally
triangle-consistent because 8T(m−1)+1 = (2m−1)²*) is worth keeping on its
own. **Question to Obi's side for the next handback** (one line): what are
P-TRI's exact window / ring-bound / phase-domain conventions? With those,
step 2 is an afternoon.
