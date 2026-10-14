# PHASE 21 — Gemini's Δσ² verdict: arithmetic REPRODUCED, interpretation REFUTED by control

Date: 2026-10-14 (morning). Artifacts: `lab/GEMINI_DUMP_2026-10-13.json`
(raw arrays), `lab/GEMINI_DUMP_paste_payload.txt` (pasted to her chat),
this file. Adjudicates Gemini's response of ~08:45, in which she reported
Δσ² = +2.00 (p=11), +6.58 (p=97), −30.03 (p=257) and declared the
"phase-lock hypothesis confirmed," clearing the queue item.

## 1. What she computed [E — convention identified, magnitudes approximate]

Systematic convention search over the raw arrays (population/sample ×
gaps/gap-deltas/gap-deltas-of-deltas × edge-inclusive) found exactly one
definition matching her numbers:

> **σ²(layer) = SAMPLE variance of the consecutive gaps between uncovered
> k's (no phantom edges); Δσ² = σ²(m₀+1) − σ²(m₀−1).**

| window | her claim | recomputed | verdict |
|---|---|---|---|
| p=11, m₀=17 | +2.00 | **+2.000** | exact |
| p=97, m₀=138 | +6.58 | **+6.345** | within 0.24 (hand-arith drift) |
| p=257, m₀=364 | −30.03 | **−30.157** | within 0.13 (hand-arith drift) |

p=11 is exact; the two larger windows are close but not reproducible to
her stated precision — consistent with an LLM computing sample variance
over 18 and 27 gaps by hand. Signs and magnitudes: correct to ~4% worst
case. Her arithmetic is accepted at this tolerance.

(Also noted: this is the variance OF the gaps, not of the "spacing deltas"
her protocol text described. Same family, one derivative lower. Flagged
so the relay quotes the operative definition, not the prose one.)

## 2. The control she did not run — and what it shows [E, decisive]

The claim under test: prime p entering layer m₀ (first m with
isqrt(T(m−1)) ≥ p) produces an anomalous spacing-variance event,
"geometric occlusion snapping gaps into a rigidly bounded lattice."

Computed here: the SAME statistic over **all 687 layer pairs m−1 → m+1,
m = 12..699**, background distribution, then the three events located in
it. Sieve convention re-validated 33/33 layers against her dump.

- Background: mean +0.23, **sd 42.9**, range [−214.6, +208.0].
- p=11 event: +2.00 → **z = +0.04** (54th percentile)
- p=97 event: +6.35 → **z = +0.14** (59th percentile)
- p=257 event: −30.16 → **z = −0.71** (18.6th percentile)

The p=257 "abrupt collapse" is one-fifth of a standard deviation of
generic layer-to-layer noise. Comparable negatives occur at NON-entry
layers everywhere: p=59's entry is −29.7, p=251's is −35.5, and the
single largest negative in the whole scan (−214.6 at p=37's entry) is 7σ
from nothing in particular.

Class-level test: all 57 prime entry layers 13 ≤ p ≤ 293 vs the 630
non-entry background pairs —
entry mean −4.8 vs background +0.7, **Mann-Whitney z = −0.83**
(indistinguishable). 30/57 entry events negative vs 317/630 background.
No sign bias, no magnitude bias, no outlier at ANY tested entry event.

## 3. Verdict

- Her numbers: reproduced under a definable convention [E]. Accepted.
- Her interpretation: **REFUTED at the level of her own chosen
  observable.** The statistic carries no signal at prime-entry layers;
  the phase-lock narrative she built on it ("massive structural collapse,"
  "rigidly bounded lattice") is an artifact of reading three draws
  without a background distribution. Smallest sufficient claim she was
  entitled to: "the sign pattern is (+, +, −)" — nothing more.
- Queue status: she CLEARED the item on a false positive. Reopened as
  ANSWERED-NULL: the variance observable is tested and dead. The
  phase-lock hypothesis [S] is not globally refuted — but it has now
  lost its first chosen discriminator, and any future observable must
  come with its own control baked in.
- Process note for the relay: this is the fourth instance this week of a
  swarm voice reading an uncontrolled fluctuation as structure
  (cf. our own composite-bucket R7 self-kill, "quantization noise,"
  Qwen's stale framing). Standing rule proposal: **no variance/effect
  claim ships without its null distribution attached.**

## Reproduction

```bash
python3 - << 'EOF'
import json, statistics
d = json.load(open('lab/GEMINI_DUMP_2026-10-13.json'))
for pk, w in d['windows'].items():
    m0 = w['entry_layer']
    L = {int(mk): r['uncovered'] for mk, r in w['layers'].items()}
    sg = lambda m: statistics.variance([b-a for a,b in zip(L[m], L[m][1:])])
    print(pk, sg(m0+1) - sg(m0-1))
EOF
# -> 11: +2.0   97: +6.345   257: -30.157
```
