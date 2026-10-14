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

---

## 2026-10-09 night — claim audit: "999999/1000000 at l=1000000 is prime" [S → REFUTED, F]

Sylvan: the ratio 999999/1000000 at lap m=1000000 decomposes to a
prime without checking. The identity decides it before any test:
k = m−1 is the dead rim column — N = T(m−1)+(m−1) = (m−1)(m+2)/2,
composite at EVERY layer m >= 4 (same forced-composite family as k=m).

  N = 500,000,499,999 = 999999 × 500001 = 3^4 · 7 · 11 · 13 · 37 · 166667
  isprime: False. Rim audit at this lap: k = 999997,999998,999999,1000000
  all composite.

What the lap actually pays nearby: 500,000,499,959 = ratio 999959/1000000
(prime, same lap), and 500,000,500,001 = T(10^6)+1 = opening tick of lap
1000001 (prime — an opening-tick coin that paid this time).

Lesson restated: fixed fractions are gears, not promises. The predictable
columns are the DEAD ones (k = m−1, k = m, gcd >= 2 columns); primality
at an eligible column is exactly the coin the sieve still flips.

---

## 2026-10-09 night — "the ratios land exact every time": THE TRIANGULAR-OFFSET THEOREM [F, exact]

Sylvan, "Every number" lens (~l594-600): the labeled dots fall on persistent diagonal
lines. Claim: the ratios land exact every layer, proportional.

MECHANISM: a dot can recur EVERY layer iff its N is a polynomial in m with a closed-form
factorization — because then nothing needs to be tested. The diagonal lines are exactly
the linear families k = m - c, and:

    N = T(m-1) + m - c = (m^2 + m - 2c)/2 = (m-j)(m+j+1)/2  iff  c = T(j) = j(j+1)/2

So the PURE-composite diagonal lines sit at offsets that are triangular numbers:
  k=m-1:  N=(m-1)(m+2)/2      k=m-3:  N=(m-2)(m+3)/2
  k=m-6:  N=(m-3)(m+4)/2      k=m-10: N=(m-4)(m+5)/2   k=m-15: N=(m-5)(m+6)/2

AUDIT (m=20..1500, calls written before running):
  all five triangular offsets: 0 primes, zero exceptions.
  every non-triangular offset c in {2,4,5,7,8,9,11,12}: carries primes (7-20% rate).
  i.e. the pure lines are EXACTLY the triangular offsets.

Same picture as always, one level deeper: the predictable positions are the dead ones,
and their addresses are the triangular numbers. The "proportional" drift (k/m -> 1) is
just c/m -> 0: all pure lines converge at the rim. The k=m-2 line (c=2, non-triangular)
is a real coin line at 0.243 enriched by the parity escape (m=2 mod 4).

---

## 2026-10-09 late night — the variable tread: lap ratio as a playable dial [S→built]

Sylvan: the wheel scales 1:1 (lap m brings m ticks); he wants to set the lap
length to any ratio — 1:1.1, 1:2, 2:1 — and play with the spiral that results.

Engineering call: the invariant "lap m has m ticks, N = T(m−1)+k" is woven
through every subsystem of index.html (flat tick-index, found[] line-tracking,
PI_T prefix arrays, sieve verdict, slip, Collatz). Changing it in place is a
refactor, not an edit. So the variable version ships as a separate playground
page, variable.html — the canonical wheel untouched.

Mechanics of the toy, stated exactly:
- Lap m lays L(m) = max(1, round(m·r)) ticks; base(m) = Σ_{j<m} L(j); tick k
  of lap m is the integer N = base(m)+k. Numbers keep their order; only the
  lattice reflows.
- WHAT SURVIVES [F]: primality and divisibility are properties of the integer.
  Gold still means prime; "cut by q" still means q | N — at any ratio.
- WHAT DOES NOT SURVIVE [G→open]: the column law and the triangular dead-lines
  were theorems about the 1:1 lattice (base = T(m−1)). At r ≠ 1 the eligibility
  algebra re-derives from the new base — that re-derivation IS the toy.
- Geometry mirrors the fixed-circle frame: ang(frac) = −π/2+2π·frac, radius
  (m−0.5+frac)/2π, seam up. Hit-test inversion audited 0/24000 mismatches
  across r ∈ {0.5, 1/1.1, 1, 1.1, 2, π}; r=1 reproduces T(m−1) bases exactly.
- One bug caught pre-ship by the roundtrip audit: lap inference from radius
  must be round(r·2π − ε), not round(r·2π + 1/2) — the latter assigns half of
  every lap to the wrong lap.

Discriminating observation the toy makes possible: at which ratios, if any,
does the visible-set structure (primes = uncovered-by-small-wheels) re-form
into clean lines? The 1:1 lattice's theorems are one point in ratio-space;
whether any other ratio has its own algebra is now a probe-able question.

---

## 2026-10-09 deep night — the ratio sweep: 165 ratios, 5M sieve, four laws

Probe: probes/ratio_sweep.py. Wheel rules as in variable.html: L[m] = max(1, round(m·r)),
N = base(m)+k. Families scanned: k = round(f·L[m])+b for f = j/48 (j=1..48), b = −20..+8,
m ≤ M with base(M) ≤ 5e6. Rational grid a/b (a,b ≤ 16, coprime) + irrationals (√2, √3, √5, π, e, φ, ln2, √2−1) + extremes (1e±2..1e±6).

**L1 — no all-prime line exists anywhere in ratio space [F, zero instances].** 165 ratios ×
~1400 families ≈ 230k family scans: ZERO families with ≥8 samples 100% prime. At rational r the
obstruction is exact (N(m) is a quadratic quasi-polynomial; a nonconstant such sequence takes
composite values). The "always p on a line" pattern is not hiding at any ratio.

**L2 — rational ⟺ has dead lines [E, measured].** Pure-dead families (0 primes, ≥40 samples,
expectation ≥4) at EVERY rational a/b tested — always including f=1 (rim) families — and at ZERO
irrationals. r=1 reproduces the triangular theorem exactly: dead at b = −1,−3,−6,−10,−15 (f=1).
Non-integer rationals have their own dead offsets (1:2 → f=0.5 b=−1,−5,−17; 2:3 → f=1 b=−4,−10,−16).
The exact indexing formula for dead offsets at general a/b [G].

**L3 — the parity escape is universal [E, 2.00× exact everywhere].** At every ratio, the
(m mod 4 × k parity) classes where N is forced odd carry exactly 2.00× prime density; classes where
N is forced even are prime-deserts. Not an r=1 quirk — a constant of the whole tread family. The
"sweep's m%4==3 dead annotations" were these parity-desert classes, not new structure.

**L4 — seam (cumulative totals base(m)) laws [F + E].** Integer r: base(m) = r·T(m−1) exactly →
seam composite ∀m≥3 (r=1: except T(2)=3; r≥2: except N=r at lap 1). 10:3 worked in full: k≡0 mod 3
→ even and ×5; k≡1 mod 3 → even; k≡2 mod 3 → divisible by 3 — every residue class killed, seam dead
except base(2)=3. Non-exceptional rationals (3:2 etc.): seam prime-normal ~7%.

---

## 2026-10-09 — the lock probe (Claude's challenge: what survives at 2:3, 3:4?)

Question: the 1:1 wheel's "lock" (spokes, visit lock, dead seam, parity axis) — is 1:1 the
only ratio that has it, and if not, which facts survive where? (`probes/lock_probe.py`, f1989ef)

**Clean-lap law [F→measured].** A lap "closes clean" when it starts at the seam or exactly
half a turn from it: 2·B[m] ≡ 0 (mod L[m]). Claude's mechanism is right but not 1:1-specific:
- every INTEGER ratio closes clean on ~every lap (r=1,2,3,1000000 all 2 start phases)
- at r = a/b reduced, the clean fraction is 1/b, and the lap start hops among finitely many
  phases (b=1,2 → 2 phases; b=3 → 6; b=5 → 10; b=4 → 5–6) — the "leftover" never wanders
  continuously; it cycles. The partial lock is periodic, not chaotic.

**Dead seam + full parity escape ⟺ denominator is a power of 2 [S, observed on 13 ratios].**
Seam is prime-dead and the (m%4 × k-parity) classes hit exactly 2.00×/0× at r = 1, 2, 3,
3:2, 5:2, 7:4 (denominators 1, 2, 4). At odd denominators (2:3, 5:3, 3:5) the seam has
hundreds of primes and the escape dilutes to 1.33×/0.67×; 3:4 concentrates the escape in
m%4∈{1,3} classes only. Mechanism: N's parity/divisibility pattern needs B[m] mod small
numbers to cycle with period 4; odd denominators break the alignment. Open: test 3:8, 5:8,
7:8 to confirm the power-of-2 boundary.

**Dead rays survive everywhere rational** — with the m%12 class split, every a/b tested has
pure-dead families (3:4: 396, 2:1: 2208, 1:1: 1092). Consistent with the sweep's L2.

**r=2 is the Ulam spiral, verified exactly [E→import].** Squares sit at frac 1/2 (k=m,
N=m², dead-adjacent seam ray); Euler's n²−n+41 is the FIXED TICK k=41 and breaks at m=41
exactly as the theorem says; the n²+n+41 diagonal is the constant seam offset k=2m+41
(211/300 primes for m<300) vs N=m²+41's 12/300 — the prime-rich Ulam diagonals are
constant-offset spirals converging on the square ray. Claude's "primes fall along curved
diagonals" = fixed offsets from the seam.

