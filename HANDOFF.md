# HANDOFF — Prime Tread Wheel, session state as of 2026-10-08 morning

Written by Kimi for Claude. Everything below is cross-checked against
INSIGHTS.md, probes/README.md, and the git log. If anything here disagrees
with those files, the files win — this document is a map, not the territory.

---

## 1. What the project is

The prime tread wheel: layer m holds the m numbers T(m−1)+1 .. T(m), where
T(m) = m(m+1)/2 (triangular numbers). Tick k on a lap sits at angle k/m.
Repo home: ostoe.com/prime-tread-wheel; remote:
https://github.com/Cosmolalia/prime-tread-wheel.git. Canonical paper is
PAPER.md (§1–§9; §8 is "the wheel as a multiplexer", §9 the renumbered open
question).

The parent conjecture (OEIS A066888): every lap contains at least one prime.
Directly verified to layer 10⁹ (`boundary.c`, 3.13B MR tests, exact below
3.3·10²⁴), extended through exhaustive prime-gap data (<4·10¹⁸, max gap
1476) to layer 2,828,427,124. Worst known bottom margin: 766 ticks, at layer
m = 264,800,157 — the "record layer" every shadow probe below refers to.

## 2. How Sylvan works (read this before touching anything)

Sylvan does **mechanism-first theoretical science**. The base rules that
govern every exchange:

- Epistemic labels on every claim: **[S]** stated by Sylvan (premise, not
  proved by plausibility), **[F]** actually follows from preceding
  statements, **[G]** gap — resolution stops here, say exactly what is
  missing, **[E]** externally established or machine-verified here (import
  only the demonstrated mechanism, not the surrounding field).
- **Never increase the resolution of a claim beyond what the mechanism
  specifies.** Names come after mechanisms. Do not retrofit into standard
  math because it resembles something. Mathematics when earned.
- **Attack connectors, not endpoints.** For A→B→C, ask why A produces B and
  whether B necessarily produces C. Mark the arrow [G] when needed.
- Honest negatives are load-bearing and are logged, never deleted.
  Superseded readings are marked, not erased.
- Use the smallest sufficient claim. Do not slide between possible /
  proposed / derived / observed / established.
- Sylvan's pictures are geometric and load-bearing ("stacking cups /
  rainbows", "leading corner falls a little short", "scaling moves right
  before 1/2, left after, meeting at 1"). When a measured result matches one
  of his pictures, say so in his language. When it doesn't, say that plainly
  too — he explicitly prefers that.
- Nothing stays only in context. **Every insight goes to INSIGHTS.md and
  gets committed the moment it lands.** Sylvan's standing instruction:
  "you lose it after each run so leave nothing inside and unsaid."

## 3. The reframe that drives current work

Sylvan's framing (now the project's): **the wheel's primary object is not
primes — it is the stagger of the numberline as the wheel grows. Primes fall
out of reading the stagger.**

Definitions (all measured, see INSIGHTS.md 2026-10-08):

- **Stagger field.** For prime p, its shadow on lap m lands at tick
  k ≡ o_p(m) = −T(m−1) (mod p). The stagger field at step m is the tuple
  {o_p(m)} over all prior primes. (`probes/stagger.py`)
- **Mouth.** The initial run of shut ticks at a lap's left edge; its width W
  = offset of the first interval prime (`ifirst_off` in shadows.c). Trailing
  mirror fields: `ilast_off`, `itrail` (right-edge shut run).
- **Seats vs interval primes.** Seat = gcd(k,m)=1 (wheel-native candidate).
  Keep seat-prime stats (`first_off`) and interval-prime stats (`ifirst_off`)
  separate — they differ structurally (e.g. m ≡ 2 mod 4 laps have ZERO
  seat-primes; all their primes sit on non-seat ticks).

## 4. What is established [E] as of this morning

1. **Stagger-determinism.** The first-prime offset of every lap m=4..5000
   (and 400/400 validation at m≤2·10⁴) is reproduced exactly by computing
   the arc cover from {o_p(m)} alone — no values. The first-prime function
   is a pure function of the stagger configuration. (stagger.py,
   stagger_mc.py with the exact sqrt witness rule)
2. **Exact composite-ness rule.** Tick k on lap m is shut iff ∃ prime
   p ≤ √(T(m−1)+k) with k ≡ −T(m−1) (mod p). Arcs p > √v never witness
   compositeness. The √T(m) sieve limit is the exact witness bound.
