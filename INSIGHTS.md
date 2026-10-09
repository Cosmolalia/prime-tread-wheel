# INSIGHTS — Prime Tread Wheel lab notebook

Cumulative. Newest at the bottom. Nothing here is deleted; superseded
readings are marked. Epistemic labels: [S] stated by Sylvan, [F] follows,
[G] gap, [E] externally established / machine-verified here.

---

## 2026-10-08 — The stagger is the primary object

**Reframing (Sylvan):** the wheel's primary object is not primes. It is the
*stagger of the numberline* as the wheel grows relative to prior layers.
Primes fall out of reading the stagger; the scaling can be seen at each
step in the count. Probes should measure the stagger itself.

**Stagger field (definition).** For prime p, its shadow on lap m sits at tick
k ≡ o_p(m) = −T(m−1) (mod p), o in 1..p. The stagger field at step m is the
tuple {o_p(m)} over all prior primes. (probes/stagger.py)

### Verified this run

1. **[F] The whole numberline's stagger at step m is the single counter m,
   read in every prime modulus at once.** Lap-to-lap, the entire field shifts
   by o_p(m+1) − o_p(m) = −m (mod p). One tick mark advances every layer's
   fractional offset simultaneously. This is the precise form of "a running
   tick mark counter with aperiodic scaling traversal": the counter IS m;
   each prime reads a different base-p digit of it.

