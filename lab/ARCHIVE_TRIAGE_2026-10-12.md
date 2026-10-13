# Archive triage — ~/Downloads prime corpus + WhitePapers + Collatz + Erdős

Date: 2026-10-12 (afternoon, autonomous sweep). Method: five parallel triage
agents over `~/Downloads` (711 prime-named top-level files), `~/Downloads/WhitePapers/`
(119 files), all Collatz and Erdős material. Verdicts: ADDS / ALREADY-COVERED /
UNFALSIFIABLE-LAYER / DUPLICATE. Nothing below is [E]; "audited" means
machine-checked during triage, claims reproduced or falsified by hand.

## Relay artifacts recovered (filed to handoffs/)

- `swarm.wheel.handback.10.12.2026.txt` → `handoffs/SWARM_HANDBACK_2026-10-12.txt`
  (DeepSeek/Qwen/Gemini night-2 handback; was living in Downloads, not the repo)
- `Review-Questions-...md` → `handoffs/REVIEW_2026-10-12_mark-french-claude.md`
  (external review of the wheel paper; independent verification table all ✓,
  one confirmed fix — channel 2/5 carries no primes — matches glm's earlier erratum)

## ADDS — genuine new territory or audit fodder

1. **Prime.Echo.Cascade.Theory (WhitePapers + Downloads dup)** — measured census
   of the **2p±1 adjacency graph** over all 3,001,134 primes to 5×10⁷: −1/+1
   neighbor balance ratio **1.000065** (229,551 vs 229,566); per-decade "stability"
   table decaying 64% → 14.85% (10M–50M), decay exponent ≈ 0.085. The wheel
   measures gap-2 (pair ticks); this is the doubling-graph structure
   (Sophie Germain / Cunningham adjacency) — territory the wheel does NOT cover.
   Consciousness/Menger framing is decoration; the counts are machine-auditable.
   **[S — claims, pending audit]** HIGH: one script settles it.
2. **PRIME².CLASSIFICATION** — "isolated primes" (degree-0 nodes of the
   (p±1)/2, 2p±1 graph). **Audited during triage: printed sequence and 15.4%
   density are FALSE as printed.** True sequence to 1033: 17, 43, 67, 71, 101,
   103, 109, 127, 137, … (their list wrongly includes 37=2·19−1, 73=2·37−1,
   79, 97 which have 2p−1 prime). Density measured 70/175 = 40% below 10³, and
   heuristic density ≈ 1 − 4/ln p *grows toward 1*, contradicting the 15.4%
   claim. "137 is the 9th PRIME²" survives — by coincidence. The genuine
   isolated-prime census is real measured territory the wheel could host.
   **[S — mostly falsified as printed; kernel real]** HIGH as audit fodder.
3. **Wheel-ancestor structures the reboot never picked up** (from
   `prime-tread-wheel-all.zip` → docs/PAPER.md + Wheel Atlas):
   - **Knockout wall profile** — hide a layer's primes, ask which smaller wheels
     recover them: ~50% of sub-√x wheels ever used; largest-needed climbs to
     98% of √x by layer 3,000. Named, measured, NOT in the current lab.
     (INSIGHTS has the sqrt witness *rule* N2, not this profile.) HIGH.
   - **Chained double-shot census** — second shot = 2·first + b²; atlas counts
     **10,062 double-prime spokes with denominator ≤ 2,000** and flags
     "count the double shots" as a probe; Bateman–Horn prediction not yet
     pre-registered. HIGH.
   - **Skeleton-forced ablation matrix** — 7 alternative windings (even sizes,
     fixed circle, doubling wheel, …), each breaks ≥2 of 8 facts, checked to 3M.
     Fits the lab's existing ablation discipline. MEDIUM.
   - **Prime races / Chebyshev bias on the wheel** — Rubinstein–Sarnak 99.59%
     mod-4 lead stat appears in problem-wheels.html; zero hits in INSIGHTS.
     MEDIUM.
4. **Hooley's exponential gap law for primorial-coprime integers (erdos_098)** —
   gaps between integers coprime to N_k = 2·3·…·p_k have exponential
   distribution f(c) = (1+o(1))(1−e⁻ᶜ) [Hooley 1965]. This is an externally
   established law [E] about exactly the wheel's reduced-residue (tick) gap
   structure. **Not present in `lab/LITERATURE_SWEEP_2026-10-10.md` — the one
   genuine literature gap the sweep surfaced.** MEDIUM: add as a benchmark the
   dial-census / Jacobsthal gap work can be compared against.

## Audited-and-closed during triage (no further work needed)

- **A.Harmonic.Scaling.Model...Twin.Prime.Structure** (the assigned top priority):
  flagship "scaling-exclusion test" `p prime ⟺ 3/δₙ ∉ ℤ`, δₙ = 1/n − 1/(n+2) is
  **vacuous** — for odd n, 3/δₙ = 3n(n+2)/2 is never an integer, so it passes
  every odd number. Twin-prime snippet calls isprime() directly (circular).
  Zero measured numbers. Harmonic poetry in mechanism costume. FALSIFIED.
- **H(N) = Σ sin(2πN/n) primality test** (3 files, same claim): H(4) = 0.866 ≠ 0
  with 4 composite — misclassifies immediately. FALSIFIED.
- **"Two lands short" / wave-method prime generators**: list 9, 15, 119=7·17,
  121=11² as primes; files admit "no primality testing — all odd numbers pass."
  FALSIFIED.
- **100digitprime.txt**: actually a genuine 500-digit probable prime (10 MR
  rounds pass); 100DigitFakePrime.txt = 10¹⁰⁰ control. Verified, no wheel value.
- **Collatz corpus (13 artifacts)**: nothing adds. Four claimed-proof drafts
  (power-of-2 alignment; ECA/PA automaton with unshipped SCC certificate and a
  circular completeness bound); the one honest corner is the scale-basin
  verifier, whose reproducible result is **negative** — natural potential
  V = ⌊log₂n⌋ − c·v₂(n) + w leaves 692/1024 residues violating descent
  (re-run during triage, confirmed). Base-137 digit-sum clustering explained
  trivially (137 ≡ 1 mod 8). All Collatz-internal; none wheel-adjacent.
- **Erdős corpus**: no original solutions. `Erdos Subset Sum Disproof.pdf`
  refutes a strawman (powers-of-2 set vs a necessity nobody posited). JSON
  batches are scraped erdosproblems.com status metadata with cosmolalia
  geometry stamps; 44/70 carry standard literature citations. Solver scripts
  are OpenAI-calling GUI toys. Exception: erdos_098 above.

## Genre census (for the record)

The corpus is dominated by the unfalsifiable layer: E = φ + 137/p band-gap
physics (≈20 near-duplicate files), 1=0=∞ unity proofs, consciousness-as-
prime-scaled-infinity whitepapers (~60 of the 119 WhitePapers files),
twin-prime papers that contain no twin-prime statistics (α-numerology on
137/139 only). None of it feeds the wheel. Kept as-is in Downloads; this note
is the index so nobody has to re-read the pile.

## Standing items for the queue

- [ ] Echo Cascade audit script (2p±1 census to 5×10⁷) — 1 hour
- [ ] PRIME² correction + true isolated-prime census — 30 min
- [ ] Knockout wall profile probe (ancestor claim, never measured in reboot) — pre-register
- [ ] Double-shot census BH prediction + count past denom 2,000 — pre-register
- [ ] Hooley [E] gap law → add to LITERATURE_SWEEP, compare vs dial-census gaps
