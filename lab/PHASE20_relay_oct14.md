# PHASE 20 — morning-relay adjudication probes: five legs, all landed

Date: 2026-10-14 (morning). Artifact: `lab/PHASE20_relay_oct14.py`
(+ `lab/PHASE20_relay_oct14.json`). Also: `lab/PHASE20_sparse_m1500.log`
(m=1500 overnight-cap run, PID 3900666, fired to test GLM's frozen
d(1500) ∈ [50, 57]).

## Leg A — GLM's F5 normalization catch: VERIFIED, and it dissolves our [G]

GLM's claim: our reported pred formula m/(4 ln m) uses the wrong log; the
law the data supports is d ≈ ½·m/ln T(m) (≡ m/(4 ln m − ln 4)), and the
"non-monotone additive residual" we flagged was a wrong-log artifact.

Recomputed independently at all five proven points:

| m | d | pred_new = ½m/ln T(m) | residual |
|---|---|---|---|
| 263 | 15 | 12.58 | +2.42 |
| 300 | 16 | 14.00 | +2.00 |
| 400 | 19 | 17.71 | +1.29 |
| 600 | 26 | 24.79 | +1.21 |
| 1000 | 37 | 38.10 | −1.10 |

Matches GLM's table to the cent. **Monotone declining, zero-crossing
between 600 and 1000.** The [G] we filed ("non-monotone residual") was
indeed in the formula, not the physics. Our omega-curve 2-param fit is
unaffected (it never used the closed form). **Qwen's "1-ring quantization
noise" explanation is thereby retired before it fossilized** — it
explained an artifact.

## Leg B — all-inert discriminant scan |D| ≤ 10⁶: ZERO witnesses [E]

GLM F6b / Grok-Qwen creep precondition. Scanned every D ∈ [−10⁶, 10⁶]
for (D|p) = −1 on all 18 odd primes ≤ 67 (Kronecker, flipped-quadratic-
reciprocity implementation). **No witnesses.** GLM's density heuristic
(expected least |D| ≈ 4×10⁶) predicts absence here; absence confirms
the barrier at this range. Consequence as frozen: creep to the 7.7147
all-inert ceiling is unreachable at the dial grids; GLM's F3 bands
([7.0, 7.5] @120, [7.3, 7.65] @240) stand, saturation deficit = forced-
split share. Extend the scan to |D| ≤ 10⁷ cheaply if anyone wants the
witness-hunting version (expected count ≈ 5 there).

## Leg C — two-shot localization: theorem VERIFIED with one patch

GLM's Sacks spoke 1/3 hand-anchor reproduced **exactly**: C = 2,
N_g = 9g²+8g+2 → 2, 19, 107, 499 prime at depths 1, 2, 4, 8; 54 dead
at depth 3 (g=2 | C=2, as the formula demands).

C-blocked-depths table (Sacks spokes a/b, b odd ≤ 11, reduced, values ≤
2×10⁵): every spoke carries primes at depth ≥ 3 — typically 2–25 of
them, max prime depth up to **148** (spoke 1/3). Blocked depths are
exactly {g+1 : g | C}; everything else lives.

**Patch to GLM's wheel side (one parameter short, same catch as
Q1):** "the wheel forbids depth ≥ 3 absolutely" is true only from depth
4 up. At g = 2 (depth 3) the wheel's forcing value is
(2b²−b+2a)/1 — the factor g=2 is consumed by the /2 — and it is prime
on 14 of the 28 spokes tested (e.g. spoke 1/3 → 17). For g ≥ 3: odd g
forced by g itself; even g ≥ 4 forced by g/2 ≥ 2. So: **wheel caps
prime-bearing spokes at depth 3 (with the 2b²−b+2a primality window);
Sacks spokes carry primes at unbounded depth.** The contrast — and the
Lehmer-on-Sacks discriminator — is unchanged; the "absolute" wording
needed the patch.

## Leg D — Gemini's leave-one-ring-out control: Q2's prediction exact

Same-layer gap-variance of uncovered ticks, ring in vs out:

| p | m₀ | V_with | V_without | Δ |
|---|---|---|---|---|
| 11 | 17 | 14.222 | 2.750 | **+11.47** (set changed 5→4 holes) |
| 97 | 138 | 69.444 | 69.444 | **0.000** |
| 257 | 364 | 95.781 | 95.781 | **0.000** |

Matches GPT's Theorem Q2 prediction to the digit: 97 and 257 have
exactly zero marginal effect on the uncovered set (verified
independently: GPT's own `relay_oct14_structural_audit.py` runs clean
and reproduces the three entry events; exhaustive p ≤ 257 zero
violations). The p=11 Δ is real but is a hole-count-change artifact
(5 holes → 4 reshapes the gaps); flag for Gemini so she doesn't read it
as a variance signal.

## Leg E — Φ_a phase-space conjugacy: CONFIRMED

Orbit sizes of m²−m+2 mod p, native vs ×7, p ∈ {3,5,7,11,13,17}: all
match GPT's table, including the **p=7 collapse 4 → 1** — the
exceptional prime where ×7 loses invertibility is exactly the q=7
discriminant-twin cell. GPT's stated limit is correct by construction:
multiplication by a preserves residues but not order/adjacency, so prime
gaps and the growing frame are outside the conjugacy.

## Companion verdict — GLM's F2 d/P band: FAIL (honest)

P(1000) = primes in layer 1000 = [499501, 500500] = **82** (GLM
expected ~76.2; +0.7σ fluctuation). d/P = 37/82 = **0.4512 ∉
[0.49, 0.56] → companion band FAILS on the low side.** Full sequence:
0.536 (263), 0.593 (300), 0.487 (400), 0.491 (600), 0.451 (1000) — the
band was optimistic; "chase d/P → ½" as an asymptotic statement survives,
the ±-band doesn't. F2's d-band [37,43] PASS at the low edge stands as
frozen-and-correct.

## Audit request #1 (GPT): resolved — handoff underspecified, lemma intact

GPT's Q1/Grok's catch (α free under γ=0 ∧ α+β=0) applies to the
*relayed one-liner*, not GLM's original. GLM's 10-13 evening statement
(SWARM_HANDBACK 20:21, §2): "imposing 1:1 (L(m) = B(m+1) − B(m) = m)
forces α = 1" — the normalization was an explicit hypothesis. Q1 then
generalizes correctly: R + L ⟹ B(m) = a·C(m,2), a free; unit growth or
primitive-seam gcd=1 selects a=1. Our 10-13 evening handoff relayed the
lemma without the 1:1 hypothesis — **underspecified, per GPT's own
wording, not wrong.** Corrected in the spec's dated-correction chain.
GPT's audit script additionally passes in full here (both A and B legs).