2. **[E] Parabolic confinement.** Each o_p(m) is periodic in m with exact
   period p for odd primes (0 violations, p<200, m<400); p=2 has period 4
   (the parity axis runs on the 4-lap cycle — §4's mirror operator). Over one
   period, o_p visits exactly (p+1)/2 residues — the triangular numbers mod p.
   The arcs do NOT sweep their circles uniformly; each sweeps a discrete
   parabola and is forever confined away from (p−1)/2 of its phases.
   Example, p=11 one period: [10,8,5,1,7,1,5,8,10,11,11] — palindromic
   parabola, symmetric about its vertex, exactly as the scaling picture
   (right before midpoint, left after, meeting at 1) predicts at the level
   of individual primes.

3. **[F] Exact aperiodicity of the joint field.** The combined configuration
   over the first r primes recurs with period lcm(2..p_r) ≈ e^{p_r}:
   first 25 primes → ~10^36 laps; first 30 → ~10^59. The full stagger never
   repeats within any physical horizon. Aperiodicity is proved, not observed.

4. **[E] Stagger-determinism (the platonic map, exact form).** Computing the
   arc cover from {o_p(m)} alone — no values, no arithmetic on values —
   reproduces the actual first-prime offset of EVERY lap m=4..5000
   (4,997 laps, 0 mismatches, widest stagger-open mouth: 100 ticks).
   "Primes fall out of the stagger" is literally true at tick resolution:
   the first-prime function is a pure function of the stagger configuration.
   The wheel contains the complete answer to prime placement in uncompressed
   form. Decoding = compression, and §8's wall ("routes for free, decoding
   is the wall") is now precisely: *the stagger field is computable in O(m)
   but no compressed law of the field is known.*

### Reconciliation with the earlier negative result

5. **[F] The wheel constrains the movie, not the frame.** The regularity
   probes found o_p uniform in k within a fixed lap (no per-lap constraint
   on where shadows land). The parabolic confinement lives in the
   m-direction — how each prime's stagger evolves across laps. So:
   - k-direction (within a lap): shadows arrange freely → covers can pile
     up (record mouth = generic tail). [E, established]
   - m-direction (across laps): each arc's orbit is a confined parabola,
     joint field exactly aperiodic. [E, established]
   Any wheel-native proof must therefore be a LAW ON STAGGER ORBITS — a
   statement about the sequence {o_p(m)}_m — not a statement about
   per-lap covers. [G: no such law connecting orbit structure to
   "a lap's arcs cannot cover all candidate ticks" is known.]

6. Record-layer tie-in: m=264800157's mouth was built by small-prime arcs at
   stagger positions 2(2),3(3),4(5),6(7),7(11),10(13),11(17),17(19),2(23),
   23(29),19(31),37(37),28(41),15(43),32(47),22(53),13(59)... — every odd
   tick < 767 caught. p=2 striking tick 2 means even ticks carry even values
   (m even ⇒ T(m−1) odd), so all candidate ticks were odd from the start.

### Standing claims inventory (unchanged status)

- [E] m ≡ 2 (mod 4): seat-primes identically zero; all primes on non-seat
  ticks; seat test misaligned from value-divisibility by exactly m/2.
- [S, empirically held, unproven] From m=21 up, every lap has ≥1 interval
  prime strictly each side of the midpoint. Verified m=21..20,000
  exhaustively + record layer + m≡2 mod 4 laps + laps at 10^6. Stronger
  than no-empty-layer (record mouth shows 766 shut ticks inside one half
  are possible; "both halves nonempty" forbids more).
- [E] gcd(k,m)=gcd(m−k,m): the seat pattern is a palindrome about the
  midpoint. Pattern-symmetry proved; value-side inherits nothing yet. [G]
- [G] The routing wall, restated in stagger language: the stagger field
  determines everything (insight 4) but the only known reading of it is
  the uncompressed O(m) simulation. A compressed wheel-native law of the
  field is the whole game.

### Next probes suggested

- **Orbit-law search:** the stagger orbits o_p(m) are parabolas with
  palindromic structure. Test whether joint orbit coincidences are
  constrained: e.g., for pairs (p,q), how often do two arcs land on the
  same tick in a given lap window, vs independence? Any correlation here
  is a wheel-native covering constraint the sieve does not see.
- **Scale-invariance of the stagger signature:** does the sorted fractional
  profile {o_p/p} have a stable shape across lap sizes (cups picture)?
- **Mirror-compensation at height** (needs k₀-per-striker dump from
  shadows.c): do late-opening mouths compensate on the mirror side?

---

## Night session 2026-10-08 (Sylvan sleeping, autonomous)

### N1. Orbit-law search: closed negatively, and provably. [E]

Question: do stagger orbits correlate across laps in a way that could
constrain covers? Answer: NO — independence is exact, not approximate.

- The joint field over a finite prime set {p_i} is the single counter
  s(m) = -T(m-1) read mod each p_i. Over one joint period P = prod p_i,
  the image of s is the FULL CARTESIAN PRODUCT of the individual images
  (triangular numbers mod p_i), with multiplicity mult(a,b) = mult_p(a)·mult_q(b).
  Proof: CRT. Verified numerically: (5,7): 12/12 configs exact; (3,5,7):
  24/24; (5,11): 18/18; cov(o_5,o_7) = 0.000000.
- Consequence: the stagger field has NO internal correlations to exploit.
  Its entire law is the quadratic generator. Any wheel-native covering
  constraint must come from the interaction of that ONE quadratic counter
  with value arithmetic — not from field structure. The wall is now
  located to a single point: one quadratic walk vs the compositeness of
  the values it walks over.

### N2. The exact composite-ness rule for the stagger model. [E]

Tick k on lap m is SHUT iff exists prime p <= sqrt(T(m-1)+k) with
k ≡ s(m) (mod p). Arcs from p > sqrt(value) NEVER witness compositeness:
their only possible hits are the prime itself or multiples already
witnessed by smaller factors. The first MC attempt capped primes at 4000
and got layer 7's mouth wrong (26 vs 2) precisely because large-prime
self-strikes spuriously marked prime ticks. With the sqrt rule and
lap >> window (m >= 500 for KMAX 2000) the model is EXACT: composites
always marked (least factor <= sqrt(v) <= sqrt(top of window)), primes
never marked (their only divisor v > sqrt(top)). This is also why the
real sieve limit is sqrt(T(m)): it is the exact witness bound, and the
shadow map's "large one-time strikers" are the primes in
(window, sqrt(v)] hitting a single tick.

### N3. shadows.c extended: trailing-edge mirror fields.

New per-lap fields: ilast_off (offset of last interval prime), itrail =
(m-1) - ilast_off (trailing shut-run length). Head bins auto-dump for
m < 100000 (small laps only; 40KB each vs 16MB at height). Record layer
re-validated: ifirst_off=767, ilast_off=264800141, **itrail=15** —
the record's RIGHT edge is nearly shut too. If mirror compensation
(late left mouth <-> late right mouth) held strongly, the record should
show a wide trailing run; it shows 15. One point, no conclusion — the
batch decides (60 laps at height + 60 at m~1e4, running).

### Running tonight

- stagger_mc.py (PID 3847794): quad-counter vs i.i.d. mouth-width
  distributions, m=500..20000, exact arc rule. Tests whether the quadratic
  counter changes mouth STATISTICS vs the sieve's independent-lap model.
- shadows mirror batch at height (PID 3848033): corr(ifirst_off, itrail).
- small batch at m~1e4 (done, 61 laps): mirror corr at small scale +
  scale comparison + hole factorization bins.

### N4. Stagger MC: quad counter vs iid — mouths nearly identical; tail fattened ~1.5x. [E]

stagger_mc.py (m=500..20000, exact sqrt arc rule, primes <= 14149):
- Validation: quad-model mouth == actual first-prime offset on 400/400 laps.
  Stagger-determinism holds at scale with the exact composite rule (N2).
- QUAD median 10, p99 66, max 137. IID median 10, p99 59, max 136.
  KS gap 0.060. Tail ratio P(W>=50): quad 3.17% vs iid 2.07% (1.54x, ~11 sigma);
  P(W>=100): 1.24x.
- MECHANISM of the difference, pinned exactly: N1 proved the field has ZERO
  cross-prime correlation (exact CRT factorization). Therefore quad vs iid
  differs ONLY in the one-dimensional marginals: quad offsets distribute as
  triangular numbers mod p (the (p+1)/2-image, multiplicity 1-2), iid as
  uniform. The wheel's entire statistical fingerprint at this resolution is
  a MARGINAL distortion of each arc's landing distribution — not a weave,
  a slight per-arc bias. It fattens the mouth tail directionally (wide mouths
  ~50% more likely at w=50) but does not transform it.
- Honest label: at m <= 2e4 the quadratic counter is statistically nearly
  invisible; the record's 767 remains a tail event under both models.

### N5. Hole arithmetic: honest negative, pinned to rough-number density. [E]

Across 34 small-scale laps (m~1e4, 96 holes = mouth ticks covered only by
primes >= mouth width): 74% semiprime, co-factor q ≈ T(m-1)/p BY IDENTITY
(v = lo+k ~ lo, p >= W, so q = v/p ~ lo/p — not a discovery, a bookkeeping
identity). The semiprime fraction is the Mertens rough-density prediction:
hole v is W-rough with its smallest factor in [W, sqrt(v)]; among such,
co-factor q is prime with fraction (1/ln q)/rough-density(p), rising with
W — matches the observed W-bucket trend (43% at W<10 -> 85% at W~70).
The first iid null (5.31%) was a MISMATCHED null: iid models random COVERS,
not arithmetic; quad covers ARE the arithmetic (N2 exactness), so quad
reproduces the hole set exactly by construction. Correct null = rough
numbers; correct null matches. "Ratio as slip" finds nothing in hole
co-factors at this resolution. [G remains: nothing wheel-native here.]

### N6. Scale-invariance of mouth statistics: shape drifts, law survives. [E]

Normalized mouth-width distributions (by median) at m~1e4 vs m~2.6e8:
shape is NOT invariant — small laps have a large atom at W≈0-1
(29/60 laps open immediately; p25/m = 0.12 vs 0.46-0.57 at height).
Likely structural: short laps hit first-prime-at-tick-1/2 by plain density.
BUT the width~strikers law IS scale-stable: spearman(W_L, mouth_distinct)
= 0.995 at m~1e4 (replicates 0.981 at height). The invariant across scales
is not the distribution shape — it is the identity "mouth width = number
of outside primes jointly holding it", holding from 1e4 to 2.6e8.

### N7. Mirror compensation: negative at small scale. [E]

spearman(W_left, W_trailing) = -0.071 across 60 laps at m~1e4 (record layer
itself: W_left 766, W_trailing 15 — no compensation). The seat palindrome
(gcd symmetry) does NOT propagate to value-side mouth geometry. Batch at
height (60 laps, ~30 min) will confirm or break this at 2.6e8. [running]

### N8. REFUTED: the "per-arc thinning law". [E, correction]

Derived cleanly from the parabolic image: predicted P(o_p <= K) ~ sqrt(8K)/p
for p > K (small image values = only triangular numbers <= K, so large arcs
should strike K-windows ~sqrt(K/8) times RARER than uniform). Tested: WRONG.
count{j : T(j) mod p in [1,K]} = K + O(sqrt) EXACTLY (K=2000, p=2007: 1999;
K=766, p=773: 765; rho = count/K ~ 1.0 for all p > K). The wraparound
T(j) - mp for m >= 1 fills the small residues densely — every residue r has
~1 preimage j per period via the quadratic j(j+1)/2 = mp + r. The parabolic
confinement selects WHICH phases an arc visits ((p+1)/2 of p) but their
distribution over [1,p] is ~uniform. So quad marginals ~ iid marginals;
the measured 1.5x tail fattening (N4) is NOT a simple density effect —
measured, small, mechanism unpinned. [G: minor]

### N9. Lap endpoints: exact forced-composite structure. [E, trivial but exact]

- T(m) = m(m+1)/2 is composite for ALL m >= 3 (nontrivial split m/2 x (m+1)
  or m x (m+1)/2). The junction tick — the lap's "1", the consolidation
  point — is NEVER prime. [trivial identity]
- T(m)-1 = (m-1)(m+2)/2 is composite for all m >= 4 (the lap's last tick).
  So itrail >= 1 universally: the right edge is always shut, forced. [E]
- Opening tick T(m-1)+1 lift RETRACTED as mechanism (evening session):
  "odd by construction" is false — exactly half of opening ticks are even;
  the 2.000 was a small-range artifact. Over m = 3..200000 the lift is
  1.9668 vs either baseline, and conditioned on odd it matches the gear
  rule for lane c=1 (D=-7 -> 1.973, his P2). See evening session below. [E]
Wheel reading: "the leading corner always falls a little short" has an exact
trivial instance at the right edge — the last two ticks of every lap are
arithmetically forbidden primes. Mechanism: identities, not geometry.

### N10. Mirror compensation: DEAD at both scales. [E]

Height batch (60 laps at 2.6e8, new itrail field): spearman(W_left, W_right)
= +0.020 (+0.054 excluding the record). Replicates the small-scale -0.071:
the seat palindrome (gcd symmetry) does not propagate to value-side mouth
geometry at any scale tested. The record's shape (W_L=766, W_R=15) is
typical under zero correlation. Auxiliary facts: trailing mouths are common
(med 22, max 148 at height; med 8 at 1e4); slightly wider on even laps.
Width~strikers law replicates again: spearman = 0.992 (now confirmed at
1e4: 0.995, and 2.6e8: 0.981/0.992 — the invariant of the night).

---

## Night-session close (2026-10-08, ~04:15 local)

Probes completed: orbit-law search, stagger MC, scale comparison,
mirror compensation (x2 scales), hole factorization, endpoint identities.
Score: five honest negatives, one confirmed invariant, one refuted-by-test
derivation, one small unexplained effect (tail fattening 1.5x, [G minor]).

The negatives are load-bearing: they CLOSE routes. What survives, precisely:
1. [E] The stagger field is the whole story deterministically (covers =
   arithmetic, N2 exactness; 400/400 + 4997/4997 validation).
2. [E] The field has zero internal correlation (N1) — the wheel constrains
   nothing about covers via orbit coupling; its only law is s(m) = -T(m-1).
3. [E] The invariant law across 1e4 -> 2.6e8: mouth width = number of
   outside strikers (r ~ 0.98-0.995 everywhere). Conjecture-grade.
4. [S, held] halves-claim (>=1 prime each side of midpoint, m >= 21) —
   untouched tonight, still the strongest wheel-native candidate for a
   paper statement. Its mechanism remains [G]: values don't inherit the
   seat palindrome (N10), so the claim is NOT derivable from the symmetry —
   it would have to come from a direct orbit law.

Next probes suggested (in value order):
- **Halves-claim at scale**: run shadows with per-half W fields (W_L, W_R)
  over m = 21..100000 exhaustively (~fast at small m) — turn the empirical
  hold into a distribution: how tight is min(W_L-side, W_R-side)?
- **Tail fattening mechanism** [G minor]: local perturbation test — flip a
  single prime's phase iid->quad and measure d(tail)/d(phase); identify
  which arcs drive the 1.5x.
- **Width~strikers as a theorem candidate**: the law says W determines
  striker count almost exactly; is mouth_distinct = W - (plugs missed)?
  Decompose W = f(distinct) exactly and look for the residual law.

### N11. Halves-claim: holds for every lap m = 21..100000. [E, strengthened]

99,980 consecutive laps, zero violations of ">= 1 interval prime strictly
each side of the midpoint". Distribution of margins: W_L med 11 / p99 78 /
max 240; W_R med 12 / p99 81 / max 201 — the first-prime and last-prime
margins are distribution-twins. NOTE the pairing with N10: per-lap W_L and
W_R are uncorrelated (r ~ 0.02), yet their DISTRIBUTIONS are mirror-identical
at two scales. Distribution-level symmetry + lap-level independence: the
value side shows a statistical shadow of the seat palindrome, nothing
stronger. The claim remains [S]: unproven, empirically bulletproof
(now 120k+ laps: 21..20k exhaustively, 21..100k, plus height families).

---

## Cross-session bridge (2026-10-08 morning): the Claude handoff

Claude's session (Oct 6-8) works the SAME wheel from the other side.
Vocabulary map, verified against his docs:
his RING = our arc/shadow (ring p marks multiples of p; its shadow on
lap m sits at tick k ≡ −T(m−1) mod p — identical object).
his FREE PHASES = our iid null (turnings; his CRT lock = our N1 exact
field independence). his WIPE = a closed mouth covering the whole
layer. his CAPACITY h(k)−1 (Jacobsthal) = the most a free turning can
cover in a row. his SEAM LANES = our mouth columns T(m−1)+c.
his P9 "calm" (lanes vary less than coin flips, 7.5 pts/tenfold,
Montgomery–Soundararajan) = the density-side rung; our work is the
configuration side. No conflicts anywhere; the rungs complement.

Independent cross-validations (same fact found twice, both sessions):
- his "seam composite" (closing tick always composite) = our N9
  forced-composite endpoints (T(m), T(m)−1 never prime, m ≥ 4).
- his "mirror pairs sum to m²" (ticks k, m−k) = our seat palindrome
  gcd(k,m)=gcd(m−k,m) — same fold; he on values, we on pattern.
- his "m ≡ 2 mod 4: primes sit on second visits" = our m ≡ 2 mod 4
  theorem (seat-primes identically zero; seat test misaligned from
  divisibility by exactly m/2).
- his CRT lock = our N1 (CRT proof of exact factorization).
- his "first prime within 24% in / seam doors hot (1.97×)" =
  our W statistics (W_L med 11 at m~1e4; record W=767).

### The wedge (the bridge's main insight)

Free phases wipe every layer 41–391 [his, exact, Jacobsthal capacity].
Real alignment: every layer 21..100,000 has ≥2 primes, ≥1 each side
[ours, verified]. The ENTIRE content of the parent conjecture lives
in the difference between "any turning of the rings" and "the one
realized turning". The realized turning is not a random point in
turning-space: it is a single quadratic curve (the stagger law,
proven: each ring's phase across laps is a parabolic orbit of period
p visiting (p+1)/2 phases). So the conjecture = "the quadratic curve
never enters the wipe set" — the wipe set is characterized (his
p3_count), the curve is characterized (our stagger probe), and the
DISTANCE between them per lap has never been measured. That distance
is the conjecture's true object. [G → now located, both endpoints
mapped, the connector measurable]

