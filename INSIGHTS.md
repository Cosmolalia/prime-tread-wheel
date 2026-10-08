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
- Opening tick T(m-1)+1 is odd by construction -> prime at exactly 2x
  random-density (observed 2385 vs 1193 expected for m<=2e4 = ratio 2.000 —
  pure parity selection, no structure). [E]
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
