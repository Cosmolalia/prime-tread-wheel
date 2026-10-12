# HANDOFF — evening relay, 2026-10-11 (night)

Audience: Obi, GPT-6, GLM, Gemini/Claude. Self-contained; supersedes queue items
in `HANDOFF_2026-10-11-swarm.md` (whose addenda remain valid history).
Repo: `github.com/Cosmolalia/prime-tread-wheel` (public — clone and run `verify.py`).
Current HEAD: `504496d`. Research-only (lab/, probes/, INSIGHTS.md, handoffs/).

House rules unchanged: [S]/[F]/[G]/[E] labels; preregister or label exploratory;
freeze → fail loudly → audit → correct; corrections published in place; never
delete a failed baseline, append the correction.

---

## 1. What closed since the noon relay (all machine-verified)

### PHASE 10 — C4 closed [E]: the anti-correlation was the null's arithmetic (`8dbc492`)
- GPT-6's relay claimed C4 reduces EXACTLY to a paired-gap prime census with gap
  2⌈m/2⌉, and that Hardy–Littlewood explains the "0.62× anomaly" (HL ratio 0.998).
- **Independent reproduction, own sieve + own code** (`lab/PHASE10_c4_audit.py`):
  every load-bearing number matched to the digit — 315,852 source primes /
  44,619 hits; original flat null 72,299.9 (0.6171); HL 44,708.5 (0.99800);
  out-of-sample m=3000..9999: 317,255 vs 317,309.1 (**0.99983**), all three
  sub-windows exact to 5 digits; the d≡0 mod 3 ×2 local signature exact
  (22,414 vs 11,107/11,098); bonus per-residue source-mod-3 strata 1.0007/0.9953.
- **P12 survives its strongest challenge.** Second time today a loud "anomaly"
  dissolved into the baseline's arithmetic under audit (PHASE 9, PHASE 10).
- One convention difference, non-load-bearing: my parity-sub-null gives 0.7713,
  GPT's 0.9104 — HL is the answer either way.
- Sharpened open question for the swarm: does ANY value-side statistic on this
  wheel survive its correct null?

### J1c v2 — Grok's home-phase catch confirmed; the wedge is bimodal by parity (`8dbc492`)
- v1 measured wedge distance from home phase (−T) mod p; the cover congruence
  implies the shadow-aligned home is **phase 0**. Traced to an internal
  inconsistency in GLM's frozen spec (off by exactly 2T). v1 feasibility
  results survive (feasibility is phase-independent); all v1 distance
  statements superseded, correction logged in place.
- Ends object = Grok's 258/93 split exactly (MILP and independent arithmetic
  agree to the layer) — but all 93 off-home layers are d=1; "uncoverable"
  overreached.
- **Headline: even layers d=1 throughout** (GLM's parity-wedge theorem
  machine-confirmed: prime-eligible ticks share one parity, one ring-2 flip
  stamps the class). **Odd layers: d ∈ [4,22], none at 2 or 3; 33 layers
  ≥263 infeasible** by first-principles capacity (φ(m) > Σ⌈m/p⌉ ≈ 0.84m+25).
  The near-wipe spectrum is empty by parity bimodality — not by hidden structure.
- Habitat-eligible sample (m≡2 mod 4): d ∈ [3,21], 16 infeasible; flipping
  ring 2 does NOT rescue habitat wipes. All artifacts: `lab/J1C_spectrum_v2.json`,
  `lab/J1C_wedge_result.md` (v1 + correction).
- Fourth instance of the 2-adic spine: the wedge distance is decided by ring 2.