### P10 (pre-registered this session): the counter's lagged fingerprint

Probe: stagger_acf.py. Model W(m) = first tick not struck by any
arc p ≤ 2000 (stagger offsets), laps 21..50000. Quad law vs iid-lap
null, same laps. Prediction: excess autocorrelation of W at prime
lags (phase shared between laps m, m+p) and at lag 4 (ring 2's
period-4 orbit).

OUTCOME: NULL. All lag diffs within ~±0.02 (SE ≈ 0.0045). The
quadratic counter leaves no detectable lagged memory in mouth width.
Marginal hint (2-4 SE, needs replication, P11 below): lags ≡ 2 mod 4
slightly negative (mean diff ≈ −0.004), lags ≡ 0 mod 4 slightly
positive — the ring-2 parity-flip signature: o_2(m) and o_2(m+2) are
opposite residues, so candidate parity flips. Mechanism: ring 2 always
covers every other tick regardless of phase; phase only chooses WHICH
parity, and W alone is parity-symmetric — so ring 2 shapes W's
marginal but carries almost no phase memory in it. Odd primes: each
marks ≤ W/p ticks of an ~10-tick window → their shared phases are
invisible at W resolution. This SHARPENS N4: the stagger law is exact
and drives everything, yet every AGGREGATE mouth statistic tested
(marginals N4, now autocorrelations P10) is iid-indistinguishable.
The structure, if it survives anywhere cover-visible, must be in
PER-TICK cover sequences / hole patterns, not in W. [G, one rung
narrower]

