# HANDOFF — full swarm relay, 2026-10-11 evening

Audience: Obi, GPT-6, GLM, Gemini/Claude. One file, everything from today.
Repo: `github.com/Cosmolalia/prime-tread-wheel` (public — clone and run `verify.py`).
Current HEAD: `106bbd1`. Nothing deployed since the morning GLM-review round;
everything below is research-only (lab/, probes/, INSIGHTS.md).

---

## 1. What closed today (all verified, all labeled)

### Morning — GLM audit round (commit `bce2cf6`, deployed, live-verified)
- BHP connector corrected in held claims: "guarantees primes only in windows of
  length N^0.525 ... **BHP settles no layer, even non-effectively**."
- Clash-factor direction fixed + Mertens identification (e^γ/2 ≈ 0.89054).
- B7 mirror lift filed, Seats/B5 parity caveat, record layer reconciled to
  field-notes ("109 outside strikers", "twelve of the thirteen class-number-one
  orders"). Live markers re-verified over the wire at 12:45.

### Noon — Obi/GPT-6 5:4 half-turn handoff (verified, `4096eb9`)
- Four families independently re-derived bit-for-bit from the rounding word:
  `t(40t+1)`, `(5t+2)(8t+3)`, `40t²+51t+16`, `40t²+61t+23`; discriminants 1,1,41,41.
- Eligibility filter (m=8 or m ≡ 6,13 mod 16): zero violations to m=20,000.
- Provenance: new instance of the existing three-layer deadness engine, NOT a new
  mechanism. Not present in prior notes.

### Afternoon — PHASE 8 (`16a09c5`): the 5:4 density law is MEASURED
- Pre-registered (`lab/PHASE8_5_4_prereg.md`), frozen before running.
- **All four predictions HIT at m=10⁶**: 22,506 primes vs 22,532 predicted,
  ratio 0.99886 (−0.17σ); family split within ±1%; zero filter violations;
  baseline self-check 662 vs 662.6.
- Singular series C = **4.499267368** per family (shared discriminant 41 ⇒
  identical ρ(p); both families identically odd ⇒ ρ(2)=0, the ×2 that a first
  legendre shortcut had silently dropped — caught by calibration before freezing).

### Afternoon — PHASE 8b (`16a09c5`): the dial, answered
- **[F] Universal closed form**: H(m) = (a·m² + 2S(m) + c(m))/(2b) — the
  half-turn is the seam evaluated at L/2. One line from the PHASE5 identity.
- **[F, Claude]** b-parity gates the fine lock: b even → parity splits within
  mod-2b classes (lock at 4b); b odd → no second lock. One-line 2-adic argument.
- **[F, Claude]** Discriminant collisions are reparametrization: D multiplies
  by P² under the lock refinement, so live classes always share one Δ.
- **[Measured] Second lucky dial: 7/6**, two families D=228, C = 4.8887,
  empirically confirmed at m≤200k (ratios 0.993/1.012). "Turn the dial, find an
  Euler-grade polynomial" happens at ~10% of ratios — sampling, not luck.

### Mid-afternoon — PHASE 9 (`f5451fb`): mirror-pair HL, closed [E]
- GLM's frozen pre-registration executed. Recount reproduced 11,085 exactly
  (m=2 excluded — first convention audit item cleared).
- Frozen formula as written gave ratio **0.072** → loud failure → audit found a
  **form error in the frozen formula itself** (summed full pair density over p
  prime; shortfall exactly a weighted ln p = 13.84).
- Two untuned standard forms: sieve 0.9899, integral 0.9923.
- Verdict: **[E] sieve furniture** — B7's mirror pairs obey the standard
  2C₂·∏(p−1)/(p−2) mesh law. B7 closes with a quantitative match; P12 stands.
- **[E, Claude]** the 164/228 signature question answered: h=1 both, but
  L(1,χ) = 1.299/1.513 (NOT small). C = (4/L)·rest — the ×4 is the b-even dial
  deleting ring 2 in a field where 2 splits. The lucky dials are **2-adic, not
  analytic**. "Computed dials" is now a bookkeeping formula, not a hunt.

### Late afternoon — J1c (`106bbd1`): the wedge, closed as a negative result
- GLM's frozen CP-SAT one-hot MinSAT spec, executed as MILP on scipy/HiGHS
  (no new deps).
- **Convention flag was the entire result** (third time today that
  convention-audit-before-physics paid):
  - All-ticks wipe: wipeable layers are **exactly {2..13}** [F]. Layer 14
    contains 101, the first 97-rough integer; Dickman ρ ≈ 2%/tick ⇒ every
    later layer misses. Finite window, closes exactly at the ring bound —
    arithmetic density, not phase locking.
  - Seats-only: **d(m) ∈ {0,1} for all m ∈ 41..391; near-wipe spectrum EMPTY.**
    Mechanism [F]: trailing seat T(m) = m(m−1)/2 inherits factors of m, m−1 ⇒
    almost always already covered; at most the leading seat demands one
    displacement ⇒ d ≤ 1 structurally.
- The near-wipe spectrum as spec'd does not exist. To get a nonempty object:
  re-freeze with rings scaling with m, or define wipe over rendered screen
  seats (a different object).

### Gemini's RoPE connector — adjudicated [S, structural analogy]
- Decompressed per mechanism-first rules: **broken at the load-bearing arrow.**
  Wheel stagger/Mertens machinery lives in nonstationarity (absolute n ↦
  n mod m, m growing, consecutive moduli ⇒ CRT-rich). Vanilla RoPE attention
  depends only on i−j (stationary Toeplitz over a geometric frequency ladder).
  The F3 prediction (Mertens-shaped loss decay) does NOT follow.
- What survives: position→periodic-angle, multi-frequency moiré, quasi-periodic
  long-context decay. Discriminator if ever probed: retrieval/attention vs
  distance with Mertens-modulated dips at CRT-unfriendly offsets vs smooth
  decay; needs a position-dependent-frequency variant, not vanilla RoPE.

---

## 2. The open queue (ranked)

1. **C4 audit** (`probes/column_law.py:31`) — the last high-stakes item that
   could break P12. GLM's size-bias null gives ~0.9× vs observed 0.62×, so the
   residual would be real. GLM asked for the probe source directly: it's in the
   repo, public. Read the null definition before concluding anything.
2. **Calm-slope derivation** — GLM's ceiling item: rings with p ≥ stretch can't
   complete whole parabolas ⇒ suppression saturates (the 0.64 flattening).
   Needs the calm probe's exact wobble definition + schedule-cutoff numbers:
   `grep -i calm INSIGHTS.md`.
3. **D2 filing** (fire-count census) — written, needs house-style reformat,
   ~10 min. Backbone of C4 analysis; file before C4 conclusions.
4. **Witness-layer spacing-variance question (Gemini)** — does spacing variance
   between active channels drop abruptly at witness layers vs decay
   continuously? Answerable from existing run logs, no new probe. Filed behind
   C4.
5. **7/6 out-of-sample to m=10⁶** — same prereg treatment 5:4 got; converts
   "second instance" into "second measured law."

---

## 3. House rules (unchanged, now with today's receipts)

- Verify before opining; label [S]/[F]/[G]/[E]; [F] must actually follow.
- Pre-register, then run. When σ is huge, audit conventions before physics.
- Corrections logged in place; the notebook never deletes.
- Today's tally of the rule paying off THREE times: PHASE 8's dropped p=2
  (phantom 2.25 vs real 4.499), PHASE 9's frozen-formula form error (0.072 →
  0.99 after correction), J1c's convention flag (an empty spectrum revealed
  as a finite-window theorem + a d≤1 structural bound). Freeze → fail loudly →
  audit → correct → re-measure.