3. **Parabolic confinement.** Each o_p(m) has exact period p in m (period 4
   for p=2) and visits exactly (p+1)/2 of p phases — the triangular numbers
   mod p. Each arc sweeps a discrete palindromic parabola across laps.
4. **Exact aperiodicity.** Joint field over first r primes recurs with period
   lcm(2..p_r) ≈ e^{p_r} (~10³⁶ laps for r=25). Never repeats physically.
5. **Zero internal field correlation (orbit-law search, closed provably).**
   The joint orbit is the full Cartesian product of individual images with
   multiplicative multiplicity (CRT, verified exactly). The stagger field
   has NO internal correlations to exploit. Its entire law is the single
   quadratic counter s(m) = −T(m−1).
6. **Movie not frame.** Within a lap, shadows arrange freely (no k-direction
   constraint; covers can pile up — the record mouth is a generic-sieve
   pile-up, rank 1/119 but fully explained by striker count). Across laps,
   orbits are confined parabolas. Therefore any wheel-native proof must be a
   **law on stagger orbits**, not a per-lap covering constraint.
7. **Width ~ striker count (conjecture-grade invariant).**
   spearman(W, mouth_distinct) = 0.995 at m~10⁴, 0.981–0.992 at 2.6·10⁸.
   Scale-stable from 10⁴ to 2.6·10⁸. (Distribution *shape* is NOT
   scale-invariant — small laps have a W≈0–1 atom — but this identity is.)
8. **Seat palindrome.** gcd(k,m) = gcd(m−k,m): the seat pattern is a
   palindrome about the midpoint. Provable, wheel-native.
9. **Halves-claim (empirical, unproven — the strongest wheel-native
   candidate for a paper statement).** From m=21 up, every lap has ≥1
   interval prime strictly each side of the midpoint. Zero violations in
   ~120k laps: 21..20k and 21..100k exhaustively, record layer, m≡2 mod 4
   laps, laps at 10⁶. Six violations below m=21 (m = 2,3,4,7,8,20).
   Stronger than no-empty-layer. Bonus structure: W_left and W_right are
   per-lap uncorrelated (r≈0.02) yet their distributions are mirror-twins
   (med 11 vs 12, p99 78 vs 81) — distribution-level symmetry without
   lap-level coupling, unexplained by any current mechanism.
10. **Record-layer anatomy.** Mouth = two-stage conjunction: small outside
    primes (2…331) shadow 766 ticks down to 57 holes; all 57 holes composite
    with both factors > 766 (43 semiprime, 14 deeper). 100% of cover from
    outside primes; routed primes contribute nothing. Redundancy 1.68× but
    270/766 seats singly covered. Striker k₀ values uniform — no slip
    alignment signature.
11. **Endpoint identities.** T(m) composite for all m≥3; T(m)−1 composite for
    m≥4 — the lap's last two ticks are arithmetically forbidden primes, so
    itrail ≥ 1 universally. Opening tick is odd → 2× random prime density
    (exactly 2.000 observed, pure parity).

## 5. Honest negatives (closed routes — do not reopen without new mechanism)

- **Orbit correlations** — none exist (exact, N1).
- **Mirror compensation** — dead at both scales (r = −0.07 at 10⁴, +0.02 at
  2.6·10⁸). The seat palindrome does NOT propagate to value-side mouth
  geometry.
- **"Ratio as slip" / hole co-factor structure** — holes are exactly
  W-rough numbers; the 74% semiprime fraction is the Mertens rough-density
  prediction, matched per-W-bucket. Nothing wheel-native.
- **Per-arc thinning law** — derived cleanly, refuted in 0.013 s
  (wraparound fills small residues; marginals ~uniform). Logged as
  correction N8, not deleted.
- **Slip/balance constraints forbidding full covers** — empirically they do
  not bind the shadows.
- **Stagger MC** — the quadratic counter vs iid changes mouth statistics
  only marginally: KS gap 0.060, tail fattening ~1.5× at W≥50 (~11σ),
  mechanism unpinned [G minor]. At m ≤ 2·10⁴ the quadratic counter is
  statistically nearly invisible; the record's 767 is a tail event under
  both models.

## 6. The load-bearing gaps [G]