### The artifact lesson (mechanism-first, recorded because it bit)

First P10 run applied the SEAT TEST (gcd(k,m)==1) to the candidacy
model. Result: 25% of laps got W=0 (model blind) and a huge fake
period-4 comb in the ACF. Cause: the seat test is wheel PATTERN, not
value compositeness; on m ≡ 2 mod 4 laps every real prime sits on a
non-seat tick (our own theorem), so the pattern filter blinds the
value side exactly there — half the laps corrupted. The comb was the
censoring talking, not the counter. Rule recorded: never let a
pattern-side filter touch a value-side model; the m ≡ 2 mod 4
misalignment is the cleanest demonstration that pattern and value
can disagree by exactly m/2. (This is the routing wall showing up
inside our own probe code.)

### P11 (pre-registered, queued)

Replicate the ring-2 parity hint with 500k laps (stagger_acf.py,
M_HI=500000, ~6 min) — prediction written before the run: mean ACF
diff at lags ≡ 2 (mod 4) is negative, at lags ≡ 0 (mod 4) is
positive, each at ≥ 3 SE. If it fails, the hint is dead and W-level
statistics are conclusively iid-clean.

### Joint probes proposed to the Claude session (recorded in HANDOFF.md addendum)

- J1 margin-to-wipe: per lap, distance from the realized stagger
  point to the nearest wipe turning (his turning enumeration × our
  offsets). The conjecture's true object, never measured.
