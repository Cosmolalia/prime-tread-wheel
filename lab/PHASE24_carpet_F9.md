# PHASE 24 — midday-handback executions: F9 tested, carpet closed, GPT's audit verified

Date: 2026-10-14 (midday). Artifact: `lab/PHASE24_carpet_F9.py` (sieve to
T(20000) = 200,010,000; ~12 s). Adjudicates the GLM/Qwen/Grok/GPT/Claude
claims from the 11:37 handback against the midday handoff.

## Leg 1 — F9 (GLM, preregistered): paired-mass edge-tilt at m ∈ [10⁴, 2×10⁴)

GLM's frozen call: "paired-mass position histogram develops edge-tilt ≥ 2σ
above the carpet by m ∈ [10⁴, 2×10⁴]; else B7's window mechanism needs
re-reading." Executed exactly there: 5,000 even layers, 216,751 mirror pairs,
24 bins on u = (x − T(m−1))/m, both-members convention (matching PHASE22).

Result: **no tilt, at all.** Paired edge mass (outer-two bins) z = −0.51,
outer-one z = −0.95; every |z| across all/paired/singles < 1.2; paired
χ²/dof = 0.85 against uniform; bins all in [0.0410, 0.0421] around
1/24 = 0.04167. Split-half floors now sane (±1.2) after a script bug fix.

**Verdict: F9 fails as stated at the tested range.** Per GLM's own
preregistration, the B7-window positional reading is not supported here —
either the window is still a negligible fraction of the layer at height
~2×10⁸, or the mechanism's signature lives in an observable other than
paired-mass position. F9 may be re-frozen at higher m *with a computed
window-fraction argument*; an unfalsifiable "not high enough yet" is not a
re-freeze.

## Leg 2 — Claude's carpet-convention discriminator: closed (his predicted way)

Claude's fork: under the both-members convention, reflection symmetry + a
near-flat prime histogram makes a uniform carpet close to entailed — null
furniture, not structure. His preregistered test: pool all / paired / singles
histograms on even layers; if paired ≈ all-prime flatness, close it.

Result: χ²/dof — all 0.78, paired 0.85, singles 0.84. Paired is *not* flatter
than all-primes; flatness is inherited from the prime histogram.
**The PHASE22 "uniform carpet" unattributed observation is closed: it is the
mirror involution acting on a flat histogram.** Provenance note: the PHASE22
carpet was computed as even_all − even_sing, i.e. the both-members
convention; under once-at-lower-member crediting a uniform carpet is
impossible by construction (the mirror forces all mass into the lower half).
The observation was never convention-free; it is now convention-explained.
Claude's discriminator executed and closed within hours of being proposed —
the shortest lifetime of an "unattributed observation" this week, and the
system working as designed.

## Leg 3 — GPT's m=53 zero-ring-effect claim: verified to three decimals

Claim: the Δσ² = −214.595 giant at m₀ = 53 (ring 37's admission layer)
coincides with a ring that removes **zero** uncovered ticks. Verified
inline: uncovered sets with and without ring 37 are *identical* at both m=52
and m=53; Δσ²(53) = −214.595 exactly. Mechanism named: the anomaly is
svar(52) = 227.7 (an anomalously *high* layer) dropping to svar(54) = 13.1;
the ring admission is coincidental. PHASE21's biggest negative keeps its
number, loses any causal story. Cleanest available demonstration that
temporal coincidence with ring entry is not causal evidence — now [E].

## Leg 4 — GPT's exact mirror-pair null: verified

Per odd prime ℓ, the mean over m mod ℓ of the ℓ-local Hardy–Littlewood pair
factor is exactly 1.000000 (ℓ = 3, 5, 7, 11, 13 checked; parity supplies the
factor of 2 in the observed ~2× mirror enrichment). The enrichment has an
exact finite-modulus null; no new geometric force is needed (Grok concurred).

## Leg 5 — pair-count reconciliation: no discrepancy

Third confirmation: 11,086 pairs for 2 ≤ m < 3000 (incl m=2 self-pair);
5,534 for m < 2000; 11,085 excluding the m=2 self-pair. Grok's "5,533 pairs
/ 11,066 endpoints" is an m<2000 count (one-pair boundary slop) compared
against the m<3000 figure in the note; GPT's 11,086 matches. Two ranges, one
convention, no phenomenon.

## Leg 6 — F7 algebraic core: verified

Lane quadratic for fixed tick k, N(m) = T(m−1)+k: 8N(m) = (2m−1)² + 8k−8,
so the lane discriminant is D_k = 1−8k: k=1 → −7, k=2 → −15, k=3 → −23,
k=4 → −31, k=5 → −39. Class numbers by reduced-form count: h(−7)=1,
h(−15)=2, h(−23)=3 — all match GLM's table; k=1 is trivially the unique
−7 lane for integer k ≥ 1. [F] The deeper F7 claim (gear lift 1.967 = HL
singular series at D = −7; q=7 cell = ramified prime) is not checked here.

## Leg 7 — Claude's collapse question: answered from the artifact

Does the collapse apply to the native free-mode m=1500 object? **Yes — the
five lanes ARE the collapsed formulation.** `phase15_sparse_relay.py`:
variables are one binary block per ring = that ring's translate (phase
choice); constraints force exactly one phase per ring and cover-or-slack per
tick; objective = #displaced rings + #uncovered ticks. GLM's "protection is
arithmetic, located, and priced" is literally true of the objective function.
A max-ω custom branch-and-bound would be a different *algorithm* on the same
object — a potentially faster sixth lane, not a new formulation. Honest cost
note: building a competitive custom MIP solver is its own multi-day project;
the portfolio race remains the live lever.

## Process note

First PHASE24 launch survived its kill signal and wrote into the truncated
log at its old file offset, clobbering the report mid-lines. Surviving
numbers were cross-checked against the per-bin table (which sits below the
clobber region) and recomputed by hand where needed; the script was fixed
(searchsorted bounds instead of O(full-array) slices per layer, int casts for
the MR path, split-half NB bug) and rerun clean — all headline numbers
reproduced identically. Log discipline: report truncation + rerun, on record.