**Corrections to the probe's own framing [G acknowledged].** (1) Residue classes were never
frac-locked — R ≈ 0 even at r=1; the 1:1 lock lives in the gcd(k,m) line lattice, not in
residue positions. (2) "≤2 primes per spoke" could not be tested here: geometric frac-rays
hold hundreds of primes at every ratio; the eight-facts "spokes/lines" are a different object
(the wheel's line/visit structure) that a frac-ray scan cannot see.

---

## 2026-10-09 dusk — THE TERRITORY MAP: full inventory + the jungle queue

Consolidated inventory of everything standing, organized for traversal. Labels as
usual. This entry is a map, not new results.

**A. The deterministic core (1:1 wheel, machine-verified)**
- A1 [E] Stagger field is the whole story: covers = arithmetic, exact
  (4997/4997, 400/400). Wheel contains the complete answer to prime placement
  in uncompressed form; decoding = compression, and no compressed law is known.
- A2 [E] Zero internal correlation of the field (CRT, exact factorization).
  The only law is s(m) = −T(m−1). The wall is located to one point: one
  quadratic walk vs the compositeness of the values it walks over.
- A3 [E] Parabolic confinement: each arc period p, (p+1)/2 phases, palindromic;
  never sweeps uniformly.
- A4 [E] Exact aperiodicity: joint field period ≈ e^{p_r} — never repeats
  physically.
- A5 [E] Width~strikers invariant: spearman 0.98–0.995 from m=1e4 to 2.6e8.
- A6 [E] ALL aggregate value-side statistics tested are iid-indistinguishable
  (N4, P10, P11). Lawful structure lives on the pattern side only; value side
  reduces to plain prime-gap statistics (P12).
- A7 [E] U(m)/m tracks Mertens with median ratio 0.96.

**B. The exact-theorem cluster (1:1, audited)**
- B1 [F] Uncovered ⟺ prime within the lap: visible set = primes EXACTLY.
  The wheel at layer m is the sqrt(N) sieve rendered as occlusion.
- B2 [F] Column law: prime ⟹ gcd(k,m)=1 or m≡2 mod 4 parity escape.
  Eligibility is a free gcd certificate forever; 100% of 316k primes in
  eligible columns, 0 violations.
- B3 [F] Triangular-offset theorem: pure-dead diagonals EXACTLY at c=T(j);
  every non-triangular offset is a live coin line.
- B4 [F] Forced-composite endpoints: T(m), T(m)−1 never prime (m≥3/4).
- B5 [F] m≡2 mod 4 theorem: seat-primes identically zero.
- B6 [E] Parity escape: 2.00× density exactly, mechanism = pure parity filter.

**C. Held but unproven [S]**
- C1 Halves-claim: ≥1 prime each side of midpoint for all m≥21.
  [S, Legendre-hard by reduction — see 2026-10-10 overnight; paper value
  migrated to the wedge-distance instrument F2]. 1M laps, zero violations.
- C2 No-empty-layer: structure-supported to layer 57 (confined), walk beyond.

**D. The ratio-dial era (variable tread, probes + toy)**
- D1 [E] L1: no all-prime line anywhere in ratio space (230k scans).
- D2 [E] L2: rational ⟺ dead lines exist; irrationals structureless. r=1's
  triangular offsets are one instance; every rational has its own.
- D3 [E] L3: parity escape universal at exactly 2.00× at every ratio.
- D4 [F+E] L4: integer ratios → dead seam by algebra; 10:3 cracked fully by
  residue-class kills.
- D5 [F] Clean-lap law: closure fraction = 1/b at a/b; leftover hops among
  finitely many phases — partial lock is periodic, never chaotic.
- D6 [S, 13 ratios] Dead seam + full escape ⟺ denominator a power of 2.
  Open: 3:8, 5:8, 7:8 confirmation.
- D7 [E] r=2 = polar Ulam spiral: squares at frac 1/2; Euler n²−n+41 is the
  fixed tick k=41, breaking at m=41 exactly; Ulam prime diagonals =
  constant seam offsets k=2m+c converging on the square ray.
- D8 [F→E] Dead-offset classification at general a/b — CLOSED FORM FOUND
  2026-10-10: Δ(r) degree ≤ 1 by structural r²-cancellation; dead classes =
  square-Δ ∪ content-killed, O(b) exact arithmetic, sieve-free. Residual
  openness only on (a,b)-parameterized compression (Dedekind-sum-like) and
  Layer-1 one-sidedness. See 2026-10-10 overnight.
- D9 [G] Claude's "≤2 primes per spoke" untestable via frac-rays; it lives
  in the gcd(k,m) line lattice, not geometric rays.

**E. Honest negatives (closed routes — load-bearing, do not reopen blind)**
- E1 Orbit correlations: none exist (CRT). E2 Holes: rough-number density.
- E3 Mirror compensation: dead at both scales (r≈0.02). E4 Per-arc thinning
  law: refuted by test. E5 Lagged fingerprints of the counter: null (P11).
- E6 C4 relocation: primes ANTI-follow their own column (0.62×) — mechanism
  open, descriptive only. E7 C5 strips: 1.09× lean, visual dominance is
  candidate density, not prime concentration.

**F. The standing wall [G]**
- F1 Routing wall: pattern covers seats; value decides composites. Stagger
  field computable in O(m), no compressed law known. (Within-lap instance
  CLOSED by B1; the mouth/window instance at W << m stands.)
- F2 The wedge: conjecture = quadratic curve never enters the wipe set;
  both endpoints mapped, the DISTANCE never measured (J1c needs SAT).
- F3 Transformer-bridge connector: what plays periodicity in a real network's
  address system — left open, not renamed.

**G. The jungle queue (traversal order proposed)**
- G1 [cheapest, decisive] Power-of-2 denominator boundary: 3:8, 5:8, 7:8,
  3:16 → promotes or kills D6.
- G2 CLOSED 2026-10-10: dead-offset classification at a/b has a closed form
  (Δ(r) degree ≤ 1; finite square tests; O(b) sieve-free). The map is
  EXTENDED by it: 9 newly-confirmed dead pairs (3:2, 5:2, 7:2, 8:3, 8:5,
  9:2, 9:5, 10:3, 11:2).
- G3 Ulam-diagonal overlay on variable.html: slider for seam offset
  k=c·m+b, draws the spiral, reports prime count; Euler arc = calibration
  shot. Turns "find bright curves" into an instrument.
- G4 Farey walk: 1:1 → 2:1 stepping the Farey sequence, dead lines permuting
  and dissolving — D5/D2 as a movie.
- G5 Sturmian test at φ/√2: is the irrational "chaos" aperiodically ordered
  (spacing word low-complexity) or sieve-random? Decides if the irrational
  sea is structureless or differently-structured.
- G6 Prime-rich quadratics at other integer r: at r=a, k=cm+b gives
  N = (a/2)m² + … — hunt Euler-class forms as bright spirals at r=3, 4.
- G7 Halves-claim distribution probe: per-half W_L/W_R fields, m=21..100k —
  turn the empirical hold into a distribution with margins.
- G8 (joint w/ Claude) J1c wipe-Hamming distance; confined half-cover scan;
  sub-Poisson tested properly; calm-slope derivation pre-registered.
- G9 C4 anti-correlation mechanism hunt.

---

## 2026-10-09 night — G1 closed, and the seam gives up its engine

### The fine-resolution lock (L3 upgraded from law to mechanism)

The m%4 "diluted escape" at non-1:1 ratios was an ALIASING ARTIFACT. Re-scanning
at resolution m mod 4b: EVERY rational shows the same pure lock as 1:1 — every
m-residue class is either exactly 2.00x or exactly 0.00x, nothing between
(residuals at 1:14/1:16 were under-resolution, cap was 48 < 4b).

Mechanism [F]: deadness of an odd-k tick is decided purely by B[m] mod 2, which
is periodic in m with period dividing ~4b (B[m] is a quasi-polynomial). Classes
with B[m] even: odd ticks all-odd -> exactly 2x density. Classes with B[m] odd:
odd ticks all even -> totally dead. The 1:1 wheel's lock period (4) is the only
one coarse enough for the eye; larger denominators hide the identical law in
fine structure. This is WHY 1:1 looks special (Claude's lock observation) —
it isn't special, it's just legible.

### The seam map (all coprime a/b, a,b <= 18)

Every integer ratio dead (seam = a*T(m), known). Row a=1: ALL dead.
b=4 column closed: dead iff a = +/-1 mod 8 (verified through a=21).
General closed form [G] — the map is the classification for now; it is a
fixed-divisor problem over quasi-polynomials (classically hard in general).

### The three-layer deadness engine (the night's real prize)

Layer 1 — content/gcd: within a constant-L block the seam values are an AP with
difference L; if gcd(first, L) > 1 the whole block is composite. Universal,
exact, sieve-free. Verified: zero violations at 5:8, 2:3 across all blocks.

Layer 2 — quasi-polynomial factorization: on each residue class m = R*t + r
(R = 2b * (power of 2)), the seam N(t) is an EXACT quadratic in t. If the
discriminant is a perfect square, N factors over the rationals and the class is
identically composite. Exhibit, 3:8, m = 16t+2: N = 48t^2 + 16t + 1 =
(4t+1)(12t+1). 3:8 has ALL 16 classes factorable -> seam fully dead, mechanism
closed (no sieve input at any point). 5:8: 8 factorable + 8 non-factorable;
every seam prime lives in a non-factorable class (classes 8, 10 are
non-factorable but unlucky in range — possible-in-principle is not obligated).

Layer 3 — only after layers 1-2 pass does the sieve actually get consulted.

7:4 anomaly resolved: 2 non-factorable classes but zero primes — they carry a
content obstruction (parity-class deadness), i.e. layer 1, not a violation.

### Unification

This is ONE engine behind: L2's dead lines (same square-discriminant classes at
other fracs/offsets), the seam map, and the Ulam connection. Euler's
n^2-n+41 = NON-factorable quadratic (disc = -163) living on a live class at 2:1.
The dead/live boundary everywhere is: square discriminant (factors) vs not
(can be prime). And 5:8's non-factorable seam classes run ~0.26 prime density —
prime-rich quadratic real estate exists at OTHER ratios, not just 2:1. G6
(hunt Euler-class quadratics) now has a mechanism: enumerate non-factorable
classes, rank by yield.

### Status changes
- L3: [E] mechanism-known (was empirical law)
- D21 power-of-2 pattern: SUPERSEDED — the lock is universal at 4b resolution;
  powers of 2 only fold it back to mod-4 legibility
- G1: CLOSED (with engine)
- G2: mostly closed by the same engine; the "formula" is now an enumeration
  recipe [F], closed-form classification still [G]

---

## 2026-10-09 late night — THE CENSUS, G5 CLOSED, ROLL ENGINE VERIFIED

### The Living Prime Map (Claude's roll engine) — connector proved here, feedback applied

- [F] Verified the connector myself rather than trusting the 30M-tick sample:
  landing-seed −T(m−1) mod p is exact (0 mismatches, rings to 2×10⁸, layers to
  282M); the add-and-wrap recurrence reproduces the stagger field exactly
  (0 mismatches, 4 rings × 3 starts × 199 layers); full stamped output equals
  primality on 40,660 consecutive ticks.
- [F] The engine is one telescoping identity: o(m₀+Δ) ≡ seed − [T(m₀+Δ−1) −
  T(m₀−1)] (mod p) in closed form. Roll is Jump at consecutive-layer
  resolution; for sparse visits, roll IS jump with a telescoped seed.
- [F] The wall's true name: holding every prime up to √N is the information
  price of an EXACT certificate — any deterministic exact sieve must pay it.
  The doors past it are different mechanisms, not optimizations: probabilistic
  certificates (Miller–Rabin: no ring list, tiny lie probability) and
  structure (decoding the stagger field — standing wall #32).
- [F] Layer-skipping can't pay: pointer maintenance is Θ(rings) per layer
  regardless of window, and locating a ring's next window-hit is a quadratic
  congruence costing more than the layers saved. The honest speedup is
  hardware: every ring's state machine is independent and 32-bit — one ring
  per GPU lane, two uint32s each. Stated as a direction, not built.
- Cleaned the page of Claude frame-runtime junk (the artifact export carried
  claudeusercontent.com infrastructure), applied the above as copy, shipped
  as living-prime-map.html with sibling links.

### The census (probes/census.py + class_no.py) — 9,216 integer-ratio offset forms + 176 seam classes, LIMIT 5M

- [E] The discriminant engine is exact. 0 / 9,216 square-D offset forms contain
  a prime. The 41 / 176 square-D seam classes that showed 1–2 primes are
  unit-factor leaks at t=0..1 only (e.g. the pronic class N=(t+1)(t+2) is
  "prime" at t=0 where a factor equals 1): densities ≤ 0.001 vs live classes
  ≥ 0.15, streaks 1–2 then stop. Dead ⟺ square-D, past the unit boundary.
- [E] Euler is champion but NOT unique. Runner-up: a=6, c=0, b=23 →
  N = 3m²−3m+23, D = −267, streak 19 vs Euler's 20, density 0.430. h(−267) = 2
  (counted exactly). It dies at m=23: N = 1541 = 23·67 — the form's own
  constant is one of the factors.
- [E] Euler's fundamental class recurs: a=8, c=2, b=41 → 4m²−2m+41,
  D = −652 = 4·(−163), density 0.502 against Euler's 0.501. h(−652) = 3
  exactly — so equal density across different class numbers is itself an
  observation worth a look someday.
- [E] Heegner reachability is ratio-gated. All twelve class-number-1 |D|
  occur somewhere in range, but the champions −43, −67, −163 occur at fixed
  offsets ONLY at a=2: the reachability congruence (c−c₀)² + 163 = 4c₀·b has
  no integer solutions for c₀ = 2, 3, 4. So 2:1 is the COMPLETE Heegner host;
  a=4, a=6 host none of the big three (a=6 hosts −3 via 3m²−3m+1 and the
  h=2 −267 champion); a=8 hosts −163 only as the conductor-2 order (−652).
- [E] Seam real estate is second-class. Best live seam class: 2:5, class
  m0=2, N = 5t²+5t+2, D = −15 (h=2), streak 7, density 0.355. Heegner seam
  hits: only −16 (4:5) and −28 (2:7). Where the wheel's algebra is strongest
  (the seam), survival is marginal; prime-rich lines want integer-ratio
  offsets, where B[m] is exactly quadratic with leading coefficient a/2.
- [G] follow-ups: a = 9..16 extension; offset lines at non-integer rationals
  (still quadratic on residue classes — unenumerated); LIMIT beyond 5M.

### G5 Sturmian (probes/g5_sturmian.py) — CLOSED

- [E] Substrate is exactly Sturmian: lap word w[m]=L[m+1]−L[m] at r = √2, φ,
  π, e all have factor complexity p(n) = n+1 through n = 12. Rational
  controls bounded as the theory demands (5/3 → p saturates at 3; 7/4 at 4).
- [E] The wheel is the sieve at irrational ratios too: on deep laps at √2,
  zero gold ticks violate k ≢ −B[m] (mod p) for p = 2, 3, 5, 7.
- [E] The residue "structure" of the coloring is the forced exclusion
  exactly: raw χ²(q=3) ≈ 124–133 vs the forced-exclusion prediction 0.03–0.15.
- [E, current resolution] Beyond the sieve: χ² over the allowed classes mod 11
  = 2.7–7.6 (df 9 — ordinary); lag-1 autocorrelation within the mod-6-allowed
  classes = −0.050, −0.019, −0.065 (se 0.028; inconsistent in sign, ≤ 2.3σ).
  No detected order beyond the sieve.
- So L2's "structureless" is now precise: at irrational ratios the substrate
  is aperiodically ordered (Sturmian), the coloring is sieve exclusions plus
  nothing detectable, and the certificate algebra is absent. Ordered floor,
  sieve furniture, no deed to the land.

---

## 2026-10-09 deep night — GPU FRONTIER (pygame + cupy on the RTX 4070)

The roll engine, one ring per GPU lane. [F] Same stagger-field mechanism as
the Living Prime Map; the GPU port adds closed-form jump seeding (mod-2p
halving trick, one uint64 multiply — no bignums) and a stamp kernel whose
first-stamp index uses a double-reciprocal estimate + integer correction
(a 64-bit div per ring per layer would dominate the whole kernel).

Verified chain: startup self-check (seed at 1,234,567, 8 layers x 1024 ticks
vs CPU span sieve, 0 mismatches) + exact audit of a dump-band at layer
6e9 (N ~ 1.8e19): 6,002/6,002 listed primes exact (deterministic MR),
1,952/1,952 non-listed composites — zero errors both directions.

The wall's true name, measured: BANDWIDTH. Every ring costs 20 B/layer of
traffic; ~3.7 GiB/layer at 6e9 caps at ~32 layers/s (~256 GB/s bus). Wide
window (1M ticks) holds certified throughput at ~33M numbers/s at 6e9 and
~100M/s at 282M. uint32 regs cap the dial at m < 2^32*sqrt(2); uint64 would
double per-ring traffic for a higher ceiling.

Ships: gpu-frontier/gpu_frontier.py (+ run.sh, README.md). Modes: windowed
pygame app (jump dial, save gold bands with sha256), --benchmark, --dump-band
(the certified-prime frontier service cut), --frames smoke test.

---

## 2026-10-10 overnight — AUTONOMOUS CHAIN (pre-registered, all phases committed)

CORRECTION to the 2026-10-09 deep-night section above: "the wall's true name
is BANDWIDTH; every ring costs 20 B/layer" is REFUTED as the stamp-kernel
bottleneck (lab/PHASE0p5_kernel_bw.md). The kernel reads only 8 B/ring; its
cost is critical-path serialization — one thread per ring, p=2's thread
walking W/2 sequential iterations bounds the whole kernel; cost ∝ ΣW/p
scattered writes, nearly independent of ring count; atomicAdd (witness layer)
is ~50% additive on top. The 20 B/ring figure describes the ADVANCE kernel's
presence traffic, not the stamp bottleneck. uint32-window variant measured
SLOWER than uint8. Fix queued: window-parallel small-p kernel (Phase 0.6).

Method note: the chain ran on pre-registered predictions with binding stop
conditions (AUTONOMY_2026-10-10.md); a personal lab log with a
context-retention rule (lab/MEMENTO.md) recorded surprises/connectors per
phase. Two standing method lessons, both from falsified priors: (1) huge
σ-deviations are more often specification errors than discoveries — the
pre-registered HL one-witness formula missed by +3,869σ and the error was in
the formula (it counted classical semiprimes; the wheel's one-witness class
N = pᵃ·q, p ≤ bound < q, is ~92× more numerous); (2) when a "hard problem"
smells like Diophantine genus, first check whether the variable is free or
periodic — periodicity trivializes curves.

### Verified tonight

- **Witness-count layer** (gpu-frontier, commit e479f32): stamp_kernel
  atomicAdd per stamp → every certified tick carries ω_small(N); zero
  measurable roll cost; `s`/`--dump-band` write witness-band sidecars.
  Startup self-check extended; the first audit caught a duplicated prime 2 in
  every prime-table cache (boolean engine was blind to it; counts exposed it
  instantly) — caches trimmed, builder fixed, load path sanitizes.
  [F] One-witness tick ⟹ N = pᵃ·q (p ≤ bound < q) or prime power; the exact
  Lehmer enumeration of that class reproduces a dumped band's count EXACTLY
  (165,861 = 165,861, 0.000σ) — deterministic certification of the witness
  semantics. [E] Gap statistics, twin density, prime density all MATCH theory
  (−0.25σ, −1.16σ; max gap 274 vs record 540 below 10¹²).

- **Census axis CLOSED [E]** — three probes, all pre-registered: (P1) band
  statistics MATCH Hardy–Littlewood/Cramér; (P2) ω-map spatial structure NULL
  vs honest nulls (the naive iid null is decisively rejected — small-prime
  determinism lives in the base, not the null); (P3) retained ring-phase
  structure NULL across 16 layers vs alignment-matched nulls (a lag-0
  excursion was root-caused as sieve-lattice self-alignment: fixed layer
  spacing shares small factors; periodically-spaced samples need
  alignment-matched nulls). Consequence: "a massive wheel reveals new
  statistics" is dead by measurement. The massive-build case now rests
  entirely on the dial geometry / instrument value.

- **C1 reduction [F-argument]** (lab/PHASE4b_reduction.md): B1 says the wheel
  IS the √N sieve, so C1 ⟺ primes in intervals of length ~0.7√N — ~3×
  SHORTER than Legendre's conjecture at comparable height; unconditionally
  out of reach (best: Baker–Harman–Pintz x^0.525). Wheel-native proof
  impossible in principle; "zero structural support" promoted from
  observation to theorem. **G7 [E, strengthened 10×]**: 999,980 laps
  (m = 21..1,000,000, N to ~5×10¹¹), ZERO violations; margins med 15/16,
  max 300/299, lap-corr 0.011; worst-margin slope 2.19 ± 0.08 vs ln N
  (constant 0.41, under the Cramér bound); closest call ever m=33 at
  0.188·H; beyond 10⁴ laps the nearest prime stays ≥ 0.99·H from the
  midpoint — claim safety GROWS with scale. Files: lab/PHASE4a_*, probes/
  g7_halves_1m.py (resumable, MR cross-validated 0/200k), g7 CSV.

- **D8 CLOSED FORM [F→E]** (lab/PHASE5_d8_pin.md, PHASE5_d8.py): the seam
  discriminant Δ(r) has polynomial degree ≤ 1 (the r²-terms of B² − 4AC
  cancel identically for every coprime a/b) with period b; proved pairing law
  P = 0 iff b odd, P = b/2 iff b even (0 violations, b ≤ 12, a ≤ 15).
  Dead classes = {r mod b : Δ(r) square} ∪ {content-killed}, O(b) exact
  arithmetic, sieve-free; all landmarks pass; the formula PREDICTS and
  confirms 9 unmapped dead pairs (3:2, 5:2, 7:2, 8:3, 8:5, 9:2, 9:5, 10:3,
  11:2). No Pell, no elliptic curve — the square tests are finite because r
  is a residue label, not a free variable.

- **GPU kernel characterization [E]**: benchmark halves under live-window
  co-tenancy (83→41 layers/s); the live window is insensitive to the CPU
  miner (77→76 layers/s) — the earlier xmrig attribution for GPU rates is
  withdrawn (xmrig's measured victim was the memory-latency startup path).

### Status changes

- C1: [S] → [S, Legendre-hard by reduction; empirically bulletproof to 1M
  laps]. Paper path = wedge-distance instrument (F2), not the claim.
- D8: [G] → [F→E] with named residuals.
- G2: CLOSED (map extended by 9 cells).
- Census/ω-spatial/retained-structure axes: CLOSED [E] (measured).
- New engine capability: witness-count layer [F], certified exact.

---

## 2026-10-10 day — PHASE6: the quadratic rhyme probe (wheel deadness engine vs
## fractal spectral universality) [E, corridor closed; new internal law]

Context: a Mar-2026 doc (three independent Claude instances) found the Menger
sponge Laplacian carries x²−(d+2)x+2 with multiplicity d, irrational spectrum
(D=(d+2)²−8 non-square). Both lab sides had square-discriminant classifiers;
question: corridor or wallpaper? Files: lab/PHASE6_quadratic_rhyme.{py,md},
lab/PHASE6_run.log.

### Fractal side, extended (all exact charpoly factorization over ℚ)
- Menger d=4 (NEW): factor x²−6x+2, roots 3±√7, multiplicity exactly 4 —
  the universality conjecture now has d = 2, 3, 4 at L1. Carpet L2 (NEW):
  factor persists at multiplicity 2 (doc had sponge only). Vicsek d=3 (NEW):
  all-integer spectrum (K₁,₈ star; keep-center → rational).
- [F] D(d)=(d+2)²−8 is a square only at d=1 (factor-pair argument; checked
  d ≤ 2000): irrationality of spectral roots PROVED universal for
  remove-center d ≥ 2 (doc had it as measured evidence).
- SURPRISE RULE vs the doc itself: "spectrum symmetric about S/2" is FALSE
  as a multiset statement at Menger L1 (mult(2)=5 vs mult(3)=1, exact).
  Carpet L1 exactly symmetric; sponge L1 partial. Doc correction logged.
  Two smaller: P²·S = cell-count encoding works only at d=3; universality
  is contact-convention-dependent (Vicsek point-contact → junction graph).

### Corridor verdict: wallpaper, closed by sign [F→E]
- All 271 wheel seam quadratics sampled have non-negative coefficients
  (C=0 in 16 classes, never negative) — no strictly positive root possible.
  The fractal factor has both roots strictly positive. The polynomial
  families are provably disjoint; needle scan: zero wheel discriminants of
  shape (d+2)²−8.
- Shared classifier = perfect-square discriminant ⟺ ℚ-factorability = the
  quadratic formula, genus 0, ancient. Analogy, not identity — labeled.

### The result that survives: the dead/live boundary is SAWTOOTH-CARRIED [E]
Strip the sawtooth from Δ(r), keep the ratio-side ramp: 135/271 correct —
49.8%, a coin flip. The sawtooth flips the other half; 47/57 ratios change
their dead-class set entirely. The all-dead a=1 row is invisible to ratio
geometry. The ratio sets the scale; the wheels write the law. The sawtooth
IS the rounding corrections c(j) — the same Dedekind-sum-like object PHASE5
pinned as D8's true obstruction. One object, two roles.

### Literature sweep (shallow — 4 searches, not MathSciNet)
No collision with the specific construction (round(a·m/b) accumulation →
per-class seam quadratics → dead-class tables). Neighbors to cite: Ehrhart
quasi-polynomials (the sawtooth's natural home), squarefree-values-of-
polynomials, primes-in-quadratics (Euler lineage). Verdict: combination
looks novel; the deep sweep stays on the rack before christening.

### Status changes
- New wheel-internal law: dead/live boundary is sawtooth-carried [E].
- Fractal universality doc: corrected in writing (symmetry, encoding,
  contact convention); conjecture strengthened (d=2,3,4; proof for
  irrationality at remove-center d ≥ 2).
- Corridor: CLOSED (wallpaper at identity level; shared classifier generic).

## 2026-10-10 (late) — deep literature sweep + the column engine lands

- **Column engine archived** (`column-engine/`): certified primes straight down
  one column with rings streamed and never held. Independently re-run here on a
  20k-layer segment at layer 6e9: 423 primes, zero MR mismatches, lane-test dead
  rate exactly 50.0%. README's run-log claims reproduced.
- **Deep literature sweep** (`lab/LITERATURE_SWEEP_2026-10-10.md`, four agents,
  ~40 query rounds). Headline verdicts:
  - Lane test and C(k) are exactly the Hardy–Littlewood Conjecture F singular
    series for m²−m+2k (HL 1923; Bateman–Horn 1962; verbatim in
    Zomlefer–Garcia–Fukshansky 2020). Now cited, never claimed.
  - Dead-class criterion (square discriminant ⟺ reducible) is textbook; our
    [F] derivations stand, no novelty ever claimed.
  - Rabinowitsch/Heegner is a real formal home for column discriminants
    D = 1−8k; among integer start-columns only k=1 is class-number one (D=−7).
  - No indexed precedent found for: the wheel enumeration + visibility,
    two-prime channels theorem, dead-class taxonomy as a ratio-family
    classification, or the column engine as an assembly. Caveat: web-scale
    sweep, not MathSciNet; one pass still owed before external submission.
  - Naming: "prime tread wheel" clean; "wheel sieve" alone is Pritchard's.
- Whitepaper §14 (relation to existing work) + references 11–20 added.

## 2026-10-10 (evening) — PHASE7: pre-registered replication, 8/9 predictions hit

Claude's handoff (`column-engine/HANDOFF_TO_KIMI.md`) froze nine predictions
for a layer-statistics run to 1.8M layers (numbers to 1.62e12) before Kimi
ran it on the 32-thread box. Protocol: certified the engine first (100k
re-run byte-identical to Claude's summary, π(T(1e5)) ✓), then ran the frozen
experiment detached (~1h54m wall, 60.8 CPU-hours — Claude's 5400-thread-sec
estimate was ~40× low; recorded in the scorecard, not held against the law).

Scorecard (`lab/PHASE7_prereg_scorecard.md`): **8/9 HIT.**

- Clash factor 100k–1M: 0.89064 vs 0.8906±0.0005 ✓; 1M–1.8M: 0.89060 ✓.
  Converges to e^γ/2 = 0.89054 from above; phantom-clash haircut [E] at 16×
  the certified range.
- Worst count/(m/ln T): 0.959, 0.985 (floors 0.93/0.95) ✓✓. Longest
  prime-free run/m: 0.00305, 0.00048 (ceilings 0.005/0.0006) ✓✓.
- Last-layer-with-≤c list identical (…10:121) ✓.
- **MISS (informative):** fewest primes 1M–1.8M predicted 35300±700,
  measured 36,720. Miss is *upward* — the sparsest layer is denser than an
  iid-style tail allows. Layer counts are more uniform than the guessed
  fluctuation model: the worst/exp floor is still climbing toward 1
  (0.959→0.985), so the minimum converges from above. The ±700 band hid an
  unstated fluctuation model → now [G]: one derivation owed.
- Total primes 59,837,421,097 = li(1.62e12) within truncation ✓.

Data: `column-engine/layers_1p8M.csv.gz` (per-layer counts, 1.8M rows),
`column-engine/layerstats_1p8M_run.log`. New instrument files archived:
layerstats.c, HANDOFF_TO_KIMI.md, column_runs.log, layerstats_100k.txt.

## 2026-10-10 (night) — the horn view ships (Claude + Obi build, Kimi reviewed)

- **[F→E] The flat page is a stretched skin; the horn is the honest metric object.**
  Give every tick a unit square tile and put layer m one unit further out: ring m
  is m tiles long at slant m, but a flat circle needs 2πm, so the skin rolls up
  into a cone with sin(half-angle) = wedge/2π. For square tiles (wedge = 1) that is
  asin(1/2π) = 9.158° — the horn. At wedge = 2π the cone opens to exactly the flat
  page; past 2π the skin ruffles. Unrolling is an isometry family (every ring keeps
  its length at every stage). Verified by `test_shape.js` (node): ring lengths exact
  to 1e-4, seam closes to 1e-9, closed-form normals match numeric to machine eps.
- **[F] Tie-in to the deadness engine:** the lap ratio dial is the wedge. Whole-number
  ratios give wedge = r ∈ ℕ, and 2π ∉ ℕ — so no actual wheel skin ever lands on the
  flat page. The page the whole lab works on is the measure-zero stretched case;
  real wheels are horns (r=1), shallow cones (r=6), or ruffles (r≥7).
- Ships as a sibling page (`horn.html` + `horn-view.js`, WebGL1, no dependencies),
  linked from the wheel masthead and the globe siblings line. Option B in
  HORN_INTEGRATION.md (a fifth view inside the wheel app) is specced but not built.

## 2026-10-10 (night, late) — the grand page

- grand.html ships: one rail, every view. Wheel / horn / globe / variable /
  living map / white paper / essay / night-shift / problem wheels load in
  frames beneath a single tab rail; a frame, once loaded, is never destroyed,
  so every instrument keeps its state across switches. Keys 1-9, hash routes
  (#horn etc.) are shareable. [F] It's pure shell — the instruments are
  untouched, so every certification on them (test_shape.js, verify.py,
  layerstats) still covers exactly what ships.
- Why a shell and not a merge: the wheel app is a 240KB self-contained
  instrument with its own render loop; merging render loops into one page is
  surgery on a certified tool, for zero measurement gain. The object was
  always one object — this makes the *presentation* one page without touching
  the instruments. Deeper fusion (horn inside the wheel app) stays on the
  list per HORN_INTEGRATION.md.

## 2026-10-11 (early) — site navigation unified on the grand page

Every deployed surface now routes to grand.html (one page, every view) instead of
leaving the instruments as separate islands:

- Registry entry: new lead card "The Whole Wheel" (grand.html) + a Horn card;
  front-matter live-pages line updated.
- Instrument pages gained an "all views on one page" link: variable.html masthead,
  living-prime-map.html siblings line, problem-wheels.html intro, horn.html title
  block (its first outbound link ever), essay.html lede, night-shift.html footer.
- Whitepaper meta line (render.py) links the grand page.
- New card images: post-media/grand-page.png (headless screenshot of the rail),
  post-media/horn-views.png.
- Repo hygiene note: root essay.html is a byte-identical duplicate of
  field-notes.html under the wrong name (not deployed — render.py uses the
  posting-kit/docs copies); root night-shift.html/field-notes.html are inert
  duplicates kept in sync with the kit copies.

## 2026-10-11 (morning) — GLM review round: 10 fixes + one new theorem filed

GLM audited the whitepaper; every load-bearing claim re-verified here before
touching anything (separate sieve counts, not GLM's arithmetic, are the
certificates). Applied to WHITEPAPER.md and PAPER.md:

1. **[F→fixed] BHP sentence was backwards.** BHP windows (N^0.525) are wider
   than the layer width √(2N), so BHP settles no layer, even non-effectively;
   the open residue is infinite, the *verified* residue finite. Fixed in both
   papers (the night log had it right all along — only the two papers erred).
2. **[F→fixed] Clash direction.** Counts sit ~11% BELOW the independent-rings
   guess, converging down to e^γ/2. Classical identification now stated:
   survivor density 1/ln N ≈ 1/(2 ln m) over Mertens e^(−γ)/ln m = e^γ/2
   (Mertens' third theorem; identity [E], phantom-clash reading [S]).
3. **[F→filed] B7 — the mirror lift (new, explains two closures).**
   T(m−1)+T(m) = m²; tick involution k ↔ m−k is an exact eligibility-
   preserving bijection, lifting the seat palindrome to values v ↔ m²−v.
   Odd m: no mirror prime pairs exist (one summand even ≥ 4) — proven, not
   probed. Even m: a mirror pair IS a Goldbach representation of m² in the
   layer window — rare, which is §6.3's mirror-compensation null in one line,
   while the bijection's exactness is why pattern-side palindrome survives
   where value-side compensation is dead. Verified: zero odd-m pairs m<3000;
   11,085 even-m pairs, all summing to m².
4. **[F→upgraded] Seats.** "φ(m) seats" needed the B5 caveat (on m ≡ 2 mod 4
   laps every seat value is even — T(m−1) odd + coprime k odd). Proven, label
   upgraded [E]→[F]. NOTE: probes/verify.py had the parity escape encoded all
   along (seat = g==1 & m%4!=2 | g==2 & b odd) — the prose was the laggard.
5. **[F→upgraded] Parabolic confinement** to proven (o_p = −T(m−1) is a
   quadratic image: (p+1)/2 phases for odd p); "zero violations p<200" now a
   certificate, not the evidence.
6. **[F→reconciled] Record-layer anatomy** against field-notes (the primary):
   109 outside strikers = arcs from primes above the seat threshold (NOT
   "small primes 2…331", π(331)=67≠109); 57 holes have no STRIKER arc, covered
   by inside primes in (766, m] — no B1 tension (witness set p ≤ m). The old
   "100% of cover from outside primes" line was contradicted by the 57 holes
   and is gone. Redundancy 1.68×, 270/497 single-cover seats restored.
7. **[F→fixed] Heegner count.** "Twelve" matches no canonical count: 9
   fundamental Heegner + 4 non-fundamental = 13; census reaches twelve of
   thirteen — now stated as reach, not canon. [G] which one the range excludes
   (needs a census list re-dump).
8. **[F→fixed] Streak onset.** 3m²−3m+23's line exists only from m=4 (lap
   length must reach 23); streak 19 runs from line onset, not m=1. Same fact,
   one clause.
9. **[F→fixed] Truncated sentence** — "layer\n5000." at a markdown line start
   was eaten as a list marker on the LIVE page (number invisible). Reflowed.
   Lesson: md line-wrap can swallow a number at the start of a continuation
   line; check rendered HTML, not the source.
10. **[E] PAPER.md §9 BHP** fixed in the same stroke; its seats sentence got
    the parity-escape parenthetical.

verify.py re-run: all checks ok. Wheel repo commit + push, site re-rendered
and deployed, grand.html#paper re-screenshotted clean.

## 2026-10-11 noon — Obi/GPT-6 handoff: the 5:4 exact half-turn, verified and filed

Source: handoff pack from Obi + GPT-6 (Luna-side), received via Sylvan, with
their verifier `prime_tread_5_4_verify.py`. Task per house rules: independently
derive, compare against existing ratio/deadness work, log everything. Nothing
below was taken from the handoff on faith — every load-bearing claim re-derived
or re-measured here first.

### Provenance verdict

The four-family 5:4 half-turn classification is NOT in the existing notes
(grepped INSIGHTS + WHITEPAPER + probes for 5:4 half-turn structure: absent).
It is a NEW INSTANCE of the existing three-layer deadness engine (2026-10-09
night), not a new mechanism: the square-discriminant criterion partitions this
ray dead/live exactly as it partitioned the seam and frac-rays. The two-branch
simplification, the mod-16 eligibility filter, and the BH constant are the new
sharpenings contributed here on top of the handoff.

One reconciliation note [O]: ratio_sweep's "lines" are k = round(f·L[m])+b —
at f=1/2 on odd-L layers this lands on a ROUNDED tick, not the exact midpoint.
The sweep's 230k-family scan therefore saw the half-turn ray only blurred; the
exact-half-turn object (L even required) was never isolated before. Two
different observables share the name "half-turn line"; the classification
below is for the exact one, per the handoff's own edge-condition warning.

### Independent derivation [F] — matches handoff on every clause

Derived from variable.html's rounding word (L = max(1, round(5m/4)),
half-up, no handoff formulas consulted):
- L(4q+s) = 5q + c_s for c = (1,3,4,5); B(4q+s) quadratic: (10,3,0),
  (10,8,1), (10,13,4), (10,18,8) — matches the sweep-era quasi-polynomial law.
- Exact half-turns exist iff m mod 8 ∈ {0,3,5,6} (existence = L even; the
  8-period is 2b — one parity layer above the b=4 rounding period).
- H(m): 40t²+t = t(40t+1) | 40t²+31t+6 = (5t+2)(8t+3) | 40t²+51t+16 |
  40t²+61t+23 on m = 8t+0,3,5,6 — all four identical to the handoff.
- Discriminants: 1, 1, 41, 41. Global branches: (5m²+m)/8 [D=1, factors]
  and (5m²+m−2)/8 [D=41, irreducible over Q].
- Exact square identities on the ray [F]: 160H+1 = (10m+1)² on the D=1
  branch; 160H+41 = (10m+1)² on the D=41 branch. Verified to m=3000. This is
  the D8-shape statement ("discriminant is a quasi-polynomial; dead = finite
  union of exact square tests") instantiated on a non-seam ray.

### Eligibility filter = engine layers 1+2, not new structure [F]

"Prime half-turn occupant ⟹ m = 8 or m ≡ 6,13 (mod 16)" decomposes:
- classes 0,3 dead by Layer 2 (Δ square → factors; t(40t+1) needs t≥2,
  (5t+2)(8t+3) always) — with the single leak m=8, H=41 (factorization
  degenerate at t=1);
- classes 5,6 halved by the mod-2 fine lock at resolution 4b=16 (B[m] parity
  kills odd-k ticks in B-odd classes): m≡13 mod 16 has k = L/2 always even
  (live); m≡6 mod 16 live only for u even (k = 5u+4 even); m≡5,14 dead by
  parity. Verified zero violations through m = 20,000 [E, 662 primes, this
  machine] — the handoff verified to 5,000; extended 4× here with zero
  violations and zero class-0 leaks.

### The new observation [E→O]: the live classes are BH-calibrated "lucky" quadratics

Both D=41 families (in u, after parity filtering: 160u²+262u+107 and
160u²+122u+23, D = 164 = 4·41) are admissible — no prime p < 200 divides all
values. Bateman–Horn partial products converge cleanly:
C ≈ 4.495 (stable from p<800 to p<30,000, both families BIT-IDENTICAL
partial products — same ρ(p) at every prime, verified numerically; root
counts mod p depend only on the shared discriminant here). Empirical singular
factor at m ≤ 20,000: 662 primes / Σ(1/log H) = 662/147.0 = 4.50. The
heuristic and the measurement agree to three digits.

Structural analogy [labeled, not identity]: Euler's n²+n+41 (D = −163) has
BH constant ≈ 3.3 and Rabinowitsch's theorem behind its luck. These families
have D = +41; Q(√41) has class number 1 and L(1,χ) ≈ 1.30 (Dirichlet class
number formula, computed here). Whether a Rabinowitsch-type exact theorem
governs positive-discriminant lucky families of this shape is [G] — the
analogy predicts the wheel found an Euler-grade polynomial by turning a dial,
which is itself the handoff's "what does the unit fix?" question answered
one level down: THE TREAD CHOOSES THE STAGE, ARITHMETIC WRITES THE DENSITY.
Which spoke hosts a prime family is embedding-dependent; the density law of
the family (via ρ(p), hence D) is intrinsic arithmetic.

### Coincidences and curiosities (logged per Obi's rule, no causal claims)

- H(8) = 41, and the other branch's discriminant is 41. Also the D=1
  branch's discriminant is 1 and the m=8 layer is the unique class-0 layer
  whose half-turn tick (k=5) is odd-k in a B-even class — triple alignment
  at one layer: lock-live, factorization-degenerate, value = 41. Curiosity.
- m=8 sits in the B-even mod-16 classes {0,1,3,4,8,9,11,12} (computed here);
  the live eligibility classes {6,13} are B-ODD — the half-turn escapes the
  lock precisely by sitting on even k in B-odd classes. The lock is the same
  fine-resolution lock from 2026-10-09 night, resolution 4b = 16, as predicted
  by "period dividing ~4b."
- Failed step logged (process): the first independent derivation run produced
  a spurious "global branch fit fails" — an off-by-one in the t-parameter for
  the m=8t class (its first half-turn is t=1, not t=0; the fitted "constant"
  was f(t₀), not c). The branch identity is exact; the bug was in the fitter,
  not the math. Notated because the handoff's §5.9 (prefer closed-form branch
  + residue restrictions over per-prime lines) is exactly the compression this
  bug illustrated.

### Queue items this round opens (no production changes made)

- [G] General a/b: closed form for the exact-half-turn residue period
  (observed: existence period 2b, eligibility settles at 4b for 5:4; is the
  4b the fine-lock period in general?). Handoff §5.2 asks; not derived yet.
- [G] Pre-registered extension: run the two live classes to m = 10⁶ and test
  the BH ratio 4.50 stays (asymptotic vs finite-window agreement). Cheap;
  would convert the 3-digit match into a measured constant of the wheel.
- [O] Sweep the denominator family at fixed small |D| live classes — is
  "dial finds Euler-grade polynomial" generic at b=4? (a/4, a mod 8 ≠ ±1,
  live seams per the b=4 map) — connects the half-turn ray to the seam map.

Verify artifacts: /tmp/derive_54.py (from-scratch derivation),
/tmp/verify_54_extended.py (counts, filter extension to 20k, square
identities, lock-class computation, admissibility, BH products).

## 2026-10-11 afternoon — PHASE 8: the 5:4 density law measured to m=10^6, and the half-turn engine at general a/b

Artifacts: `lab/PHASE8_5_4_prereg.md` (frozen predictions), `lab/PHASE8_5_4_run.py`
+ `PHASE8_5_4_results.json` (HIT scorecard), `lab/PHASE8b_halfturn_engine.py`
(general a/b engine + dial sweep). All exact arithmetic, all reproducible.

### The pre-registered extension: HIT at −0.17σ

Frozen prediction before the run: 22,532 total primes on the 5:4 exact half-turn
m ≤ 10^6 (Bateman–Horn singular series C = 4.499267368, exact rational product
p < 300,000, × logarithmic sums S13+S6 = 5007.644, +1 for the deterministic
m = 8 value). Measured: **22,506, ratio 0.99886, −0.17σ** (Poisson σ = 0.0067).
Family split predicted 11,265/11,266, measured 11,175/11,330 (−0.80%/+0.57%).
Eligibility filter: zero violations out of 500k candidates. Baseline self-check
662 vs 662.6. **All four scorecard entries HIT.**

One correction filed against the morning's note: the singular series computation
must include p = 2. Both live families are identically odd (ρ(2) = 0), the p = 2
factor is exactly 2, and the full constant is 4.4993 per family — the morning's
4.495 was the brute product and rounds the same way. The Euler polynomial's
"3.3" is likewise the odd-prime product; its full constant is 6.646 (brute),
empirical 6.569 at U = 1249. Calibration pipeline validated on both.

Status: [E] the wheel's measured half-turn density tracks Bateman–Horn to 3
digits out-of-sample at m = 10^6. Bateman–Horn itself remains [G].

### The general a/b engine (PHASE8b) — what the dial does, generically

Twenty coprime ratios probed (b = 2..8). Four structural findings:

1. **[F] Closed form, universal.** H(m) = (a m² + 2 S(m) + c(m)) / (2 b) with
   c(j) = b·L(j) − a·j, S(m) = Σ_{j<m} c(j) — exact on every even-L layer of
   every ratio tested. This is one line from the PHASE 5 seam identity
   (B[m] = a m(m−1)/(2b) + S(m)/b); nothing new assumed. The whole half-turn
   apparatus is the seam apparatus evaluated at L/2.
2. **[S→measured] Fine-lock period depends on b's parity.** b even: n's parity
   splits WITHIN every mod-2b class — the fine lock lives at 4b (the 5:4
   pattern). b odd: parity is constant on mod-2b classes; no second lock.
   Why b's parity gates a parity lock: [G] — mechanism not yet decompressed.
3. **[S→measured] Discriminant collisions are the rule.** Live classes never
   come alone: at 5/4 two classes share D = 164; at 5/3 FOUR classes share
   D = −80; at 7/6 two share D = 228. The PHASE 5 discriminant is a
   degree-≤1 quasi-polynomial in the class index whose r² terms cancel
   identically — collisions across nearby classes are the generic output of
   that engine, and eligibility clusters where the ramp lands. Exact collision
   (not just nearby values) still wants a one-line reason: [G].
4. **[S→measured] Fully dead half-turns exist.** 4/3 and 8/3: every even-L
   half-turn value is even — the spoke is composite on its face, before any
   discriminant argument. 3/2, 5/2: odd values, but all discriminants square.
   So the dial has three outcomes: dead-by-parity, dead-by-factorization, live.

### Dial sweep verdict: Euler-grade density is rare but not unique

Singular series of every live family across the 20 ratios: mostly C ∈ [1.1, 3.8].
Two ratios stand apart: **5/4 (C = 4.50, D = 164 = 4·41)** and **7/6
(C = 4.89, D = 228 = 4·57)**. The 7/6 families (m ≡ 7, 10 mod 24,
H = 336t² + 198t + 29 and 336t² + 282t + 59) were verified EMPIRICALLY on the
spot: 1,871/1,905 primes to m = 200k against C·S predictions 1,884/1,883 —
ratios 0.993 and 1.012. Second instance confirmed.

So: "turn a dial, find an Euler-grade polynomial family" happens at ~10% of
ratios — not generic, not a 5:4 coincidence. [G] the discriminant statistic
that predicts C: 164 and 228 are both 4×(fundamental D with small L(1,χ)/
class number 1?) — Q(√41) has h = 1, L(1,χ) = 1.30; whether Q(√57) echoes
this and whether small L(1,χ) ⇒ high C across the sweep is untested.

### Queue (unchanged + new)

- J1c near-wipe SAT encoding (standing).
- [new] b-parity fine-lock mechanism: why does b odd kill the second lock?
- [new] Δ-collision one-liner under the PHASE 5 ramp.
- [new] L(1,χ) vs C correlation across the 20 ratios (cheap, numeric).
- [new] if 7/6 deserves the full treatment: prereg to m = 10^6 exactly as
  PHASE 8, now that it is the second candidate.

## 2026-10-11 mid-afternoon — swarm reports + PHASE 9: mirror pairs are HL sieve furniture [E]

**Claude closed three PHASE 8b gaps** (HANDOFF_CLAUDE_2026-10-11b.md, re-run here):
1. **b-parity fine lock — now [F].** H mod 2 fixed by numerator mod 4b; num(m+2b)−num(m) ≡ 4C_b (mod 4b); b|C_b iff b odd. b even ⇒ parity flips every 2b layers ⇒ lock at 4b. Same 2-adic fact as T(m) mod 2 having period 4. Matches sweep on 15/15.
2. **Discriminant collisions — one line [F].** Class polys are reparametrizations m = Pu+r of global branch quadratics; substitution multiplies D by P²; #kernels ≤ #branches. 160u²+262u+107 = (5m²+m−2)/8 at m=16u+13, checked.
3. **Field type by b parity [E, 21/21].** b even ⇒ 2 splits in every kernel (≡1 mod 8); b odd ⇒ 2 ramifies; zero inert. Extends the 1:1 no-2-inert theorem to the dial. And the queued L(1,χ) question is answered the opposite way from my guess: h=1 both, but L is NOT small (1.299, 1.513). The Euler-grade C comes from the **×4: the b-even dial deletes ring 2 in a field where 2 splits** (L has ½ at p=2, live class has ρ(2)=0 ⇒ ratio 4), plus bad-prime root losses (ring 5 ×1.25 at 5:4; ring 3 ×1.5 + ring 7 ×7/6 at 7:6) and small-inert corrections ~1.1–1.2. "Computed dials" — the signature is 2-adic, not analytic-size.

**PHASE 9 — the mirror-pair HL pre-registration (GLM's frozen formula, run here).**
Recount reproduced 11,085 bit-for-bit (m=2 excluded; incl gives 11,086 — convention audit item cleared, ±1 only). Frozen formula as written gave ratio **0.0723 — loud out-of-band failure**, exactly what a prereg is for. Conventions audited clean; root cause was a **form error in the frozen formula**: it summed the full pair density 1/(ln p·ln q) over *p prime*, double-counting the p-prime factor (shortfall factor = weighted mean ln p = 13.84). Two untuned standard forms: sieve form 11,197.6 (ratio **0.9899**), integral form 11,170.8 (ratio **0.9923**). Verdict per frozen rule: **[E] sieve furniture** — B7's mirror pairs follow the same 2C₂∏(p−1)/(p−2) mesh law as the radial locks. B7 closes quantitatively; P12 stands; no value-side structure. Artifact: lab/PHASE9_mirror_hl_prereg.py + .md.

**Gemini's RoPE connector (F3 ↔ Will §7) — filed as [S] structural analogy, connector BROKEN as stated.** Decompression: wheel maps absolute n ↦ angle via n mod m with m growing per layer (nonstationary; moduli are consecutive integers — CRT-rich); vanilla RoPE gives attention scores depending only on i−j (stationary, Toeplitz) over a geometric frequency ladder. The wheel's stagger/Mertens machinery lives precisely in the nonstationarity and the consecutive-moduli arithmetic — vanilla RoPE has neither, so the F3 prediction (Mertens-shaped loss decay) does NOT follow [F-check fails at the stationarity arrow]. What survives: position→periodic-angle + multi-frequency moiré + long-context quasi-periodic decay (known empirically as rope-wavelength artifacts). Discriminator if ever probed [S]: retrieval/attention-vs-distance showing Mertens-modulated dips at CRT-unfriendly offsets vs smooth decay. Not queued ahead of J1c — smallest sufficient claim.

Surprise-rule note: the 0.072 → 0.99 arc is the second time today a loud prereg failure converted into a stronger result than a first-pass hit would have been (first: the p=2 legendre miss in PHASE 8). Freeze, fail loudly, audit, correct, re-measure.

## 2026-10-11 late afternoon — J1c wedge distance: the convention IS the result

GLM's frozen one-hot MinSAT spec (CP-SAT → MILP via scipy milp/HiGHS, no new
deps), both variants of the convention flag executed, conventions frozen
before running. Three findings:

1. **[F] All-ticks wipe is a finite-window phenomenon: wipeable layers are
   exactly {2..13}, window closing at value 101** (first 97-rough integer;
   every layer ≥ 14 contains a 97-rough tick, Dickman ρ ≈ 2% per tick at
   these heights). Feasibility is pure arithmetic — a smallest-prime-factor
   sieve decides it in <1 s; the MILP only prices distances. The 13→14
   transition is the ring bound, not a phase-lock fact.
2. **[Measured] Seats-only: d(m) ∈ {0,1} for ALL 41 ≤ m ≤ 391. The
   near-wipe spectrum {d=2} is EMPTY.** 218 layers at d=0, 133 at d=1.
   Mechanism: trailing seat T(m)=m(m−1)/2 inherits factors of m,m−1 (almost
   always covered realized); at most the leading seat can demand displacement;
   one ring covers one seat ⇒ d ≤ 1. The durable object is the distribution
   of the 133 d=1 layers (leading seat 97-rough + singly coverable).
3. **[S/G] If the spectrum is wanted nonempty, either the ring bound must
   scale with m (spec re-freeze) or "wipe" must mean the rendered screen's
   sparse seats — a different object, not this one.**

Surprise log: the smoke test returned d(391)=None (infeasible) on the
PRIMARY convention before the sweep started — GLM's "CONVENTION FLAG: all
ticks, or seats only?" turned out to be the whole ballgame, exactly the
+3,869σ lesson one more time: when sigma is huge (here: object exists vs
doesn't), audit the convention before believing the physics. Negative result
filed with the same weight as PHASE 8/9's hits — the empty spectrum plus the
{2..13} window is a clean, checkable claim nobody had stated.

Artifacts: probes/j1c_wedge_milp.py, lab/J1C_spectrum.json,
lab/J1C_wedge_result.md.

## 2026-10-11 evening — PHASE 10 (C4 closed [E]) + J1c v2 correction (Grok's home-phase catch confirmed)

**PHASE 10 — C4 audit (lab/PHASE10_c4_audit.{py,md,json}).** GPT-6's relay claim,
independently reproduced to the digit with a from-scratch sieve implementation
(no GPT code, no sympy): C4 reduces exactly to a paired-gap prime census
(target N + 2⌈m/2⌉ — verified analytically against the probe's window
definition), and the HL even-gap singular series predicts it: 44,619 observed
vs 44,708.5 expected (0.99800) on m = 3..2999; out-of-sample m = 3000..9999:
317,255 vs 317,309.1 (0.99983), all three disjoint sub-windows exact to 5
digits. The d≡0 mod 3 ×2 local signature: 22,414 vs 11,107/11,098, exact.
Bonus per-residue signature: source-value mod 3 strata at 1.0007/0.9953.
**Verdict [E]: C4 was the null's arithmetic — same disease as PHASE 9, same
cure. P12 survives its strongest challenge yet.** Non-load-bearing: my
parity-sub-null (0.7713) differs from GPT's (0.9104) — sub-convention
difference, HL is the answer. Both candidate value-side anomalies (mirror
pairs, C4) have now dissolved into classical pair correlations; the open
question sharpens to: does ANY value-side statistic on this wheel survive its
correct null?

**J1c v2 (lab/J1C_wedge_result.md correction; probes/j1c_wedge_milp.py;
lab/J1C_spectrum_v2.json).** Grok's relay audit caught a real error: v1
measured wedge distance from home phase (−T) mod p; the cover rule implies the
shadow-aligned home is phase 0. Traced to an internal inconsistency in GLM's
frozen spec (c* vs cover congruence, off by 2T). v1 feasibility results
unaffected; all v1 distance statements superseded. v2 results, conventions
frozen in the note: object D ('ends') = Grok's 258/93 split *exactly*, all 93
at d = 1 (nothing "uncoverable"); object C (prime-eligible) = **bimodal by
parity**: even layers d = 1 throughout (GLM's parity-wedge theorem CONFIRMED
on sample), odd layers d ∈ [4, 22], 33 layers ≥ 263 infeasible by the capacity
bound φ(m) > Σ⌈m/p⌉ ≈ 0.84m + 25; near-wipe spectrum {d = 2} EMPTY — the odd
sublattice sits at d ≥ 4; object B (habitat-eligible) strictly harder, no d = 1
(parity flip orphans even-valued coprime ticks). Side-corrections: capacity
kills all-ticks wipe only for m ≥ 157 (not 41); trailing seat = T(m) =
m(m+1)/2. **The 2-adic spine scores a fourth instance: the wedge distance is
decided by ring 2** — even layers one flip away, odd layers far, ends smooth.

## 2026-10-11 evening — PHASE 11 calm-slope: pre-reg (a) FAILS LOUDLY, (b) PASSES inverted

Ran Claude's frozen lane pair-density sum (lab/PHASE11_calm_slope.py, conventions
C1–C9 frozen in-script; audit-first). Machinery VERIFIED exact before trusting the
fail: F[d] matches direct local counts (two real bugs fixed in flight — Legendre
sign, prime-power exponents — Kronecker table then sympy-verified on all 72 lanes,
zero mismatches); f(t)=t sanity returns -ln10; band-mean F = 1.0000 exactly.

VERDICTS. (a) FAIL: pooled 12-lane theory rungs 0.785/0.674/0.571/0.463/0.337/0.023
vs P9 measured 0.890/0.814/0.741/0.671/0.597/0.509 — off 2x at the FIRST rung, gap
grows super-log (T(W) drifts -5..-9/decade, rate still growing; the two-point sum
is not summable for quadratic lanes — D's split-prime lattice plants correlation at
every scale). (b) PASS inverted: with d^2==D terms off, per-prime average = prod
(p^2-4p+2)/(p(p-4)) ~ 0.40, S ~ -0.6W LINEAR — the common-root terms are
load-bearing for the log-law itself, not an 11% correction. GLM 0.64 ceiling:
truncated free-sum curve (0.82->0.58) misses his cut-off rungs at every level and
inverts the shape — same root cause.

GAP [S hypothesis]: the free quadratic singular series is the FREE-RING ceiling;
the wheel's lanes inherit P10 confinement and are calmer than any free-phase model.
Measured 11%-over-MS = gears' true contribution; naive 0.067 = plain-prime floor;
-0.14 = unachievable free-phase bound. The calm is MADE by confinement more than
gears. Discriminator: confined-phase prediction of the cut-off asymptote.
Side note: pbar 34.2 vs 29.2 convention logged, wrong direction, non-load-bearing.

## 2026-10-11 night — PHASE 12 (D2 filing): fire-count census + parity-dead channel family [E]

D2 = GLM audit-session "Draft 2 (fire-count census)". Its body was never relayed in
full — this is an INDEPENDENT RECONSTRUCTION from the three relayed descriptors,
filed with provenance [G] (reconciliation against GLM's original text open). Its
"C4 backbone" role is superseded: PHASE 10 closed C4 [E] as HL prime pairs.

Frozen conventions: rings = primes p <= sqrt(T(m)) (sieve boundary); a ring FIRES at
tick value N iff p|N; fire count f(N,m) = #{rings dividing N}. Channel (a,b): gcd=1,
visit g on layer m=gb at tick k=ga, value x = g(gb^2-b+2a)/2.

- [F->E] zero fires <=> N prime (composite N has a factor <= sqrt N, present as a ring).
  Zero class of the census IS the layer prime count — verified exact on 204 layers.
- [F, shape] mean f -> sum_{p<=sqrt T(m)} 1/p ~ ln ln m; within 0.5% at every layer.
- [F, THEOREM, verified both directions over 2,045,000 visits] a channel is parity-dead
  (every visit value even, no prime ever) IFF b even AND a == b/2 mod 2. Layer-side
  dual of B5: B5 = layer congruence (m==2 mod 4 kills seats), P-C = channel congruence.
  Minimal member: the half-turn channel (1,2) = the parity-axis values 2,8,18,32,50.
- [F, closed form, exact on 750 layers] dead ticks on layer m = sum_{b|m, b==2 mod 4}
  phi(b); b==0 mod 4 contributes ZERO (units of even b are all odd). Prereg's phi(b)/2
  line was a false step, caught in flight at m=4, corrected in the note.
- [E] dead ticks carry zero primes on all 750 layers m==0 mod 4 <= 3000; density
  mean 16.7%, max exactly 1/4.

Fifth instance of the 2-adic spine: parity decides the wedge distance (J1c), dial
luck (PHASE 9), the fine lock (PHASE 8b), and now an exact permanently-dead channel
family. Artifacts: lab/PHASE12_fire_census.{py,json,md}.

## 2026-10-11 night — PHASE 13 (relay adjudication): the calm's FAIL was three artifacts; confinement [S] retires; the wheel's third anomaly dissolves

Claude's 11d relay claimed my filed PHASE 11 (a)-FAIL was three normalization slips; GPT
sent corrections to my (b) filing; GLM pasted the original D2 and froze P13. House rule:
audit before accepting. Everything checked, several of my own claims corrected in place.

- **(a) FAIL superseded by PASS.** Fix 3 (decisive, my code bug): build_F applied the
  generic base to 1e7 but the common-root correction only to 1e5, leaving mean(F)
  7.9e-7 below 1 and S with a −7.9e-7·W drift — my "not summable" mechanism retracts
  (verified: drift/W = 7.94–8.01e-7 both lanes; last-decade slope −10.09 → −2.92).
  Fix 2 (Claude's handoff-c spec omission): the self-term — pooled R − 1 = Σ((e−v)/2)(S+1)/Σv;
  (e−v)/2 = Σp̄² exactly. Fix 1 (my sample): the 12 lanes are all 5-split (C = 0.7470 vs
  0.9996 over P9's 300). With all three: 300-lane pooled theory −0.0733/tenfold vs
  measured −0.0751 (frozen band ±0.005); every rung W ≥ 1e3 within 1.8 SE; 1e8 extrapolation
  0.4494 vs 0.4458 ± 0.036. Reproduced Claude's pooling independently (his S vs my
  build_F: 8e-9). **Calm slope on wheel lanes [E] = Montgomery–Soundararajan on the wheel's
  polynomial family** — C·S(W) = −ln W + O(1) lane-by-lane (BH constant = reciprocal
  residue of the pair series, Claude's exact identity). Third loud anomaly → classical
  law in one day (P9 mirror pairs, P10 C4, P11 calm). GLM's 0.64 ceiling also resolved:
  the rings ≤ 1000 truncation reproduces the sched column at every rung; plateau ≈ 0.68.
- **Confinement [S] RETIRED** — by normalization audit, not by a confinement experiment.
  GPT's §7 objection was the right instinct: the series was never free (ρ(p) = 1+(D|p)
  already carries the lane's confined quadratic structure). GLM's frozen c_pq prereg
  withdrawn by events.
- **(b) passes with corrected mechanism.** My printed no-cd mean formula was wrong
  (correct: μ_p = 1 − 2/(p−2)²; actual mean 0.70 not 0.40) — GPT's catch. His
  mean-preserving ablation reproduces exactly (μ to 9 digits; per-decade slope ratio
  0.40; ln-fit beats linear 1.1 vs 15.6): **mean-1 normalization is load-bearing for
  the log-law; common-root terms are its physically correct construction, not its
  unique source.** Fix 3 is the same artifact class in miniature.
- **PHASE 12/D2 reconciliation CLOSED** (GLM's verbatim draft in `lab/D2_original_GLM.md`):
  dead-tick count collapses to **oddpart(m)**; dead ticks are exactly one 2-adic shell
  {k : v2(k) = v2(m)−1}; density 2^{−v2(m)} (1/2 on m≡2 mod 4 including seats, 1/4 on
  m≡4 mod 8, …; asymptotic mean 1/6 over 4|m). Prime-2 exception restored (channel
  (1,2) carries 2). Trichotomy F ∈ {0,1,2} verified and needs no localization: x_g =
  g(b²g−b+2a)/2 kills g ≥ 3 outright; b ≤ 300 to 4e6 clean ({0:20201, 1:6764, 2:433}).
  Channel census (D2) vs tick census (PHASE 12): two objects, one engine. Grok's
  tightening adopted: four manifestations of ring 2, not five independent spines.
- **J1c capacity correction:** my "φ(m) > Σ⌈m/p⌉ ≈ 0.84m+25" certificate was wrong
  (Σ1/p = 1.80 over the 25 rings; Σ⌈m/p⌉ ≈ 1.83m > m always — certifies nothing, on
  objects A and C alike). The 33 infeasible layers are exact-cover structure: random
  placement covers ≈ 0.88(m−1), structured placement wins up to a cliff — prime layers
  feasible with d ≈ 0.0737·m + 0.64 (r = 0.978) through 257, ALL infeasible from 263;
  the 11 infeasible composites all have large-only prime factors. Cliff mechanism [G].
- **GLM's P13 scored:** (i) holds 99/100 finite composites (m = 55 exception); (ii)
  partial (d = 4 spans φ/m to 0.727; smoothest 3^k-class absent); (iii) confirmed;
  (iv) falsified — prime-layer d is a linear curve, not a constant 11–12.

House-rule tally for the night: my code bug (load-bearing), my sample bias, my formula
error, my overclaim, my wrong certificate — five self-caught/caught-by-swarm corrections,
all logged in place. The day's running score: every loud value-side anomaly dissolves
under its correct null; the method (freeze → fail loudly → audit → classical) is now
three for three.

## 2026-10-12 post-midnight — PHASE 14: 7/6 CLOSED [E]; J1c cliff CLOSED [F+E]; audits all green

- **7/6 dial, m = 10^6: CLOSED [E].** Independent reproduction of GPT's
  census matched every frozen number to the digit: F1 = 8,280 / F2 = 8,180
  against BH predictions 8,222.12 / 8,221.78 (C = 4.9116695006), total ratio
  1.00098; the m <= 200k sub-window matched to the unit (1,871 / 1,905) —
  which also retro-validates the dial sweep's originally filed counts. MR
  validated against SymPy on 600 values before counting; ties-up convention
  verified (GLM's round() landmine does not bite: PHASE8b is ties-up, and a
  warning comment now guards ratio_sweep.py's banker's-rounding wart).
  Second Euler-grade dial family confirmed; value-side ledger extends to
  16,462 total half-turn primes (GPT's factorable-branch census, checked by
  expansion).
- **J1c feasibility cliff: CLOSED [F + E].** GPT's CRT reduction verified
  against the frozen v2 convention: 25 one-hot phases <-> Delta mod 97#, so
  prime-layer wipe feasibility = existence of m-1 consecutive Q-non-coprime
  integers = primorial Jacobsthal. h(25) = j(97#) = 258 (Hagedorn 2009,
  OEIS A048670): last feasible prime 257, first infeasible 263 — exactly the
  measured edge. Grok's table is the same theorem. Correction filed in
  J1C_wedge_result.md v4: "all-ticks feasible iff 2..13" was a d = 0 census;
  the true statement is d = 0 iff m <= 13, feasible iff m <= 257, with the
  object-A d-curve measured by exact MILP (d ~ 0.0747m + 0.54 through 257,
  all finite; None from 258, theorem-guaranteed). The pre-cliff slope is
  object-independent (0.0747 all-ticks vs 0.0737 prime-layer) — the shared
  [G] is now "why ~m/13.5", well-posed as a primorial CRT Hamming distance.
- **pair8.c (1e8 calm rung) verified [E]**: G to 12 digits, S rungs to 4e-10
  under the frozen fix3 convention (bp over ALL split primes <= bound — the
  stale B2 = 1e5 default in my own harness reproduced exactly the 0.7 S-shift,
  a second independent confirmation of fix3's magnitude). Latent wart noted:
  unbounded weights-grid read, >65536 lines segfaults (non-load-bearing).
- **P15 foundation verified**: Claude's layer counts zero-mismatch vs my
  independent column engine over all m <= 1e5. The wheel-rings-at-the-zeros
  result rests on verified data; explicit-formula reading is known math,
  wheel-native, as framed.
- **Meta**: third straight relay where every load-bearing claim survived
  independent audit modulo one terminology correction (d=0 vs feasible) and
  one notational garble (GPT's "h(n)=2omega(n)+2", non-load-bearing).
  House rule candidate reinforced: census claims must state the displacement
  regime they census.

## 2026-10-12 morning — PHASE 15 (autonomous): the 1/13.5 slope decomposed

The wedge displacement cost d ~ m/13.5 (object A, 25 fixed rings) splits
into two loads [S->fit, R^2=0.974]: rough-tick harvesting
(0.215 * U, U = 97-rough tick count, density e^{-gamma}/ln 97 ~ 0.123) plus
re-cover overhead (0.051 per tick). Slope arithmetic: 0.215*0.1227+0.051
~ 0.077 ~ 1/13.0 vs measured 1/13.4 — the constant is set by the RING
BOUND B, not free. Consequence: native schedule (rings = primes <=
sqrt(T)) should make d sublinear in m (U collapses to the prime count).
LEG S: j(31#) <= 60 (infeasible at 60/100/150); 100 < j(53#) <= 150;
B=53 finite points sit +2.2 above B=97-constant predictions (fewer rings
-> costlier per rough tick) — constants are B-dependent as theory requires.
LEG N (native rings, m=263..1000): first point d=15 vs P=28 (d/P=0.54,
below the harvest-only band — more rings harvest more efficiently).
Full note: lab/PHASE15_wedge_slope.md. Object C is parity-dominated
(GLM's parity wedge), prime-count model correctly FAILS there (H4).

## 2026-10-12 morning — PHASE 15 (part 2): the 1/13.5 slope is ring-budget-contingent [E]

Leg S (fixed-B sensitivity): B=31 infeasible already at m=60 (j(31#)<=60);
B=53 gives d=7/11 at m=60/100 then infeasible at 150. Cliffs land exactly
at the Jacobsthal boundaries of the ring primorials [F+E]. Leg N (native
schedule, rings = primes <= sqrt(T)): d finite at m=263/300/400/600,
d/P stable ~0.5 (BELOW the B=97 harvest constant 0.65 — harvest efficiency
rises with ring density [S]), and d/m declines monotonically
0.057 -> 0.043 across the measured range: growth is sublinear, ~0.5*m/(2 ln m).
m=1000 OOM-killed at the MILP build (19.8 GB rss) — infrastructure, not
science; needs a streamed formulation. Full adjudication:
lab/PHASE15_dynrings.md.

## 2026-10-12 afternoon — Downloads archive sweep (5-agent triage)

Full corpus (`~/Downloads` 711 prime files, WhitePapers/119, Collatz, Erdős) triaged → `lab/ARCHIVE_TRIAGE_2026-10-12.md`. Recovered two live relay artifacts that were sitting in Downloads, not the repo: SWARM_HANDBACK_2026-10-12.txt and REVIEW_2026-10-12 (Mark French & Claude; independent verification all ✓, one fix already known). Genuine ADDS found: (1) Echo Cascade 2p±1 adjacency census to 5e7 (balance 1.000065) — doubling-graph territory the wheel doesn't cover [S, un-audited]; (2) PRIME² isolated-prime classification — printed sequence/density FALSIFIED in triage (true: 17,43,67,71,101,103,109,127,137…; density ~1-4/ln p, not 15.4%); (3) two never-rebooted ancestor measurements: knockout wall profile (~50% sub-√x wheels used, largest-needed →98% of √x by layer 3000) and chained double-shot census (2p+b², 10062 double-prime spokes ≤2000); (4) Hooley 1965 exponential gap law for primorial-coprime integers [E] — NOT in LITERATURE_SWEEP_2026-10-10, the one real lit gap; benchmark candidate for dial-census gaps. Collatz/Erdős corpora: nothing wheel-adjacent (Collatz scale-basin verifier = reproducible NEGATIVE result, re-confirmed). Harmonic twin-prime "test" falsified: vacuous for odd n.

## 2026-10-12 afternoon — ARCHIVE QUEUE run: all five triaged items measured

Queue from the Downloads/WhitePapers triage executed as one probe
(lab/ARCHIVE_Q_2026-10-12.py, 6.3s; writeup lab/ARCHIVE_Q_2026-10-12.md):
- Q1 Echo Cascade 2p±1 census: PASS. pi(5e7)=3,001,134 exact; counts match to
  p=2,3 edge conventions; balance 1.000070 vs claim 1.000065; mechanism named
  (mod-6 forced 3-divisibility, kills 1,500,652 vs 1,500,480); corollary [F]:
  p=3 is the ONLY prime with both 2p-1 and 2p+1 prime. Their "stability"
  metric undefined in corpus [G], uncheckable.
- Q2 isolated primes: PASS. Sequence 17,43,67,71,101,... confirmed; density
  0.583->0.757 below 1e4..1e7 tracking 1-4/ln p; PRIME^2's 15.4% stays dead.
- Q3 knockout wall: PASS, ancestor claims reproduced in the reboot (share
  0.46-0.59 settling ~0.5; biggest-needed/sqrt -> 0.981 by layers 2000-3000).
- Q4 double-shot census: 10,062 reproduced EXACTLY; all double-prime spokes
  odd-b (parity mechanism [F] confirmed). BH predictions all underpredict,
  monotonically closing: naive 4,110 -> standard SS 7,582 -> family-restricted
  SS 8,672 vs observed 10,062; residual 1.16x FLAT across b (not small-N).
  [G] uniform density excess; follow-up: Sophie Germant calibration to split
  machinery bias from structure.
- Q5 Hooley 1965: frozen finite-k statement FAILS (KS 0.29-0.32, not
  shrinking) BUT the theorem's actual hypothesis is n/phi(n) -> infinity —
  enumerable primorials cap at n/phi ~ 7.5. One-period gap law = Exp(1)
  squeezed by lattice floor (c >= 2phi/N) + Jacobsthal cap (max gaps 22/26/34
  = j(N_k) exactly, cross-checking PHASE 14). [E] stands; truncated-fit
  follow-up proposed. Added to LITERATURE_SWEEP as addendum.

## 2026-10-12 evening — 17:19 relay adjudicated (six voices), Q4 dissolved, N1 → theorem, P11 record corrected

Full adjudication: `lab/RELAY_2026-10-12-evening.md`. Relay artifacts in `handoffs/`.

- **[E] Q4 double-shot excess DISSOLVED.** Claude's pre-sieve mechanism (shots ≡ a, 2a mod every ℓ|b ⇒ local factor (1−1/ℓ)⁻², 𝔖_fam = 2C₂∏ℓ/(ℓ−2)) reproduced here exactly: pred 10,138.2 vs 10,062 observed (ratio 0.9925); correction chain 5,008 → 7,582 → 8,672 → 10,138 all on record. Fourth value-side anomaly to fall to Bateman–Horn under its correct null. Value side now 0-for-4 against the fence; meta-arc (Claude's standing claim) keeps winning.
- **[E] Native Jacobsthal windows VERIFIED.** Infeasible set {2–18, 22–24, 26, 27, 40, 41} reproduced exactly from the j(p_k#) table under the rings≤√T(m)/(T(m),T(m+1)] convention (the one GPT's sparse script implements); every m ≥ 42 wipeable ⇒ **N1 is a theorem**, contingent on convention standardization. Caveat filed: PHASE15_dynrings.py's header convention (√T(m−1)) gives a different infeasible set — the two solvers differ by a one-layer shift. Pin the seam convention lab-wide (GPT's warning, elevated).
- **[E] Sparse one-hot MILP verified** (m=263: OPTIMAL d=15, ring 2 home, 12 s, ~15k nnz). Dense-build OOM family dead.
- **[F] GPT prime-square boundary correction verified by arithmetic** (U=P+ε; m=400: 283²=80089).
- **[E] P11 RECORD CONTRADICTION CONFIRMED (GLM's grep request executed).** Frozen script rule (`mh_all > 4*mr_all`, mr_all a mean of absolutes) can only fire on a POSITIVE mean; INSIGHTS pre-reg predicted NEGATIVE ≥3 SE; measured −0.0073 stable across halves (~4.6σ). The two frozen texts give opposite verdicts on the same number. P11 verdict SUSPENDED; entry amended here rather than edited (append-only). P11c fired: reproduction + 200 parity-stratified surrogates + 200 plain shuffles, null-before-signal. Verdict deferred to the null.
- **[S→audit] GLM's CRT-shift collapse** accepted pending independent re-derivation: covered(N) ⟺ gcd(N−a,Q)>1; d = #{p∤a}; feasibility position-independent; wedge = pure arithmetic, no MILP at any m; "why m/13.5" = ω-degradation rate of Jacobsthal run-starts. If it survives audit it is the largest simplification since the cliff.
- **[G→queued]** m=1000 sparse MILP running detached (3 h limit, lab/PHASE15_sparse_m1000.log); P11c verdict; convention standardization; C(X) truncation law prereg; B=67/79 harvest point; conditional ring-2 split (d_home vs d_flip); Gemini spacing-variance dump.
- Cloud: ~$20 credit noted; not needed while sparse build fits in 2 MB — B&B time, not RAM, is the wall. GLM's SAT route may remove that too.

## 2026-10-12 late evening — overnight jobs resolved

### P11c (record-repair run): mostly explained by phase structure, residual marginal
Deterministic arm reproduced obs = -0.00731 exactly. Two nulls:
- plain shuffle null: mean -0.00012, sd 0.00054 -> z = -13.4 (the naive read; NOT the
  honest one, since phase structure is real physics of the arm)
- phase-stratified null (shuffle within each ring-2 phase class): mean -0.00620,
  sd 0.00051 -> obs -0.00731, z = -2.16, two-sided empirical p = 0.015 (200 surrogates)
Verdict: ~85% of the negative lag-4 displacement correlation is carried by ring-2's
phase-class structure itself (forced arithmetic, not evidence); the residual is a
marginal 2.2-sigma negative hint. P11 verdict repaired: NOT "positive mean, PASS"
(script text), NOT "clear negative pattern" (INSIGHTS text) — it is
"[marginal negative residual after phase stratification, p=0.015, needs a
pre-registered replication at a different M_HI before any weight]".
Log: lab/P11C.log; json: probes/logs/stagger_acf_p11c.json.

### m=1000 sparse MILP: ran to time limit, d=38 (not proven optimal)
GPT's sparse build scaled fine (40,313 vars, 166k nonzeros, 2 MB class matrix).
10800 s limit hit at d=38, best bound 32, gap 15.8% — incumbent not proven.
Consistency check: native-schedule law d ~ 0.5*m/(2 ln m) predicts 36.2 at m=1000;
incumbent 38 sits 5% above. Consistent with the law's historical scatter; the
law is not contradicted but m=1000 joins {251} as a proven-or-near d point.
Log: lab/PHASE15_sparse_m1000.log.

## 2026-10-13 morning — site sync + GLM collapse audited STANDS [E]

Site sync (commit 273f443): PAPER.md §10 (displacement curve, two loads,
native-schedule sublinearity, N1, 4th BH dissolution), WHITEPAPER.md §15
(wedge era) + open-problems refresh + Hooley/Hagedorn refs; whitepaper.html
BUILT for the first time via tools/build_whitepaper.py (grand.html's White
Paper tab had 404'd since the rail was written). Pushed; ostoe.com rsync'd.

GLM CRT-shift collapse AUDIT — STANDS, all legs PASS [E]
(lab/GLM_COLLAPSE_AUDIT_2026-10-13.{py,md}, ~16 s):
- LEG 1 exhaustive Q in {6,30,210}: identity covered(N) <=> gcd(N-a,Q)>1,
  feasibility <=> m <= j(Q)-1, and d = #{p !| a} = |P| - max omega_P(a),
  over ALL translates/windows. j(6,30,210)=(4,6,10) by scan.
- LEG 2: GLM's m=14 witness reconstructs exactly (a = Q_odd, d=1, d=0
  blocked by 97-rough 101/103) — matches measured d(14)=1.
- LEG 3: B=53 recomputed MILP-free: d(60)=7, d(100)=11, infeasible@150
  (also instant from j(53#)=106). LEG S reproduced from arithmetic alone.
- LEG 4: A048670 confirms j(31#) = 58 exactly as GLM stated (resolves our
  "j(31#) <= 60" bracket to the exact value).
Consequences: feasibility closed everywhere by table; d(m) = small
prime-set exact cover (m=1000 native now a 127-prime SAT, not a 40k MILP);
"why m/13.5" is now the omega-degradation law max|S|(m); slope-universality
attack is pure arithmetic. Naming pinned: house h(k)=j(p_k#) (first
infeasible layer) vs "max coverable window" = j(Q)-1.

## 2026-10-13 late morning — dial-theorem evidence swarm: question SHARPENED

Three-agent evidence pass (census definition / arithmetic / geometry):
- "Modal" was naming [S]: measured content = argmax of live-family singular
  series C over the 20-ratio b<=8 sweep (7/6: 4.89, 5/4: 4.50, else <=3.8) [E].
- Argmax is resolution-dependent: 14/11 (C~5.13) at b=11; b<=60 ratios like
  59/46 reach ~6.64. max-C confounds denominator size with live-family count
  (lottery tickets). 8/7 fully parity-dead (0 eligible classes).
- 7/6 not arithmetically unique: 5/4, 9/7 (C=4.44), 6/5 (C=4.14) share the
  full profile (h=1 kernel, identically-odd family, bad-prime losses).
- Surplus mechanism decomposed [S on measured inputs]: 2-adic x4 (b-even dial
  deletes ring 2 where 2 splits) + bad-prime root losses (rho(3)=0 x1.5,
  rho(7)=1 x7/6); small-L(1,chi) guess refuted (L(1,chi_57)=1.513).
- Nothing geometric peaks at 7/6; Gemini spacing-variance dump still does not
  exist (and concerns 1:1 wheel witness boundaries, not the dial).
Sharpened open question (WHITEPAPER §13 amended in place): what selects the
winning field club, and at what resolution is argmax-C a stable statistic?
Next instrument: C-decomposition census across a wide ratio grid.

## 2026-10-13 late morning — PHASE 16 both probes: alternatives pass complete

### Dial C-decomposition census (lab/PHASE16_dial_census.md, .json, _grid.json)
Full coprime grid b<=60, 1<=a<=2b (2202 ratios; 2132 live). Adjudications:
- D1 PASS (7/6 argmax at b<=8), D2 PASS (89/46 argmax at b<=60).
- D3 REFUTED: logC2 = log 2 for ALL 2132 live ratios — parity eligibility
  filter forces odd families; the 2-adic factor is universally x2 and
  cannot select. "b-even dial deletes ring 2" is dead as a selector.
- D4 half: 7/6 bad-prime factor at 3 = 1.5 exactly; the "x4" was wrong
  (absolute x2, universal).
- D5: top-5 SET identical small-C vs full-C; internal order is cutoff
  noise (2% cluster).
- 7/6 rank by resolution: 1/35, 3/78, 14/232, 48/521, 442/2132.
- MECHANISM [F from measurement]: C-selection = prime-avoidance
  constellation = inert-prime profile of the family's quadratic field
  (rho=0 <=> inert). Leaders keep ~15-16 of 19 primes p<=67 inert with
  split losses only at large primes; 7/6 has 11 inert + 6 split losses.
  The dial's real role is lattice richness (family count grows with b:
  7/6 has 2, 45/47 has 60) — argmax-C resolution-dependence is a
  best-of-N SEARCH effect, winners saturating at C~6.6-6.8.
- Two winners by statistic: best family 89/46; total haul (sumC) 1/59.

### Omega-degradation curve (lab/PHASE16_omega_curve.md, .json, .log)
Collapsed exact-cover, no MILP. Slopes measured exact: k_31 = 0.1386,
k_53 = 0.10367, k_97 = 0.07472. k(B) = 0.876/ln B - 0.117 fits 3/3
[S->measured; discriminating test: B=131/151 predicts ~0.066/0.063].
F1 frozen bands FAIL (measured well above two-load extrapolation at
small B; 0.215/0.051 constants do not transfer down-B — right 1/ln B
shape, wrong amplitude [G]). F2 PASS (above-mechanism direction).
F3 PASS (collapsed DFS == MILP at B=97 m=60, d=6). F4 PASS (omega
24->3). LEG D bind: two instruments agree at 25 rings [E].
Native: m=300 d=16 (47 rings), m=400 d=19 (60 rings), both PROVEN
OPTIMAL (sparse MILP, 19s/40s). Law d ~ 0.5*m/(2 ln m) systematically
low, converging: d/pred 1.26 -> 1.22 -> 1.14 -> 1.05(incumbent).
Named follow-ups: B=131 slope point; native m=600; d_home/d_flip as
omega-accounting (GPT queue #6).

## 2026-10-13 midday — UNIQUENESS TEST spec filed (flagship relay item)

SylvaN's pillar added to the geometry-first claim: "we don't need to compute a
thing, just roll" — the wheel's function is realized by motion, not symbol
rewriting. Spec: `lab/UNIQUENESS_TEST_2026-10-13.md`.

- Three scoring axes: A generative closure (gate + constellations), B intrinsic
  verbs (displacement/turning owned by the object), C realization economy
  (actuation ∝ laps, parallelism geometric).
- [E] Axis C is historical, not hypothetical: D.H. Lehmer's 1927 sieve was 19
  bicycle-chain loops whose lengths ARE moduli (64, 27, 25, 49, 22, 26, 17, …,
  67) with pins as excluded residues — one chain per ring. The physical wheel
  was already built once.
- Pre-registered predictions [S] for 8 candidates before survey; upset
  candidate designated: prime-generating cellular automata (maybe on B).
- Methodological note: this test is the operational form of the morning's
  direction-of-explanation correction — "the wheel is what makes it true, and
  'it' is the bundle."
- Open [G]: G1 self-assembling masks/unit/L-build; G2 formal cost model for
  "just roll" (analog complexity as parts catalog); G3 CA verb survey.

Queue status: B=131 slope point, native m=600, d_home/d_flip ω-accounting still
awaiting fire command; relay handoff drafts from this spec + PHASE 16.

## 2026-10-13 midday — PHASE 16 (cont.): B=131 slope point + home/flip accounting

Queue items from the morning report, all three fired. Collapsed covering ILP
(`lab/PHASE16_b131_homeflip.py`), all solves optimal, zero gap:

- **B=131 slope point [E]**: k131 = 0.0578 vs 2-param prediction 0.0627 — PASS
  at 8% deviation. The 1/ln B k-law survives its first honest test; still
  [S]-grade (2 params / now 4 points). Side catch: all grid m feasible →
  j(131#) ≥ 201 (E-checkable against Hagedorn's tables).
- **d_home/d_flip ω-accounting [E]**: m=263 — free=home=15, flip=17 (B1 binds
  ILP to MILP to the unit; universal-flip dead, certified optimal). m=100 —
  free=flip=9, home=10: the gap REVERSES sign with m. |gap| ≤ 2 at both
  points: "the turning is not a ring-2 artefact" now holds at both ends.
  B2 frozen sign prediction refuted at m=100, filed as such.
- **Uniqueness test**: axis C2 (raw-state legibility, the movie-wall frame)
  added with pre-registered predictions; Lehmer 1927 [E] precedent already
  filed in the spec.
- **m=600 native MILP**: fired detached (PID 3480815,
  lab/PHASE16_sparse_m600.log, 3 h limit) — pending at filing time.

Lab note: lab/PHASE16_b131_homeflip.md

## 2026-10-13 early afternoon — native m=600 MILP lands: d=26 PROVEN OPTIMAL

`lab/phase15_sparse_relay.py 600` (82 rings, 15,537 vars): status Optimal,
d = 26, 294 s. Native-schedule law `d/pred` (pred = 0.5m/(2 ln m)) now
1.26 → 1.22 → 1.14 → **1.11** at m = 300/400/600 — still systematically
low, still converging. The arithmetic queue is fully closed; the board is
ready for the updated relay handoff.

## 2026-10-13 afternoon — 13:29 day-relay handback adjudicated (six voices + Claude)

Full adjudication: `lab/RELAY_2026-10-13-day.md`. Spec amendments: `lab/UNIQUENESS_TEST_2026-10-13.md` §8 (v2 addendum; v1 frozen text untouched).

- **[E] j(131#) = 378, j(167#) = 510, j(53#) = 106** — OEIS A048670 verified directly; j(53#) additionally pinned by our own exact-cover translate scan in 3.2 s (GLM's request). GLM's indexing hazard checked: unfounded (a(10)=46; a(11)=58=j(31#) consistent with the morning audit) — discipline adopted anyway.
- **[E] All-inert ceilings computed:** ≤53 budget ×2 = 7.348 (Qwen's 7.28, mechanism right); full ≤67 budget ×2 = 7.7147 (GLM's range). 89/46's 6.834 = 93% of the ≤53 ceiling.
- **[F] Uniqueness Test v1 scored to death in 3 hours — as designed.** B was circular (question-list ownership: Grok, GPT, Claude independently); prediction #3 "pure CRT fails B" REFUTED BY OUR OWN collapse (the CRT torus owns displacement: d(x,0)=Σ 1[x_p≠0]). C2 v1 conflated coordinates with legibility (GPT §6: a zero cell is as positional as a hole) — v1 CA prediction refuted by Wolfram p.640 / Umeo–Kamikawa prime CAs [E]. Adopted: B_math/B_phys split; C2 v2 re-frozen on GPT's four bullets (rubric-first before scoring, per DeepSeek); C_fixed/C_growing cost split (GPT §7).
- **[F] GLM's R1+R2 adopted as the v2 core:** gate-intrinsic (R1) + temporality triple (R2: intrinsic time, persistent phase-bearing agents, growing frame) ⟹ "the wheel is the unique simple object whose state space is a stagger field." Conditional uniqueness — the form that survives a referee.
- **[F] THE SEAM LOCK (Claude's find):** among linear-turn spirals, turn length m uniquely phase-locks ring m to its own layer (T(m−1)=m(m−1)/2). Ulam 8m: no lock. Sacks 2m−1: seam at k², no lock. Discriminating experiment pre-registered: Lehmer-chains-on-Sacks vs wheel; Claude's prime-layer prediction (#18) is the cheap existing-count test. New slogan [S]: motion-sieve dynamics on the one linear spiral whose turn length locks to its seam.
- **[E] Three new rivals admitted:** Fischer 1965 prime CA (the upset made concrete — rings as bouncing signals), Hickerson's Life primer, PRIMEGAME. All fail R1/R2 for named reasons; scoreboard: no rival takes the wheel's whole row — the corner is the pairing + stagger-field triple + seam lock.
- **[S→queue] GPT's restricted classification theorem:** uniqueness up to equivariant isomorphism in the five-primitive class (one cyclic phase per prime, one excluded class, OR-composition, independent translations, home config) — the theorem-shaped core of the flagship.
- **[S frozen-exploratory] GPT's alternative slope law** k ≈ c·π(B)/j(B#), c≈0.70–0.75; k(167) ≈ 0.0558 vs frozen log-fit 0.0542 — too close at 167, reserve larger B. Frozen log prediction NOT replaced. Normalized position x = m/(j(B#)−1) adopted for d-curve analysis.
- **[F] GLM's two failed heuristics filed:** aggregate harmonic relaxation vacuous (home classes pinned, not chosen); coupon-collector contradicts measured covers ⟹ the slope is genuinely run-structural. His cliff reframe adopted: near h(Q) the qualifying-translate set collapses to ω-poor generic positions (ω=3 vs E[ω]=1.80); degradation = set-shrinkage.
- **[E] P11 answered for GLM:** the thread was NOT dropped — adjudicated 10-12 evening, P11c run with the honest null: phase-stratified z = −2.16, p = 0.015; ~85% carried by forced phase-class arithmetic; needs pre-registered replication at a different M_HI. His 5σ framing superseded. Real failure: handoff completeness (now corrected).
- **[C] Four fact-level fixes:** 6k±1 ≠ sexy primes (coprime-to-6 seats — Grok's catch); Lehmer mid-prime doubling restored (46/74/94 — GLM's recall canonical); bicycle-chain (1926/28) ≠ photoelectric (1933) machines unmerged; dial-census ⟺ statement qualified (exceptional primes; code already correct by direct scan).
- **Handoff-completeness lesson [F]:** GLM's P11 grep request reached us already executed — the day handoff's queue must carry verdicts-in-flight, not just open items.

## 2026-10-13 late afternoon — PHASE 17: #18 seam-lock check PASS; P-TRI step 2 filed as [G]

Claude's #18 (prime layers less seam-locked) decompressed to pure wheel arithmetic:
ring q hits tick 1 of layer m iff m^2-m+2 ≡ 0 mod q (disc −7 — exactly why r_q = 1+(−7|q)).
Measured 300k layers, odd q ≤ 97: prime-layer rates match r_q/(q−1) at |z| ≤ 0.46 everywhere
including degenerate q=7 ((−7|7)=0, single root, emp 0.16658 vs 1/6); r_q=0 primes exactly zero;
lift = q/(q−1) at every q (7/6 is a statistical lift, flagged in advance, NOT dial evidence).
Our frozen P1 composite expectation mis-specified by the prime-bucket subtraction (z=−3.37 at q=7,
deficit predicted 0.00227 vs observed 0.00225 — corrected, all cells |z| ≤ 0.46). P4 layer-content
extension FAILS honestly (no correlation; prime counts phase-insensitive to first order — named the
phase-sensitive observable for a future probe). N1 re-verified 3..20k from our own sieve.
P-TRI step 2 NOT run: engine absent from repo; both reconstructions fail against Claude's published
#16 numbers — native reading refuted by the u=0 witness (8T(m−1)+1 = (2m−1)^2 ⟹ seam anchor always
triangle-consistent ⟹ every layer coverable). Question relayed: P-TRI's window/ring-bound/phase-domain
conventions, one line, then step 2 is an afternoon.

## 2026-10-13 night — 20:21 handback adjudicated; P-TRI CLOSED; Gemini dump fired; m=1000 running

- **Seam lock retracted at class level** (Claude/GPT/Grok, three-way
  independent): the lock is generic to L = a·m. Survives, theorem-grade:
  GLM's lock+palindrome lemma (γ=0 ∧ α+β=0 ⟹ B = T(m−1) uniquely;
  verified here), Claude's a=1 residue, GPT's restricted classification
  theorem + exact-stagger rigidity. Folded into v2 spec as dated
  correction §10, failed prediction preserved with scope.
- **P-TRI acquitted [E]:** two independent exact-cover implementations
  agree to the unit; published set reproduced EXACTLY as tri∖free (the
  confinement-delta) — Claude's "exact equality" was imprecise, content
  fully recovered. Our afternoon u=0 kill retracted (R7). Reading B
  confirmed; GLM's Reading-A "universal feasibility" refuted for the
  one-offset-per-ring engine (holds only for the per-ticket QR
  relaxation). Frozen: no new tri∖free-infeasible layers in 61..80.
- **Discriminant twin Δ(a)=a(a−8)** verified: −7 shared by 1:1 and 7:1
  at every odd prime ≠ 7; q=7 cell is the discriminator (already in
  PHASE 17 data). PHASE 17 arithmetic stands, "unique seam geometry"
  interpretation retired (R8 framing).
- **Gemini dump [E]:** GEMINI_DUMP_2026-10-13.json — uncovered-k arrays
  at sieve-bound entries m0 = 17 (p=11), 138 (p=97), 364 (p=257),
  ±5 windows. Hand-verified p=11, m=17.
- **m=1000 native fired detached** (PID 3640867, PHASE18_sparse_m1000.
  log, 3h cap) — tests GLM's frozen F2 band d ∈ [37, 43].
- Adopted: Jacobsthal-translate-spectrum naming; Fischer CA best rival
  (fails only growing frame); Grok's creep precondition (check inert
  feasibility before extending census); GPT's A1/A2/A7/A8 affine-rival
  experiment pre-registered; Claude's Sacks "loses nothing structural"
  prediction recorded with refutation condition.

## 2026-10-13 night — m=1000 native MILP: d=38 FEASIBLE, optimality NOT proven

`phase15_sparse_relay.py 1000 10800 free` hit the 3 h cap: incumbent d=38
(126 rings, all laps covered), dual bound 32, gap 15.8%. True d(1000) ∈
[32, 38]. GLM's frozen band [37,43] is consistent-but-unconfirmed (dies if
opt < 37). Incumbent native-law ratio 1.05 continues 1.26→1.22→1.14→1.11
downward, but as an upper bound, not a proven point. Note: lab/PHASE18_sparse_m1000.md.
Options for relay: accept weaker line, overnight 12 h rerun w/ warm start.

## 2026-10-14 post-midnight — m=1000 verdict + night handoff

**m=1000 [E]:** 3h cap hit honestly — feasible d=38 (126 rings, 0 uncovered),
optimality unproven, dual bound 32, gap 15.8%, opt ∈ [32,38]. GLM's frozen
band [37,43] alive, half-tested. Ratio on incumbent continues 1.05 (upper
bound, not proof). Overnight 12h plain rerun fired PID 3718615 (cap ~12:15);
warm start impossible — incumbent translate vector wasn't persisted (lesson:
persist solution vectors). Log: lab/PHASE19_sparse_m1000_overnight.log.

**Handoff:** handoffs/HANDOFF_2026-10-14-night.md — closes the 20:21 round:
m verdict + P-TRI closed [E] (published set = tri∖free reproduced exactly,
both implementations) + seam-lock dated correction + 7-item standing queue.
Bundle refreshed.

## 2026-10-14 06:07 — m=1000 overnight rerun CLOSED: d=37 PROVEN OPTIMAL

12h-cap rerun closed in 4h57m. Objective 37 = bound 37, gap 0. GLM's frozen
band [37,43] PASSES at the low edge — fully tested. Ratio sequence on PROVEN
points: 1.26 → 1.22 → 1.14 → 1.11 → 1.02 (pred 36.19). Additive residual
d−pred: 3.1 → 2.8 → 2.3 → 2.55 → 0.81 — NOT monotone; ratio→1 supported,
smooth additive decay refuted by the 600→1000 step (1-ring quantization or
finite-m correction [G]; next point m=1500 or 2000). Night handoff §1
amended in place with the update. Five native proven points total.
Artifact: lab/PHASE19_sparse_m1000_overnight.md.

## 2026-10-14 morning — 07:40 handback adjudicated (PHASE 20): F5 verified, Q1/Q2/Phi confirmed, Sacks tension resolved, d/P band fails

Relay (`lab/RELAY_2026-10-14-morning.md`, probe `lab/PHASE20_relay_oct14.*`):

- **[E] GLM's F5 normalization catch verified to the cent.** Our pred denominator was wrong by ln 4: the law is d ≈ ½m/ln T(m), residuals 2.42/2.00/1.29/1.21/−1.10, monotone, zero-crossing between 600 and 1000. The "non-monotone additive residual" [G] we filed was in the formula, not the physics. Qwen's "1-ring quantization noise" story retired with the artifact it explained.
- **[E] All-inert D-scan |D| ≤ 10⁶: zero witnesses.** Creep to the 7.7147 ceiling unreachable at dial grids; F3 bands stand (Grok/Qwen precondition closed at this range).
- **[E] GPT's Q1 + Q2 both confirmed.** Q1: reflection + odd seam lock ⟹ B(m) = a·C(m,2), a free (GLM's original lemma is intact — our relayed one-liner dropped his explicit 1:1 hypothesis; handoff underspecified, per GPT's own disposition). Q2: twin-prime ring-entry gate, exhaustive ≤257 zero violations, two implementations; 97/257 entry events change NOTHING (Δ variance exactly 0.000; 11's Δ is a hole-count artifact, flagged for Gemini).
- **[E] Φ_a conjugacy confirmed** incl. p=7 collapse 4→1 — the q=7 discriminant-twin cell IS where the phase automorphism loses invertibility. Adopted as the unified explanation of PHASE 17's q=7 exception.
- **[E] Sacks localization tension resolved: both voices right, Claude scope-limited.** P-SAX tested tick-1/dead-columns/seam-profiles (all pass, verdict stands there); GLM's two-shot localization is an untested observable and lands: Sacks spokes carry primes at unbounded depth (up to 148 in-table), blocked only at g+1 | C(a,b). **Patch to GLM's wheel side:** "forbids depth ≥ 3 absolutely" holds from depth 4 up; at depth 3 the value 2b²−b+2a is prime on 14/28 spokes (g=2 consumed by the /2 — the same free-parameter catch as Q1). Wheel caps at depth 3 with a primality window; Sacks unbounded. Lehmer-on-Sacks discriminator armed with the corrected table.
- **[E] GLM's F2 d/P companion band FAILS: P(1000) = 82** (primes in layer [499501,500500]), d/P = 0.4512 ∉ [0.49,0.56]. Sequence 0.536/0.593/0.487/0.491/0.451: asymptotic "→ ½" survives, the band doesn't. d-band [37,43] PASS stands.
- **m=1500 fired** (PID 3900666, 24h cap, `lab/PHASE20_sparse_m1000.log`-style log at `lab/PHASE20_sparse_m1500.log`) against GLM's frozen d(1500) ∈ [50,57], pred 53.8.
- **Process:** Qwen/Gemini responses byte-identical this round (flagged to Obi). DeepSeek's "scope inflation" diagnosis adopted as standing bias warning — this round's instances: our palindrome one-liner, GLM's depth-3 wording, Qwen's noise story.

## 2026-10-14 morning — Gemini's Δσ²: numbers reproduced, "phase-lock confirmed" refuted by control

`lab/PHASE21_gemini_variance.md`. Her convention (sample var of consecutive
gaps, Δ across m₀±1) reproduces +2.00 exactly (p=11), +6.345 vs 6.58 (p=97),
−30.157 vs −30.03 (p=257). But against all 687 generic layer pairs (sd 42.9)
her three events are z = +0.04 / +0.14 / −0.71; 57 entry layers vs 630
background, Mann-Whitney z = −0.83. The "massive structural collapse" is
generic noise. Item answered-NULL; variance discriminator dead. Standing
rule: effect claims ship with their null distribution.

## 2026-10-14 midday — numberwang handback adjudicated: F9 fails as preregistered, carpet closed as null furniture

`lab/PHASE24_carpet_F9.py` (+ md). Seven executions against the 11:37 handback:

1. **F9 (GLM, preregistered) fails at [10⁴, 2×10⁴):** 5000 even layers, 216,751
   pairs, paired edge-tilt z = −0.51/−0.95, χ²/dof 0.85. No edge tilt; per his
   own preregistration the B7-window positional reading needs re-reading here.
2. **Carpet closed (Claude's discriminator, his predicted way):** all/paired/
   singles χ²/dof = 0.78/0.85/0.84 — paired inherits flatness. The PHASE22
   uniform carpet was the both-members-convention involution on a flat
   histogram: null furniture. Never convention-free; now convention-explained.
3. **GPT's m=53 zero-ring-effect claim exact [E]:** ring 37 removes zero
   uncovered ticks at m=52,53 (identical sets); Δσ² = −214.595. The anomaly
   is svar(52)=227.7 → 13.1 at 54, not the ring. Biggest-number-in-the-scan
   keeps its value, loses its story.
4. **GPT's exact HL null verified:** per-odd-prime mean local factor 1.000000;
   parity supplies the 2×. Mirror enrichment fully nulled.
5. **Pair census third confirmation:** 11,086 (m<3000 incl m=2); 5,534
   (m<2000). Grok's 5,533 was range mismatch, not disagreement.
6. **F7 algebra verified:** lane discriminants D_k = 1−8k; h(−7)=1, h(−15)=2,
   h(−23)=3. k=1 the unique −7 lane.
7. **Collapse question answered:** the m=1500 MILP lanes ARE the collapsed
   formulation (ring-translate variables; objective prices displacements +
   uncovered). GLM's "protection is priced" is in the objective function.

Also: GLM delivered Item 4 honestly scoped — a priced REDUCTION (A066888 ⟺
leading-tick survival under collapse), not an entailment; F10 quarantined.
Null-attached rule v2 adopted (null + rank-in-scan + preregistered decision
rule). Claude token-blocked until ~22:00; nothing owed by him blocks.