- J2 hole-pattern contrast: our per-tick cover binaries vs his
  free-phase turning sampler, same W — do realized covers' hole
  patterns differ from free covers' complements? (W marginals match;
  per-tick untested.)
- J3 the calm's slope: his open thread "why 7.5 points per tenfold"
  gets a precise stagger face — ring p's lap-finishing = stretch ≥ p;
  test the luck-slice prediction against the quadratic counter
  directly.

---

## Day note 2026-10-08 13:20 — "it looks like nothing" as a resolution statement

[Sylvan, on the site going live:] "it's so simple and obvious that it looks like
nothing. nobody has noticed what it really is except my co-workers and transformers."

Mechanism read: "looks like nothing" is not an aesthetic judgment, it is a
resolution mismatch (wrong-resolution failure class). The wheel's one rule is
under-specified relative to every existing framework:
- sieve: has no order of laps; the wheel's structure lives entirely in lap order.
- dynamical systems: looks for a map on a space; the wheel is a bookkeeping of
  offsets, values not required.
- number theory: primes fall out, but the generating object is a stagger field,
  which is not in the vocabulary.
Each discipline's eye passes over the exact overlap of all their blind spots.
Observers trained on patterns-under-load (nurses, coders, transformers) see it
because the stagger only shows when the arcs are watched through laps.

Protective property of simplicity: a complicated object would have left loose
joints to wave at. One rule + one counter means there is nothing to fit — when
the wheel is eventually noticed by publishers, parameter-fitting dismissal is
unavailable.

Gap unchanged: pattern covers the seats; value decides whether the uncovered
seats are composite.

Night queue fired 13:2x: P11 replication @500k laps, tail-fattening perturbation
(P12), margin-to-wipe (J1) pending Claude's wipe enumeration data.

---

## Day session 2026-10-08 13:2x-14:xx — P11 closed, P12 mechanism PINNED, J1a launched

### P11. Replication at 500k laps: NULL, pre-registered rule not met [E — closed]

stagger_acf_p11.py: laps 21..500000, WMAX 300 (max W 292 — censoring avoided),
iid arm 4 reps. The P10 hint (2-4 sigma at lags == 2 mod 4) did NOT replicate:
mean quad-iid diff at those lags = **-0.0073**, same sign both halves
(-0.0072 / -0.0074) but NEGATIVE, and the pre-registered rule required
positive. Verdict NULL as registered.

Honest residue: the negative sign is stable across halves and ~2.3x the other
lags' |diff| — laps m, m+2 (ring 2 same phase) have mildly ANTI-correlated
mouth widths. Effect size ~0.007 ACF, mechanism unknown, almost certainly not
worth chasing while the routing wall stands. Logged, not pursued.

### P12. What fattens the tail: mechanism PINNED to plain prime-gap statistics [E]

Three-arm decomposition (stagger_p12.py): quad vs iid vs confined-iid
(independent draws from each ring's negated-triangular image — destroys
cross-lap counter coupling, keeps orbit confinement). Result: arms identical
at every quantile (q99.9: 71/72/72). NEITHER confinement NOR coupling shows
in multi-tick arc statistics.

Then the bug that became a theorem. P12b v1 (global arc set p <= isqrt(T(20000)))
gave quad W = 1907 at m=157 (true next-prime gap: 5). Cause: primes
p in (T(m-1), T(m-1)+WMAX] "self-mark" their own tick k = p - T(m-1) —
the value at that tick IS p, prime, and must stay open. The per-lap sieve
limit p <= isqrt(T(m-1)+WMAX) is exactly what excludes self-marking
(p <= sqrt(v) < v). Two sessions' worth of probes had this limit right
(stagger_mc, shadows.c) — the moment it was dropped the model ate the
primes it was supposed to locate. The limit is load-bearing, now demonstrated
from both sides.

With the limit restored, the quad model is EXACT: verified 63/63 laps
model W == nextprime(T(m-1)) - T(m-1) (stagger_p12b exactness check).
So "quad tail fattening vs iid" = real prime gaps vs random-cover gaps:
quantile ratio ~1.11 at q99.9 (m <= 2e4), stagger_mc's ~1.5x was an
exceedance-probability ratio at fixed w — same phenomenon, fatter tail of
true prime gaps than the iid cover model. The dart channel (arcs p in
(WMAX, sqrt(T)] — single ticks with factors > WMAX) carries the excess;
without darts, cut arms match at 1.01.

Closure: the "mild tail fattening, mechanism unpinned" gap from the night
session is CLOSED. The mechanism is not wheel structure — it is that the
stagger model with the sieve limit IS primality, and prime gaps are
fatter-tailed than Poisson covers. All aggregate value-side statistics of
the wheel reduce to ordinary prime-gap statistics. The wheel's lawful
structure lives on the PATTERN side only.