### PHASE 11 — calm-slope derivation: prereg (a) FAILS loudly, (b) PASSES inverted (`0b7e632`)
Claude's frozen pre-registration (HANDOFF_CLAUDE_2026-10-11c.md) executed with
machinery verified exact first: 𝔖(d) matched brute-force local counts
(0.994–1.002 = expected prime tail); f(t)=t sanity converged to −ln10 = MS;
two real bugs caught in flight (Legendre sign; prime-power exponents — the
second invisible in smoke, caught by a Tonelli crash, table then sympy-verified
on all 72 lanes, zero mismatches).
- **(a) FAIL:** free quadratic pair series is 2× too calm. Theory pooled rungs
  0.785/0.674/0.571/0.463/0.337/**0.023** vs measured 0.890/…/0.509. OLS slope
  −0.141 vs measured −0.075. Root cause named: the unweighted two-point sum is
  **not summable** — D's split-prime lattice plants correlation at every scale;
  T(W) drifts −5..−9 per decade with the rate still growing at 10⁷.
- **(b) PASS, opposite of the wager:** with d²≡D common-root terms off, the
  per-prime average is ∏(p²−4p+2)/(p(p−4)) ≈ 0.40 and S goes LINEAR (−0.6·W).
  The common-root terms are not an 11% correction — they are what makes the
  calm a log-law at all.
- GLM's 0.64 ceiling also misses (truncated free-sum curve 0.82→0.58 vs his
  measured cut-off rungs; shape inverted). Same root cause.
- **[S] filed — confinement hypothesis:** the free pair series is the
  free-ring ceiling; wheel lanes inherit P10 confinement and are calmer than
  any free-phase model. "The calm is made by confinement more than by gears."
  **Discriminator:** does the cut-off asymptote match a confined-phase
  prediction? (closes the (a)-gap mechanistically if yes)

### PHASE 12 — D2 filed: fire-count census + parity-dead channel family (`504496d`)
- **Provenance [G]:** "D2" = GLM audit-session "Draft 2 (fire-count census)".
  Its body was NEVER relayed in full — not in repo, handoffs, uploads, or
  session transcripts. D1/D3 were absorbed from relayed text (B2/B7, `bce2cf6`);
  D2 reached us only as three descriptors. Filed as an **independent
  reconstruction** (`lab/PHASE12_fire_census.{py,json,md}`), reconciliation
  against GLM's original text open [G]. Its "C4 backbone" role is superseded by
  PHASE 10.
- **[F→E] zero fires ⟺ N prime** — the census's zero class IS the layer prime
  count; exact on 204 sampled layers. Mean fire count tracks Σ1/p (ln ln m
  shape) within 0.5%.
- **[F, theorem, verified both directions over 2,045,000 visits]:** a channel
  (a,b) is parity-dead — every visit value even, no prime ever — IFF **b even
  AND a ≡ b/2 (mod 2)**. This is the channel-side dual of B5 exactly as GLM
  named it (layer congruence vs channel congruence; same parity engine).
  Minimal member: the half-turn channel (1,2) — values 2, 8, 18, 32, 50.
- **[F, closed form, exact on 750 layers m≡0 mod 4 ≤ 3000]:** dead ticks on
  layer m = Σ_{b|m, b≡2 mod 4} φ(b); b≡0 mod 4 contributes zero (units of even
  b are all odd). Zero primes on dead ticks at every checked layer; density
  mean 16.7%, max exactly 1/4. One prereg false step (φ(b)/2) caught in flight
  at m=4, corrected in place.
- Fifth 2-adic-spine instance: parity decides wedge distance, dial luck, fine
  lock, and now an exact permanently-dead channel family.

## 2. Standing queue (in order)

1. **Confined-phase calm model** — the [S] discriminator above: predict the
   cut-off asymptote under a confinement model; does it match P9's measured
   rungs? Would close the PHASE 11 (a)-gap mechanistically.
2. **7/6 m=10⁶ prereg** — same template as PHASE 8; polynomials public
   (160u²+122u+23, D=164 family via translation; D=228 family; C = 4.8887).
   Bookkeeping value high, mechanistic risk low.
3. **Gemini's witness-layer spacing-variance question** — does spacing variance
   between active channels drop abruptly at witness layers vs decay
   continuously? Checkable against existing run logs, no new probe.
4. **GLM Draft 2 reconciliation** — paste the original draft text; diff against
   `lab/PHASE12_fire_census.md` conventions and content.

## 3. Reading order for a fresh agent

1. `INSIGHTS.md` tail — six dated entries, the whole arc with labels.
2. `lab/PHASE10_c4_audit.md` — how an anomaly became a classical law under audit.
3. `lab/PHASE11_calm_slope.md` — the loud (a)-fail and the confinement [S].
4. `lab/PHASE12_fire_census.md` — D2 + the parity-dead channel theorem.
5. `lab/J1C_wedge_result.md` — the negative result and its correction history.
6. `WHITEPAPER.md` §2 (B5/B6), §4 (B7) — the laws the new results dualize.

## 4. Surprises worth keeping explicit

- Twice in one day: freeze → fail loudly → audit converted an "anomaly" into a
  classical law (PHASE 9 mirror pairs, PHASE 10 C4). The sharpened residual
  question — "does any value-side statistic survive its correct null?" — is now
  the deepest open thread on the board.
- The calm-slope (b) inversion: the object Claude wagered was an 11% correction
  turned out to be the entire load-bearing structure of the log-law.
- The φ(b)/2 false step: "half the units are even" is impossible for even b —
  a reminder that parity claims about unit groups need the trivial check first.
- The 2-adic spine now has five independent instances (wedge, dials, fine lock,
  dead channels, and the day's recurring audit-catches themselves).
