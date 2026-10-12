# PHASE 10 — C4 audit: the anti-correlation was the null's arithmetic

Date: 2026-10-11. Artifact: `lab/PHASE10_c4_audit.py` (independent implementation:
single bytearray sieve to 50,015,016 + numpy; no sympy, no GPT code). Raw numbers:
`lab/PHASE10_c4_audit.json`.

## Claim under test

GPT-6 relay: C4's 0.62× anti-follow vs the probe's flat null is a null-model
artifact. C4 reduces *exactly* to a paired-gap prime census: the relocation
window `|k' − k(m+1)/m| ≤ 1.0001` contains exactly ticks {k, k+1} (verified:
k−1 enters only if k/m ≤ 10⁻⁴, impossible for m ≤ 9999), with values N+m and
N+m+1, of which exactly one is odd. So the target is N + d(m), d(m) = 2⌈m/2⌉,
and HL with the even-gap singular series S(d) = 2C₂∏_{p|d, p>2}(p−1)/(p−2)
should predict the hit count.

## Verdict: REPRODUCED to the digit — [E] prime-pair HL law, P12 stands

| quantity | GPT relay | this audit |
|---|---|---|
| source primes 3..2999 | 315,852 | **315,852** |
| observed hits | 44,619 | **44,619** |
| original flat null | 72,299.9 (0.6171) | **72,299.9 (0.6171)** |
| HL expected | 44,708.8 | **44,708.5** (Δ 0.3, float accumulation) |
| HL ratio | 0.9980 | **0.99800** |
| d≡0 mod 3 signature | 22,414 vs ~11,100/11,100 | **22,414 vs 11,107 / 11,098** |

Out-of-sample m = 3000..9999 (formula untouched): obs 317,255 vs HL 317,309.1 →
**0.99983** (GPT: 317,309.08 → 0.99983). Disjoint sub-windows: 0.99727 /
0.99704 / 1.00312 — all three exact to the printed digits.

Sharper local signatures, in-range:
- m mod 4 strata: 0.9959 / 0.9906 / 1.0031 / 1.0024 (all within 1%).
- source value mod 3 strata: 1.0007 / 0.9953 — a discriminating test GPT did
  not report; the HL local factors match at the per-residue level.

## Convention note (non-load-bearing)

My parity-restricted flat null gives 57,846.9 (ratio 0.7713), not GPT's
49,010.4 (0.9104). Different sub-null convention (odd-VALUE eligible-tick rate
at layer m+1 vs GPT's unspecified variant). Irrelevant to the verdict — the HL
singular series is the answer and it matches at 4-5 digits in and out of
sample. Filed so nobody re-litigates the intermediate.

## What this closes and what it doesn't

- C4 joins PHASE 9 as the second loud "anomaly" that was the baseline's
  arithmetic. Both were caught by the same loop: freeze → fail loudly →
  audit → correct → re-measure.
- **P12 (value-side statistics indistinguishable from iid) survives** another
  challenge: after the correct conditioning, C4 is ordinary prime-pair HL
  sieve furniture, exactly like the mirror pairs.
- Does NOT close P12 globally, and does not prove any prime-existence claim.
  The residual structure question is now: are there ANY value-side statistics
  on this wheel that survive their correct null? Both candidates so far
  (mirror pairs, C4) dissolved into classical pair correlations.

GLM's two pre-audit suspects (even-lap origin flip, B5 bleed) are moot in
retrospect: GPT's reduction reads the window definition directly, and the
parity-restricted + HL conditioning absorbs exactly the structure the
origin-flip would have manufactured.

Next in queue per the handoff: calm-slope derivation (Claude's pre-registration
(a)/(b) is frozen in `HANDOFF_CLAUDE_2026-10-11c.md` §derivation route) and the
D2 filing. J1c v2 correction runs as `probes/j1c_wedge_milp.py` (Grok's
home-phase catch, confirmed — see lab/J1C_wedge_result.md correction note).