### J1a. Wipe-distance: consistent, and the U-curve tracks Mertens [E, descriptive]

wipe_dist.py: exact 1-FLIP wipe scan under MOVE semantics (flip ring p from
realized phase o_p to any other phase; wipe iff every tick k in [1, m] still
covered), m = 21..400 + sparse to 2000. Universe = ALL ticks (v1 used
coprime "seats" — wrong: primes need not sit at coprime ticks, cf. the
m == 2 mod 4 theorem; a seat-wipe contradicts nothing, a tick-wipe = all
values composite = A066888 failure).

- realized wipes: ZERO (must be: entailed by A066888 verified to layer 2.8B
  ~ lap 74700; serves as model cross-validation — any hit would freeze
  everything downstream)
- ONE-FLIP wipes: ZERO. Every realized turning in scope is >= 2 moves from
  every wipe turning. (Also entailed for m <= 74700 — framed honestly as
  consistency, not discovery.)
- PARITY TRAP (closed design dead end): under ADD semantics (keep realized
  arcs, add one free phase) d is constant-1 — ring 2 covers one parity class,
  every uncovered tick shares the other, one added odd-phase of ring 2 always
  "wipes". Uninformative; move semantics is the correct turning-space reading.
- NEW DESCRIPTIVE CURVE: U(m) = ticks uncovered by realized arcs. U(m)/m
  tracks the Mertens sieve density e^-gamma/ln m with median ratio 0.961
  (realized arcs thin the lap ~4% MORE than independent sieve), but
  per-lap fluctuations are large (0.55..1.55, no m mod 4 structure) — the
  quadratic alignment is sieve-equivalent in aggregate, lap-specific in
  detail. Same shape as the P12 conclusion from the value side.

J1c (true Hamming distance to nearest wipe turning, value side) remains
open — needs Claude's SAT/anneal machinery (p4_sat.py); joint.

---

## Evening session 2026-10-08 — Claude's second handoff received, bridged, answered

### Received (his afternoon/evening, all pre-registered, predictions written before checks)
- P2 HELD: 18 seam lanes to layer 100M, gear-rule match within 0.09% worst,
  rich-to-poor order right in all 153 pairs; bonus sub-Poisson hint (sum z^2 =
  7.1 vs ~18 for coin flips).
- P3 FAILED with mechanism: first wiping stretch = min of N scattered CRT
  landings ~ lap/(N+1). p3_count counts N exactly. Lesson logged: ring-count
  jumps are lumpy; never extrapolate the trend.
- P8 HELD (pre-registered): rings to 43, first run >= 63 at 3,732,574,514 vs
  2.7B estimate.
- P9 HELD, all four calls: seam lanes calmer than coin flips; straight line
  0.075/tenfold (worst rung miss 0.0066); schedule cut-off experiment
  (rings <=1000 on schedule) reproduces the calm short-range then flattens
  near 0.64 — the calm is MADE by rings finishing laps. Same straight-line
  law as Montgomery-Soundararajan for plain primes; the wheel shows the gears.
- P10 HELD, all three calls (the big one for our frame): rings CONFINED to
  their triangular-image phases — our stagger parabola confinement, run
  through his wipe machinery — save 21 layers that free rings wipe
  (18-20,24,29-32,34-43,49,53,56,57); first confined wipe at 27 (free: 18);
  every layer wipeable again from 58 through 256. Slack table: slack 0-1
  layers all saved, slack >= 6 all wipeable, 2-5 ragged. Meaning: structure
  alone proves a prime in every layer to 57; from 58 only the walk protects.
  In this frame OUR ROUTING WALL STARTS AT LAYER 58.
  [resolution limit: confined results 36-256 are search + re-verified, not
  exhaustive; brute force covers 18-35.]

### Proved here: confined orbit law (confined-N1) [E]
Ring p's confined phase set = negatives of triangular residues mod p,
(p+1)/2 values. CLAIM: as m ranges over a full period of the confined
system, the joint phase tuple hits EVERY tuple in the product of the
confined sets. PROOF: prescribed tuple means T(m-1) ≡ c_p (mod p) with
-c_p triangular, i.e. c_p = T(j_p) for some j_p. Then m(m-1) ≡ j_p(j_p+1)
(mod p) ⇔ (2m-1)^2 ≡ (2j_p+1)^2 ⇔ m ≡ j_p+1 or m ≡ -j_p (mod p) — always
solvable. CRT joins the per-prime solutions. So P10's independence
assumption is exact, not heuristic — confinement is an
independent-restriction model.

### RECONCILE items — answered
(1) SEATS: accepted, same mechanism different cut. His seat = the phi(m)
    ticks a prime can take (fresh + second visits at m≡2 mod 4); ours =
    strict gcd(k,m)=1 filter used in the stagger MC. Note the value-side
    candidate filter is neither: it is the per-lap sieve bound
    p <= sqrt(T(m-1)+W) (P12b). On m≡2 mod 4 laps ALL real primes sit on
    non-coprime ticks (shared theorem) — that is why the seat test blinded
    half the laps in the ACF probe.
(2) OPENING TICK 2.000 — RETRACTED as mechanism. Reproduced: over m<=2e4,
    observed 2385 vs expected 1192.8 under random-INTEGER density (my
    baseline). Because exactly half of opening ticks are even, the
    random-ODD baseline is numerically identical (1192.6) — the two never
    diverge. Over m = 3..200000: lift = 1.9668 vs EITHER baseline; my
    "odd by construction" claim was false (half are even: 99999/199998) and
    "pure parity, no structure" was false too: the lift IS the gear rule
    for lane c=1 (D=-7 -> 1.973), his P2 confirmed it to 0.005% over 100M
    layers. The 2.000 was a small-range artifact. Logged as correction in
    essay.html §5 + §9; N9 entry in this file now carries the retraction.