1. **The routing wall (the whole game, precisely stated).** The stagger field
   determines everything (stagger-determinism) but the only known reading is
   the uncompressed O(m) simulation. No compressed wheel-native law of the
   field is known. The gap is located to a single point: **one quadratic
   walk s(m) = −T(m−1) interacting with the compositeness of the values it
   walks over.**
2. **Halves-claim mechanism.** Values don't inherit the seat palindrome
   (mirror compensation dead), so ≥1-prime-each-side cannot come from the
   symmetry — it would need a direct orbit law. Unproven, empirically
   bulletproof.
3. **Tail-fattening mechanism [minor].** Which arcs drive the 1.5× W≥50
   fattening? Local perturbation test queued.

## 7. Queue (value order, from INSIGHTS.md)

1. Decompose W = f(mouth_distinct) exactly — the width~strikers law says W
   determines striker count almost exactly; find the residual law
   (is mouth_distinct = W − plugs-missed?).
2. Tail-fattening perturbation test (flip one prime's phase iid→quad,
   measure d(tail)/d(phase)).
3. Draft the halves-claim for PAPER.md as a named conjecture whenever
   Sylvan says go — it's the strongest wheel-native statement available and
   is narrower/more falsifiable than the parent conjecture.
4. m ≡ 2 (mod 4) theorem is a clean §3/§4 paper line (seat-primes
   identically zero; seat test misaligned from value-divisibility by m/2).

## 8. House conventions

- **INSIGHTS.md** (repo root) is the standing lab notebook: cumulative,
  newest at bottom, nothing deleted, epistemic labels on every entry.
  Every insight lands there the moment it appears — never held in context.
- **probes/README.md** documents every probe with its exact reproduce
  command and expected result. Update it when adding/changing probes.
- Git discipline: commit specific files only (NO `git add -A`). Compiled
  binaries (`shadows`, `boundary`, `layer_gap*`) are committed alongside
  sources per existing practice; `*_head.bin` diagnostic binaries are
  gitignored (regenerable, 40KB small / 16MB record) — regenerate with
  `./shadows <m>`; keep small-lap bins (m<100000) on disk for the
  factorization analyses.
- Long jobs: `setsid nohup ... & disown` from the probes dir, log to
  probes/logs/ (gitignored except the named batch logs we deliberately
  add with -f). Report PID + log path.
- C probes: `gcc -O3 -march=native -o <name> <name>.c -lm`; verify against
  hand-checks or sympy before trusting output at height.
- shadow batch commands: `./shadows -b <start_m> <count> all` (consecutive)
  or `prime` (prime laps only). Record-layer full dump: `./shadows
  264800157` (~24 s).
- Logs: shadows_batch_all2.log, shadows_batch_prime.log (60 laps each, the
  119-lap batch), shadows_batch_small.log + shadows_batch_mirror.log
  (60 laps each at m~10⁴ / m~2.6·10⁸ with trailing-edge fields),
  stagger_mc.log.

## 9. Sylvan's live geometric pictures (for interpreting future results)

- **Cups/rainbows:** each lap is a 2D curve with width and depth; stacking
  laps, the leading corner always falls a little short. The measured lip =
  singly-covered + uncovered seats at the mouth edge. Mirsky–Newman–Davenport–
  Rado covering-system theorem is the nearest proved statement to "no exact
  closure" (exact tiling forces redundancy) — import only that mechanism.
- **Scaling signature:** scaling moves right before the 1/2 point, left
  after, meeting at 1; offsets consolidate into the new unit. PROVED at the
  pattern level (seat palindrome) and, remarkably, at the single-arc level
  (each o_p(m) orbit is a palindromic parabola). NOT propagated to values.
- **1/5-offset banking:** prime 5's stagger advances by −m mod 5 each lap,
  banking one whole unit of drift per lap — five laps = one full unit. Sylvan
  described this before the stagger field had a name; it is now a theorem in
  the field's language.

## 10. Session handoff state

- HEAD: 90310f3 ("halves-claim holds m=21..100000..."). Working tree clean
  except regenerable `*_head.bin` files (deliberately untracked).
- Nothing running. No scheduled wakeups.
- Last open thread with Sylvan: whether to (a) decompose W =
  f(strikers) exactly, (b) chase the tail-fattening mechanism, or
  (c) draft the halves-claim into PAPER.md. He tends to answer with a new
  geometric picture rather than picking — follow the picture.