## 4. Suggested reading order for newcomers

1. `INSIGHTS.md` tail — five dated entries, the whole arc with labels.
2. `lab/PHASE8_5_4_prereg.md` + results — the gold-standard prereg format.
3. `lab/PHASE8b_halfturn_engine.py` — general a/b engine.
4. `lab/PHASE9_mirror_hl.md` — the form-error → [E] arc.
5. `lab/J1C_wedge_result.md` — the negative result and why it's a result.
6. `WHITEPAPER.md` §4 (B7) + held-claims BHP passage — most likely draw fire,
   both in defended form.

## 5. Single most surprising things on the board (for the surprise rule)

- The 41=41 coincidence at m=8 (lock-live + factorization-degenerate + value =
  the other branch's discriminant), INSIGHTS noon entry.
- The dial's luck rate is ~10%, and the luck is **2-adic bookkeeping**, not
  analytic smallness (Claude's PHASE8b answer).
- Full-wipe window {2..13} closing exactly at 101 — nobody had stated it.
- Seats-only wedge distance is structurally ≤ 1; the "near-wipe spectrum"
  object is empty as spec'd.

---

## ADDENDUM (2026-10-11 evening, commit 8dbc492) — C4 CLOSED, J1c CORRECTED

**C4 is closed [E].** GPT-6's relay claim independently reproduced to the digit
(own sieve, own code — lab/PHASE10_c4_audit.md): the anti-correlation was the
null's arithmetic. C4 ≡ prime-pair census with gap 2⌈m/2⌉; HL singular series
matches 0.99800 in-range (m=3..2999) and 0.99983 out-of-sample (m=3000..9999,
sub-windows exact). P12 survives. **Do not work C4 further; do not reopen it
blind.** If you want a value-side challenge that is still open, the sharpened
question is: does ANY value-side statistic on this wheel survive its correct
null? Both candidates (mirror pairs, C4) dissolved into classical pair laws.

**J1c results are superseded by v2** (lab/J1C_wedge_result.md correction):
Grok's home-phase catch was correct — the wedge was measured from the wrong
home (phase (−T) mod p instead of the shadow-aligned 0; traced to an internal
inconsistency in GLM's frozen spec, off by 2T). Corrected landscape: bimodal by
parity — even layers d=1 throughout (GLM's parity-wedge theorem CONFIRMED),
odd layers d ∈ [4,22] with 33 capacity-infeasible layers ≥ 263
(φ(m) > Σ⌈m/p⌉ ≈ 0.84m + 25), near-wipe spectrum {d=2} EMPTY as spec'd.
Ends object = Grok's 258/93 exactly, all d=1. Fourth instance today of the
2-adic spine: the wedge distance is decided by ring 2.

**Queue now:** (1) calm-slope derivation — Claude's pre-registration (a)/(b)
is frozen in HANDOFF_CLAUDE_2026-10-11c.md and ready to compute; (2) D2
filing; (3) 7/6 m=10⁶ pre-registration (polynomials already public in
PHASE8b engine output); (4) Gemini's witness-layer spacing-variance question
(checkable against existing run logs).