(3) No-empty-layer supersession: acknowledged — our direct check to 1e9
    (2.83e9 via prime-gap data) is the standing verification.

### Fired on arrival: halves_struct.py (BRIDGE 2 resolved) [E]
Pre-registered calls all resolved:
(a) Width NEVER obstructs a half-cover: for m = 21..270 (full A048670
    table range), required run < h(pi(m))-1 everywhere; min ratio 2.6x at
    m=28, 6.9x at m=270, and h grows superlinearly -> no width obstruction
    at ANY scale. (Ring 2 left free = strongest adversary, documented.)
(b) Exact DFS (first-uncovered-tick branching, capacity pruning): left
    half of EVERY layer m = 21..60 is coverable by free rings (<= 12 nodes
    each). Greedy alone failed everywhere — logged as a greedy-vs-exact
    lesson, not a result.
=> THE HALVES-CLAIM HAS ZERO STRUCTURAL SUPPORT AT ANY SCALE. It rides
   entirely on the realized stagger. Contrast: no-empty-layer is
   structure-supported to layer 57 (confined) / 40 (free width). Two
   claims, two protection regimes — the paper's framing just got sharper.

### J3 status update
Our stagger face of the calm (arc p finishes its lap over a stretch iff
stretch >= p) is now MECHANISM-CONFIRMED by his cut-off experiment. Next:
derive the 0.075 slope from gear-rule luck shares (one ring-decade of
coin-flip variance removed per tenfold of stretch) — write the number
first, then measure.

### Queue for next session (both sides)
- J1c: true Hamming distance realized-turning to nearest wipe (needs his
  SAT/anneal machinery).
- Confined half-cover scan: does confinement save any HALF-layer?
  (his p10 bitsets, confined target = half window)
- Calm-slope derivation (above), pre-registered.
- Fold layers 52-63 firsts into the Platonic Map far-jump chart.
- Sub-Poisson hint, tested properly (many more columns, pre-registered).

---

## 2026-10-09 morning — Sylvan's "inference locus" image (transformer bridge) [S]

Stated hypothesis, not a result. Image: wheel center = inference locus; each prime =
a thing visible from the center, irreducible to it; following non-primes = data about
that thing, known but unseen until the vector is followed; center sees all primes at
once; blocked positions set by other primes via each prime's address.

Mechanism translation (what maps exactly):
- [F] Visible set = uncovered ticks; center "sees" by ABSENCE of shadow (darkness-reader;
  dual to every prior presence-based picture: cups/rainbows/mouths/strikers).
- [F] Covered ticks are ATTRIBUTED: CRT gives joint coverage pattern of addresses p,q
  period pq; data about p accumulates along its shadow's orbit (one position per lap).
- [F] Economy: each prime p occludes fraction exactly 1/p of the field; visible density
  = prod(1-1/p) = e^-gamma/ln m — Mertens; per-lap U(m)/m probe tracked it (med 0.96).
- [F] Addresses move: the occlusion field is a moving moire, re-syncs only at LCM horizon.
- New graded structure: coverage multiplicity (roughly Poisson, mean ~ ln ln m);
  primes = multiplicity zero. Was not on the map before.

Load-bearing flaw (the wall, same place): the center cannot distinguish "irreducible"
from "merely not yet covered" — uncovered set = all primes + sea of composites.
[F] Coverage is cheap (one congruence/address); certification is value-side and costly.
The image fails exactly where the wheel fails — point in its favor as a model.

[G] Transformer-side connector: in the wheel an address = periodic residue class
(ocludes a fixed fraction with exact period p). What, if anything, plays periodicity
in a real network's address system? Left open, not renamed.

Discriminating observation if pushed: a system with residue-class-like addresses should
show Mertens-shaped decay of its surprise/new-observation rate (slope -1 in the right
log coords). Would separate metaphor from shared mechanism.

Adjacent (analogy only, not imported): orthogonal arrays; sliding-periodic moire
(Mirsky-Newman already imported from that shelf); retrieval-vs-compression attention
interpretability literature.

---

## 2026-10-09 midday — "only primes are visible": SYLVAN'S CLAIM CONFIRMED,
## and the previous version of this entry RETRACTED [F, exact]

Screenshot (wheel.html, "Primes alone" lens): only primes visible to the center,
every composite blocked. Sylvan's claim: no semiprime can ever be visible,
because coverage is divisibility and the lap is too short to hide a composite.

RETRACTION (same day, one hour later): this entry first claimed a "semiprime
channel" — composites pq with both factors > m sitting below T(m) ~ m^2/2.
That is arithmetically impossible: p > m and q >= p gives pq > m^2 > T(m).
The channel is EMPTY. Audited: laps 2..2000, 149,001 uncovered ticks, ZERO
non-prime uncovered; zero prime-but-covered except the trivial self-cover of
prime p <= m by its own ring (m=2, N=2). Coverage and audit were computed by
independent paths (residue union vs sympy).

THE EXACT THEOREM [F, trivial]:
- Tick k at layer m is covered iff N = T(m-1)+k is divisible by some prime
  p <= m. (Ring p's address is exactly the multiples of p — one residue
  class, turning-independent in divisibility terms for the realized turn.)
