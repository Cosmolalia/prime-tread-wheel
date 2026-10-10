# MEMENTO — lab notes to self (context-retention rule)

STANDING RULE (Sylvan's instruction, binding): after EVERY phase or
significant observation, append here:
- **Surprise** — the highest information-density signal. What did I not expect?
- **Patterns noticed** — even ones that "don't matter yet."
- **Epiphanies / reframes** — the moment a connector clicked, with the connector.
- **What's actually important right now** vs noise.
- **Open loops** — things I said I'd check and haven't.
If context was compacted: THIS FILE IS THE PLOT. Trust it over reconstruction.
Tone: first person, terse, honest about nulls. A boring answer is a closure,
not a failure. Surprise ledger and connector log below.

---

## Entry 2026-10-10 ~01:35 — chain start (state of the world)

**Trust-this-over-reconstruction facts:**
- Machine: Prime Tread GPU frontier, `data/projects/prime-tread-wheel/gpu-frontier/`.
  Live window pid 6410, layer ~282.005M, ~77 layers/s, 200,920,348 rings
  (TRIMMED table — the duplicated-2 cache bug is fixed; caches sanitized;
  load path guards legacy files). Do not re-litigate the duplicated-2 bug.
- Tonight shipped: witness-count layer (ω(N) per tick, uint32 window via
  atomicAdd, zero roll cost; `s` and `--dump-band` save
  `witness-band-m<M>.npy` sidecar). Self-check verifies counts exactly.
  Commits: e479f32 (code), 08c58d1 (docs).
- Band on disk: layer 1,500,000 dump — N ≈ 1.125×10¹², 1,048,576 ticks,
  37,739 primes, one-witness rate ~15.8% (audited 400 ticks vs trial
  division, 0 mismatches).
- Mechanism truths [F]: one-witness tick ⟹ N = p·q (semiprime) or prime
  power; count 0 ⟺ prime; ≥2 ⟹ full ω. Poke rate Σ1/p ~ ln ln N ≈ 3.6/tick
  at N≈4×10¹⁶. Cam-count (memory) grows π(√N); event rate barely grows.
  The machine is ONE clock with passive cams — "parallel computation" was
  the wrong frame.
- Binary question settled with numbers: hot loop IS compiled (NVRTC SASS);
  Python is a per-layer shell (~8ms/frame of ~104ms); the 12ms/layer roll vs
  0.9ms floor gap is contention (xmrig) + kernel-under-contention, NOT
  language. Resource law (20B/ring/layer presence traffic) is
  substrate-independent.

**Mined-out vs open (the map):**
- Value side: PROVABLY depleted (A2: zero internal correlation; A6: iid-
  indistinguishable). Every value-side probe now predicted null BY THEOREM.
- Pattern side: open queue = C1 (halves, flagship), C2, D8, D9, F2 (needs
  SAT), G2–G4, G6–G9. Witness layer opened NEW territory with zero probes
  (hardness classification axis).
- INSIGHTS.md ~30 probes deep; territory map at INSIGHTS.md:907–1002.

**Tonight's chain:** AUTONOMY_2026-10-10.md (same dir as this file).
Phases 0–6. Pre-registered predictions: P0 → gap mostly closes under paused
miner; P1 → MATCH (census axis dies by measurement); P2 → null; P3 → null.
Binding rulings. Global stop 06:00. Midnight rule: nulls are closures, never
re-run a boring probe.

**What would surprise me tonight (ranked):**
1. P1 deviation — would mean a mechanism-level bug, huge.
2. Any ring-phase predictivity (P3) — contradicts A2 by construction.
3. C1 cracking under factor-form algebra — the paper door opening.
4. P0 gap surviving miner pause — kernel finding, redirects everything.

**Open loops right now:** P0 number not yet taken; Phases 1–2 not started;
user asked for uncontended-floor measurement earlier — P0 answers it.

## Surprise ledger

- 2026-10-10 01:37 — **xmrig is GONE** (not stopped — absent). Load decay says
  it died/stopped ~01:15–01:30. The planned pause-A/B evaporated; the world
  changed under the experiment. Lesson: verify experimental conditions BEFORE
  designing the probe, not during.
- 2026-10-10 01:39 — **prediction falsified, twice over.** (1) Live window
  rate insensitive to miner (77→76 layers/s) — the confident "xmrig is the
  drag" attribution from earlier tonight was WRONG for the GPU path; xmrig's
  real victim was memory-latency paths (searchsorted), not GPU throughput.
  (2) Benchmark halves when the live window co-occupies the GPU (83→41) —
  co-tenancy, not CPU contention, is the benchmark's dominant variable.
  Both corrections come from MEASUREMENT, not re-reasoning. This is why the
  pre-registration rule exists: a falsified prediction is a finding, and
  tonight it killed a bad causal story before it ossified into the README.
- 2026-10-10 01:45 — Phase 2 NULL: the ω-map has no spatial structure beyond
  deterministic small-prime periodicity. The naive iid null is decisively
  REJECTED (P(gap=1) 0.272 vs 0.328) — the honest null had to carry the
  determinism; that's a methodological lesson for every future null in this
  lab: the wheel's "randomness" only starts above the deterministic base.
  Residual ~2σ clustering hint logged, NOT chased (below the 3σ bar).
- 2026-10-10 02:05 — Phase 1 MATCH, with the scariest-looking number of the
  night: the pre-registered formula was off by +3,869σ and it was MY formula,
  not the machine. The exact enumeration hit 165,861 == 165,861 (0.000σ) —
  a DETERMINISTIC identity, stronger than any statistical match: the witness
  array's semantics are now certified by independent construction. Lesson
  (standing): in this lab, huge σ-deviations are more often spec errors than
  discoveries — root-cause the PREDICTION with the same rigor as the data.
- 2026-10-10 02:20 — Phase 0.5: BOTH hypotheses falsified; true mechanism is
  critical-path serialization — one thread per ring, p=2's thread walks W/2
  iterations and bounds the entire kernel while the other threads idle. Cost
  ∝ ΣW/p scattered writes, nearly INDEPENDENT of ring count. My "220MB ring
  traffic" framing (repeated all evening, even into the physical cam model!)
  was a red herring — the stamp kernel reads 8B/ring. Corrected picture:
  PRESENCE was never the traffic; EVENTS were never the count; the kernel is
  LATENCY-bound on its longest thread. Also: uint32 window measured SLOWER
  than uint8; atomicAdd ≈ 50% of kernel time. Fix queued (Phase 0.6):
  window-parallel small-p, projected ~1–3 ms/layer vs 12.
- 2026-10-10 02:10 — **the live window died silently** (no traceback; probe at
  ~02:15 found no process; HUD was fine at 01:39). Likely a human quit — if
  Sylvan didn't close it, a silent no-traceback crash is itself worth chasing.
  Relaunched pid 19718 from layer 282,200,000, verify PASS. LESSON: the chain
  assumed the co-tenant existed for ~35 min without checking — same lesson as
  the xmrig A/B, one level down. Verify experimental conditions FIRST.
- 2026-10-10 02:50 — Phase 3 NULL: retained-structure axis closed with data.
  Every cross-layer correlation inside the corrected null envelope. The
  interesting moment: lag-0 j=3 looked like a 2σ+ excursion past the naive
  null — and was root-caused as SIEVE-LATTICE SELF-ALIGNMENT: the wheel's
  fixed layer spacing D_j carries small factors, so periodic sampling of the
  number line correlates with the sieve lattice for free. STANDING METHOD
  LESSON: nulls for any periodically-spaced sample must be ALIGNMENT-MATCHED,
  or the lattice itself manufactures fake structure. (Parallels the Phase 2
  lesson: determinism lives in the base, not the null.)

## Connector log

- 2026-10-10 00:28 — "the machine has exactly one moving part": GPU lanes,
  CPU sieve, and physical cam-shaft are the same mechanism wearing different
  substrates; the resource laws (π(√N) presence, 20B/ring, √N wall) travel
  with the mechanism, not the substrate.
- 2026-10-10 00:34 — witness set IS a complete factorization certificate
  (remainder after dividing by all witnessed primes is 1 or prime — proof by
  contradiction using the contract bound; one CPU division recovers the
  cofactor; bignum only past ~1.8×10¹⁹).
- 2026-10-10 02:05 — the one-witness class N = pᵃ·q (p ≤ bound < q) is ~92×
  more numerous than classical semiprimes. The wheel natively emits a hardness
  census that π₂-based tools undercount by two orders of magnitude — that's a
  capability claim, not just a closure: anyone wanting this statistic cheaply
  should use a witness engine, not Lehmer machinery.
