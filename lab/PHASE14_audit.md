# PHASE 14 — 7/6 census reproduction + relay audit round (10-12 handback)

Date: 2026-10-12 (post-midnight). Artifacts: `lab/PHASE14_dial76.py`,
`lab/PHASE14_dial76.json`, `lab/PHASE14_objA_dcurve.py` (running),
`lab/oct11e_relay/` (extracted handoff-claude-oct11e zip).

## 1. GPT's PHASE 14 (7/6 dial, m <= 1e6): reproduced to the digit [E]

Independent reproduction (`lab/PHASE14_dial76.py`), MR primality
(bases [2,3,5,7,11,13,17], deterministic at these magnitudes) validated
against SymPy on 600 random family values before counting — zero
mismatches. Convention `L(m) = floor(7m/6 + 1/2)` (ties up), matching my
PHASE8b engine `(2*a*m+b)//(2*b)` — GLM's round() landmine does not bite
this repo (see §4).

| quantity | GPT's relay | this reproduction |
|---|---|---|
| F1 prediction (C = 4.9116695006) | 8222.1167 | 8222.1167 (8222.1167257) |
| F2 prediction | 8221.7768 | 8221.7768 (8221.7767788) |
| F1 primes (u = 0..41666) | 8,280 | 8,280 |
| F2 primes | 8,180 | 8,180 |
| total ratio observed/predicted | 1.00098 | 1.0009794818 |
| F1 primes, m <= 200k | 1,871 | 1,871 |
| F2 primes, m <= 200k | 1,905 | 1,905 |

Every count matches to the unit, including the in-sample sub-window.
The 7/6 m = 10^6 prereg is therefore CLOSED [E]: Bateman-Horn on the
induced family to 1.00098, second instance after 5:4. Note both families
were counted over u = 0..41666 (full range, m <= 1e6 inclusive); GPT's
prediction window matches. GLM's prereg used C = 4.8887 (2,000-prime
product) and an out-of-sample window m > 200k — different constants,
same law; with the correct C the m > 200k slice is 6409 + 6275 = 12,684
actual vs 12,672.3 predicted (ratio 1.0009).

## 2. GPT's Jacobsthal closure of the J1c cliff: reduction verified, one claim overreaches

**Verified [F + E]:**
- Convention match: my frozen v2 probe (`probes/j1c_wedge_milp.py` header)
  states home c* = 0, cover iff c == (j+T) mod p — exactly GPT's CRT
  reduction setup (phases one-hot, Delta free mod Q by CRT).
- h(25) = j(97#) = 258 is published [E] (Hagedorn 2009; OEIS A048670;
  Ziller-Morack 2016). Prime-layer cliff edge matches my
  `lab/J1C_spectrum_v2.json` exactly: last feasible prime 257, first
  infeasible 263, all prime layers >= 263 infeasible.
- Corollary for object A: m >= 258 impossible (needs m consecutive
  Q-non-coprime integers; max run is 257).
- Grok's seat table (256 vs 262 against 258) is the same statement.
- GPT's home-cover census reproduces exactly: d = 0 wipeable =
  {2,...,13}, first failure layer 14 (tick values 101, 103 are
  97-rough) — verified against my own probe's smoothness test.

**Overclaim, corrected [F]:** "All-ticks wipe feasible iff 2 <= m <= 13"
conflates d = 0 (home cover) with feasibility (any displacement). The
census GPT ran establishes d = 0 iff m <= 13. Feasibility with
displacement is the MILP question, and for 14 <= m <= 257 the
Jacobsthal runs predict FEASIBLE with d >= 1. The true global statement:
d = 0 iff m <= 13; feasible iff m <= 257. The gap 14..257 is measured by
`lab/PHASE14_objA_dcurve.py` (see J1C_wedge_result.md CORRECTION v4).

**Noted, non-load-bearing:** GPT §3 prints "h(n) = 2*omega(n)+2" with
"omega(25) = 128" — omega here is not prime-omega; as printed the formula
is notational/circular and unverified. The ring-2 parity sketch (257: 128
seats per parity at the extremal threshold; 263: 131, impossible) is a
plausible mechanism story but was not independently checked; the closure
does not rest on it.

## 3. Claude's pair8.c (1e8 calm rung): verified [E]

Compiled clean; lane c=14, W=1e6, PG=2e6 with uniform and engine weights.
- G to PG = 2e6 matches my Kronecker-table computation to 12 digits
  (0.336145392662 both).
- S rungs vs my fix3-convention build_F (bp over ALL split primes <=
  bound): agreement ~4e-10 at every rung 1e2..1e6 — Claude's "9 digits"
  claim confirmed.
- Housekeeping: the S discrepancy I measured mid-audit (0.7 at W = 1e6)
  was my harness calling build_F with the STALE default B2 = 1e5; under
  the frozen fix3 convention (B2 = full prime bound) it vanishes. This
  re-confirms fix3's magnitude from a second direction: extending bp from
  1e5 to 2e6 moves S(1e6) by 0.698, growing ~3.4 * d(ln ln bound).
- Latent wart (non-load-bearing): pair8 reads the weights grid with
  unbounded fscanf into a 1<<16-entry buffer; grids > 65536 lines
  segfault. His documented usage supplies 5000-line grids.
- Claude's layer counts (P15 foundation): his
  `p15/claude_layercounts_m_le_1e5.csv` matches my independent column
  engine (`column-engine/layers_1p8M.csv.gz`) with ZERO mismatches over
  all m <= 1e5. P15's data foundation is [E]; the explicit-formula
  reading is known math shown wheel-native, as framed.

## 4. GLM's round() landmine: repo audit [E-verified safe for 7/6]

- `lab/PHASE8b_halfturn_engine.py` (the source of the filed 7/6
  families): L(m) = (2*a*m + b)//(2*b) = floor(a*m/b + 1/2) — ties UP,
  engine-consistent. SAFE.
- `lab/PHASE14_dial76.py` convention spot-check: L(9) = 11 (ties-up) ✓,
  and the triple agreement of §1 (my filed 1,871/1,905 counts, GPT's
  census, this reproduction) confirms the filed 7/6 column was computed
  ties-up.
- `probes/ratio_sweep.py` used Python banker's round() — WARNING COMMENT
  ADDED in place. Affects only tie laps (m*r half-integer, exists for
  even b) at even-b ratios. The filed L1-L4 laws are qualitative and
  tie-robust; no re-run warranted. Do NOT use ratio_sweep for family
  identification at even-b ratios.

## 5. Status of the standing queue

- 7/6 m = 1e6 prereg: CLOSED [E] (§1).
- J1c cliff [G]: CLOSED for prime layers [F + E] (Jacobsthal + CRT,
  convention-verified). Object-A d-curve completion: see J1C correction
  v4. Pre-cliff d ~ 0.0737m + 0.64 slope mechanism ("why m/14"):
  reframed by GPT §4 as a primorial CRT Hamming distance — still [G],
  now with exact formulation.
- 1e8 calm rung: verified [E] (§3); every P9 rung 1e2..1e8 matched by
  the bare pair series stands.
- Gemini's witness-layer spacing-variance question: still open (needs
  per-tick channel logs; not in the column-engine CSVs, which store
  per-layer counts only).
- GPT §7 factorable odd branches + total 16,462: the factorizations are
  one-line arithmetic [F] (verified by inspection: (6t+1)(56t+5) etc.
  expand to the stated polynomials); the census total follows from §1.