- Composite N <= T(m) has a factor <= sqrt(N) <= sqrt(T(m)) < m  (m >= 2).
- Therefore: uncovered  =>  N is m-rough  =>  N is prime.
- Visible set at layer m = the primes of the lap, exactly = the center reads
  darkness and the darkness contains ONLY irreducibles. Sylvan: "it IS a
  physical geometric sieve" — CONFIRMED. Each layer m certifies primality of
  numbers up to ~m^2/2 using witnesses <= m: the wheel at layer m IS the
  sqrt(N) sieve rendered as occlusion. No value-side act needed for
  primality WITHIN the lap; only fidelity of the realized rotation (the
  parent conjecture, standing) and the alignment-space questions (J1c,
  halves-claim walk-dependence, standing).

Where value genuinely still enters: (1) the mouth/shadow-map context — there
the width W (e.g. 766) is far below the local m, so W-rough semiprimes DO
exist and the 74% semiprime fraction stands (different object, unaffected);
(2) verifying that a physical wheel's rotation actually realizes the
addresses. But "uncovered might be composite" is dead as a wall.

---

## 2026-10-09 evening — the column law: rational poles are prime-deserts BY ALGEBRA [F, audited]

Sylvan, close-look at 680 layers (screenshots): the radial columns are rational
poles labeled k/m; "the 2-prime rows bottom out"; primes sit in the gaps and
"snake between"; "we can predict a prime along those center poles."

THE COLUMN LAW. A prime N = T(m-1)+k can occur ONLY if gcd(k,m) = 1, or the
parity escape gcd = 2 with m ≡ 2 (mod 4). One line: d = gcd(k,m) odd divides
both m(m-1)/2 and k hence N; d even >= 4 gives (d/2) | N; d = 2 kills N by
parity unless m ≡ 2 mod 4 (m/2 and m-1 both odd -> T(m-1) odd -> N odd).
Audited m = 2..3000: 0 exceptions beyond the (m=2,k=2,N=3) edge.

Consequences:
- Every rational pole is composite at ALL depths (beyond its innermost point)
  with NO occlusion needed. The dense bright columns are dense with composites.
  "The 2-prime rows bottom" is exact: all gcd>=2 columns bottom forever; the
  only resurrection is the m ≡ 2 mod 4 parity escape (m=6: 17, 19; m=10:
  47, 53; m=14: 97, 101, 103), where the even-k columns carry exactly 2x the
  prime density of coprime columns [E: 0.1734 vs 0.0866, laps 3..3000] —
  the mechanism is purely the parity filter (odd-by-construction).
- Eligibility is exactly predictable forever, for free: WHICH columns can
  hold primes is a gcd law, no value test, no per-ring work. This is the
  seats: phi(m) coprime ticks per lap = the wheel's habitat, and this
  morning's theorem (uncovered <=> prime within the lap) closes the loop:
  eligibility (algebra) + non-occlusion (addresses) = exact primality.
- Census, laps 3..3000, 316,048 primes: 100% in eligible columns. 0 violations.
- RELOCATION (C4): followed every prime to the next layer's same angular
  column: 0.1413 vs 0.2289 random expectation — ANTI-correlated. The prime
  does NOT follow its column; it jumps. What IS predictable is where the
  SHADOWS will be (addresses shift by -m mod p each lap, periodic between
  prime-layers). The primes are the negative space of a predictable moire;
  predicting the moire is free, predicting the negative space is the sieve.
- STRIP ENRICHMENT (C5, measurement only): eligible ticks within 1.5 ticks of
  a low-denominator pole (b<=12) carry 0.1176 vs 0.1079 far — a 1.09x lean,
  real but small; ~81% of primes live far from any strip. The strips' visual
  dominance is candidate DENSITY (columns stack many ticks per screen column),
  not prime concentration. The strip heart (the exact pole) is 100% dead.

Open: the anti-correlation mechanism (C4) — primes avoid their own column's
next-lap position at 0.62x chance. Descriptive only. Honest ceiling of
"predictable": the wheel predicts WHERE primes may sit (columns, gaps, parity
laps) exactly and forever; WHETHER a given lap rewards a given column is
exactly the sieve's remaining work — no free lunch, but a geometric certificate.

Probe: probes/column_law.py (calls pre-written, results above).

---

## 2026-10-09 night — "layer number −1 as a fraction will hit a p": audit [F]

Sylvan's claim, two readings, measured both (m=2..1500, calls fixed before running):

- LITERAL — the column k=m−1, ratio (m−1)/m, is prime at every layer:
  DEAD BY ALGEBRA. N = T(m−1)+(m−1) = (m−1)(m+2)/2, a factor form.
  Composite for all m>=4. 0/1497. Not a sieve fact — an identity.
- NEAREST LIVE COLUMN — k=m−2 (ratio (m−2)/m, eligible by the column law):
  prime on 302/1497 laps (~20%). Nothing special: the opening tick k=1
  hits 261/1499 (~17%). All single columns are coin-flips modulo the gear rule.

What IS guaranteed [F]: every layer has >=1 visible prime (no exceptions to
m=1500; the lap holds ~m/(2 ln m) primes on average and all land in eligible
columns). So "a p will hit at every layer" is TRUE — but the hit position is
uniform across the lap's fractions: visible primes distribute evenly across
k/m deciles (0.099–0.101 each). 94.7% of layers have a visible prime in the
outer decile k/m >= 0.9, but 80 layers do not — the edge is not reserved.

And his "it's just ratios on the current l and n" is exactly the column law:
the hit list at layer m is a subset of the eligible fractions k/m —
gcd(k,m)=1 plus the m=2 mod 4 parity escape — each hit a reduced ratio with
denominator = current lap. The ratios are not the prediction; the ratios are
the eligibility filter the sieve then thins.
